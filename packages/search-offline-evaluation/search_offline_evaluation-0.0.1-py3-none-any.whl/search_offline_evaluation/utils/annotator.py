import json
import logging
import time
import requests
import pandas as pd
from tqdm import tqdm
from pathlib import Path
from search_offline_evaluation.prompts import prompt_dir, read_prompt
from search_offline_evaluation.helpers.misc import merge_dicts
from search_offline_evaluation.helpers.helpers import load_file
from search_offline_evaluation.utils.logging_config import setup_logging
from search_offline_evaluation.utils.agent import RelevanceAgent, ModelConfig
from ratelimit import limits, sleep_and_retry

logger = setup_logging(__name__)


class Annotator:
    """Annotator class for managing and generating relevance annotations for ads."""

    def __init__(self, data_dir: str, ads_data: pd.DataFrame):
        self.model_config = ModelConfig(
            model_name="gpt-4o",
            max_tokens=512,
            temperature=0.0,
            top_p=1.0,
        )
        system_prompt = read_prompt(Path(prompt_dir, "binary_relevance.prompt"))
        self.agent = RelevanceAgent(
            system_prompt=system_prompt, model_configuration=self.model_config
        )
        self.annotations_dir = Path(data_dir, "annotations")
        self.cache = load_file(self.annotations_dir, "cache.json")
        self.cache_raw = load_file(self.annotations_dir, "cache_raw.json")
        self.qrels = {}  # All annotations from 2 runs
        self.catalog = ads_data
        self.cost = 0
        self.annotated_samples = 0

    def save_progress(self, ranx_dict, filepath, run_dir, llm_qrels):
        """
        Save annotations and ranx_dict to disk.

        Parameters:
        ranx_dict (dict): Dictionary containing ranking data.
        filepath (Path): Path to the file.
        run_dir (Path): Directory to save the run files.
        llm_qrels (dict): Dictionary containing LLM QRELs.
        """
        logger.debug(f"Save progress")
        with open(
            Path(run_dir, f"llm_{filepath.name.split('_results')[0]}.json"),
            "w",
        ) as f:
            json.dump(ranx_dict, f, indent=4)

        Path(self.annotations_dir).mkdir(parents=True, exist_ok=True)

        with open(Path(self.annotations_dir, f"cache.json"), "w") as f:
            json.dump(self.cache, f, indent=4)

        with open(Path(self.annotations_dir, f"cache_raw.json"), "w") as f:
            json.dump(self.cache_raw, f, indent=4)

        with open(Path(run_dir, f"qrels.json"), "w") as f:
            json.dump(llm_qrels, f, indent=4)

    def get_ad_details(self, ad_id: int):
        """
        Retrieve ad details from the catalog.

        Parameters:
        ad_id (int): The ID of the ad to retrieve.

        Returns:
        DataFrame: A DataFrame containing ad details.
        """
        ad_details = pd.DataFrame()
        try:
            # Check if ad_id exists in the catalog
            if ad_id in self.catalog.index:
                ad_details = self.catalog.loc[ad_id, ["ad_info"]]
            else:
                logging.warning(f"Ad ID {ad_id} is not available in the catalog.")

            return ad_details
        except KeyError as e:
            logging.error(f"KeyError: {e} - The catalog may not have the expected structure.")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")

    @sleep_and_retry
    @limits(calls=100, period=60)  # 100 calls within 1 minute
    def call_agent(self, query, ad_details):
        """
        Call the agent with rate limiting.

        Parameters:
        query (str): The query to send to the agent.
        ad_details (dict): Details of the ad to include in the query.

        Returns:
        dict: The response from the agent.
        """
        return self.agent.run(query=query, ad=ad_details).model_dump()

    def cache_update(self, query, relevance_dict, ad_details):
        """
        Update the cache with relevance scores and ad details.

        Parameters:
        query (str): The query string.
        relevance_dict (dict): Dictionary containing relevance information.
        ad_details (dict): Details of the ad.
        """
        logger.debug(f"Updating cache {relevance_dict.get('id')}, query: {query}")
        if not self.cache.get(query):
            self.cache[query] = {}

        if not self.cache_raw.get(query):
            self.cache_raw[query] = {}

        self.cache[query][relevance_dict.get("id")] = relevance_dict.get("relevance").get("score")
        ad_with_relevance = {**ad_details, **relevance_dict}
        self.cache_raw[query][relevance_dict.get("id")] = ad_with_relevance
        self.cost += relevance_dict.get("relevance").get("metadata").get("cost")
        self.annotated_samples += 1

    def get_annotation(self, query: str, ad_id: str) -> dict:
        """
        Retrieves or generates a relevance annotation for a given query and ad ID.
        Args:
            query (str): The search query.
            ad_id (str): The ad ID.
        Returns:
            dict: The ad details with relevance annotation.

        """

        ad_details = self.get_ad_details(int(ad_id))

        saved_annotation = None
        if self.cache.get(query):
            saved_annotation = self.cache.get(query).get(str(ad_id))

        if saved_annotation is not None:
            logger.debug(f"Getting annotation from memory: {query}, ad_id: {ad_id}.")
            relevance_dict = {"relevance": {"score": saved_annotation}, "id": ad_id}
        elif ad_details.empty:
            logger.debug(f"Missing ad information, ad_id: {ad_id}.")
            # FIXME: find a better way to handle missing ads (SEARCH-1138)
            # FIXME: ads with status = 'outdated' do not appear in the original tables if they were created
            # FIXME: before retention period, they will no longer appear, mitigation: access source tables maybe.
            relevance_dict = {"relevance": {"score": None}, "id": ad_id}
        else:
            logger.debug(f"LLM annotation: {query}, ad_id: {ad_id}.")
            relevance_output = self.call_agent(query, ad_details)
            relevance_dict = {"relevance": relevance_output, "id": ad_id}

            self.cache_update(query, relevance_dict, ad_details)

        return {**ad_details, **relevance_dict}

    # TODO: sleep and retry should most likely be put elsewhere, we don't need a buffer to get annotations from mem
    def get_annotation_with_retry(self, query, ad_id, retries=3, backoff_factor=0.3):
        """Get annotation with retry mechanism and rate limiting."""
        for attempt in range(retries):
            try:
                return self.get_annotation(query, ad_id)
            except requests.exceptions.Timeout as e:
                logger.warning(
                    f"Timeout for query: {query}, ad_id: {ad_id}. Attempt {attempt + 1} of {retries}."
                )
                time.sleep(backoff_factor * (2**attempt))  # Exponential backoff
            except Exception as e:
                logger.error(
                    f"Failed to get annotation for query: {query}, ad_id: {ad_id}. Error: {e}"
                )
                raise e  # Re-raise the exception for non-timeout errors
        raise requests.exceptions.Timeout(
            f"Failed to get annotation after {retries} attempts for query: {query}, ad_id: {ad_id}."
        )

    def llm_annotation(self, run_dir: Path, topk: int) -> dict:
        """
        Generates LLM annotations for search results in the given directory.
        Args:
            run_dir (Path): Directory containing search results.
            topk (int): Number of top results to annotate.
        Returns:
            dict: Generated LLM annotations in ranx format.
        """

        llm_qrels = {}
        filepaths = run_dir.rglob("*_results.json")
        try:
            for filepath in filepaths:
                with open(Path(run_dir, filepath.name), "r") as f:
                    search_results = json.load(f)
                logger.debug(f"Number of search requests: {len(list(search_results.keys()))}")
                ranx_dict = {}  # Saving annotations into ranx format to be used later
                for query, ads in tqdm(
                    search_results.items(), desc=f"Getting annotations [{filepath.name}]"
                ):
                    logger.info(f"Getting annotations for query: [{query}]")
                    ranx_dict[query] = {}
                    for ad_id in list(ads.keys())[
                        0:topk
                    ]:  # tqdm(list(ads.keys())[0:topk], desc=f"Processing ads for query [{query}]",
                        # leave=False, dynamic_ncols=True):
                        try:
                            ad_with_relevance = self.get_annotation_with_retry(query, ad_id)

                            ranx_dict[query][ad_id] = ad_with_relevance.get("relevance").get(
                                "score"
                            )
                        except requests.exceptions.Timeout as e:
                            logger.error(f"Timeout error: {e}")
                            self.save_progress(ranx_dict, filepath, run_dir, llm_qrels)
                            raise e

                llm_qrels = merge_dicts(llm_qrels, ranx_dict)
                self.save_progress(ranx_dict, filepath, run_dir, llm_qrels)

        except Exception as e:
            logger.error(f"An error occurred: {e}")
            # Save progress in case of an error
            self.save_progress(ranx_dict, filepath, run_dir, llm_qrels)

        return llm_qrels

    def upload_to_s3(self) -> None:
        # TODO: Upload annotations that are stored in llm_annotations_archived.json into S3 (SEARCH-1129)
        pass
