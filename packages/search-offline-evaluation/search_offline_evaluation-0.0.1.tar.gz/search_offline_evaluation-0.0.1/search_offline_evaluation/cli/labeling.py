from concurrent.futures import ProcessPoolExecutor, as_completed
from enum import Enum
from pathlib import Path
from tqdm import tqdm

from search_offline_evaluation.labeling.simple import list_parquet_files, worker
from search_offline_evaluation.labeling.structured import file_worker
from search_offline_evaluation.prompts import (
    MULTI_DEGREE_RELEVANCE_PROMPT_SCORES,
    binary_relevance_prompt,
    multi_degree_relevance_magic_prompt,
    multi_degree_relevance_prompt,
)
from search_offline_evaluation.cli.logs import cli_log_setup
from search_offline_evaluation.utils.agent import ImageRelevanceAgent, ModelConfig, RelevanceAgent
from typing_extensions import Annotated
import typer


labeling_app = typer.Typer()


class PromptChoices(str, Enum):
    binary = "binary"
    multi_degree = "multi_degree"
    multi_degree_magic = "multi_degree_magic"


_PROMPT_CHOICE_MAP = {
    PromptChoices.binary: binary_relevance_prompt,
    PromptChoices.multi_degree: multi_degree_relevance_prompt,
    PromptChoices.multi_degree_magic: multi_degree_relevance_magic_prompt,
}


class LabellerModel(str, Enum):
    gpt_4o_mini = "gpt-4o-mini"
    gpt_4o = "gpt-4o"


@labeling_app.command()
def relevance(
    input: Annotated[Path, typer.Argument(help="Input directory to the parquet files")],
    output: Annotated[
        Path, typer.Argument(help="Output directory to save parquet files", exists=False)
    ],
    max_workers: Annotated[int, typer.Option(help="Maximum concurrent workers/processes")] = 4,
    max_requests: Annotated[
        int, typer.Option(help="Maximum requests to the LLM provider per second")
    ] = 50,
    prompt: Annotated[
        PromptChoices, typer.Option(help="Prompt to use")
    ] = PromptChoices.multi_degree_magic,
    labeller_model: Annotated[
        LabellerModel, typer.Option(help="Model to use for labeling")
    ] = LabellerModel.gpt_4o_mini,
):
    input_dir = Path(input)
    output_dir = Path(output)
    output_dir.mkdir(exist_ok=True, parents=True)

    file_paths = list_parquet_files(input_dir)

    # Setup the agent
    model_config = ModelConfig(
        model_name=labeller_model.value,
        max_tokens=512,
        temperature=0.0,
        top_p=1.0,
    )

    if len(file_paths) < max_workers:
        max_workers = len(file_paths)

    max_requests_per_worker = max_requests // max_workers
    _prompt = _PROMPT_CHOICE_MAP[prompt]()
    agent = RelevanceAgent(
        system_prompt=_prompt,
        model_configuration=model_config,
        rate_limiter=max_requests_per_worker,
    )

    typer.echo(f"Starting to label files using prompt: {prompt}, model: {labeller_model}")

    if max_workers == 1:
        for filepath in tqdm(
            file_paths, desc="Files Processed", position=0, total=len(file_paths)
        ):
            worker(filepath, output, agent)
    else:
        with ProcessPoolExecutor(max_workers=max_workers, initializer=(cli_log_setup)) as executor:
            futures = [
                executor.submit(worker, filepath, output_dir, agent) for filepath in file_paths
            ]
            for future in tqdm(
                as_completed(futures),
                desc="Files Processed",
                total=len(file_paths),
                position=0,
            ):
                future.result()


@labeling_app.command()
def relevance_structured(
    input: Annotated[Path, typer.Argument(help="Input directory to the parquet files")],
    output: Annotated[
        Path, typer.Argument(help="Output directory to save parquet files", exists=False)
    ],
    max_workers: Annotated[int, typer.Option(help="Maximum concurrent workers/processes")] = 5,
    max_requests: Annotated[
        int, typer.Option(help="Maximum requests to the LLM provider per second")
    ] = 50,
    annotations_per_query_small_agent: Annotated[
        int, typer.Option(help="Number of annotations that the small agent used will do")
    ] = 50,
    prompt: Annotated[
        PromptChoices, typer.Option(help="Prompt to use")
    ] = PromptChoices.multi_degree_magic,
):

    output.mkdir(parents=True)

    possible_scores = MULTI_DEGREE_RELEVANCE_PROMPT_SCORES
    file_paths = list_parquet_files(input)

    if len(file_paths) < max_workers:
        max_workers = len(file_paths)

    max_requests_per_worker = max_requests // max_workers

    prompt = _PROMPT_CHOICE_MAP[prompt]()

    model_config = ModelConfig(
        model_name="gpt-4o-mini",
        max_tokens=512,
        temperature=0.0,
        top_p=1.0,
    )
    small_agent = RelevanceAgent(
        system_prompt=prompt,
        model_configuration=model_config,
        rate_limiter=max_requests_per_worker,
    )

    model_config = ModelConfig(
        model_name="gpt-4o",
        max_tokens=512,
        temperature=0.0,
        top_p=1.0,
    )
    big_agent = ImageRelevanceAgent(
        system_prompt=prompt,
        model_configuration=model_config,
        rate_limiter=max_requests_per_worker,
    )
    big_agent_fallback = RelevanceAgent(
        system_prompt=prompt,
        model_configuration=model_config,
        rate_limiter=max_requests_per_worker,
    )

    if max_workers == 1:
        for filepath in tqdm(
            file_paths, desc="Files Processed", position=0, total=len(file_paths)
        ):
            file_worker(
                filepath,
                output,
                possible_scores,
                annotations_per_query_small_agent,
                small_agent,
                big_agent,
                big_agent_fallback,
            )

    else:
        with ProcessPoolExecutor(max_workers=max_workers, initializer=(cli_log_setup)) as executor:
            futures = [
                executor.submit(
                    file_worker,
                    filepath,
                    output,
                    possible_scores,
                    annotations_per_query_small_agent,
                    small_agent,
                    big_agent,
                    big_agent_fallback,
                )
                for filepath in file_paths
            ]
            for future in tqdm(
                as_completed(futures),
                desc="Files Processed",
                total=len(file_paths),
                position=0,
            ):
                future.result()
