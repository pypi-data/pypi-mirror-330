import json
import asyncio
import pandas as pd

from pathlib import Path
from itertools import chain

from tqdm.asyncio import tqdm_asyncio

from multiprocessing import current_process

from search_offline_evaluation.schemas import Ad
from search_offline_evaluation.utils.logging_config import setup_logging
from search_offline_evaluation.utils.agent import RelevanceAgent
from search_offline_evaluation.schemas import RelevanceJudgement


logger = setup_logging(__name__)


async def predict_relevance(
    agent: RelevanceAgent, query: str, ad: Ad
) -> RelevanceJudgement | None:
    relevance = await agent.arun(query=query, ad=ad)

    return (
        RelevanceJudgement(ad_id=ad.id, score=relevance.score) if relevance is not None else None
    )


async def batch_predict_relevance(
    agent: RelevanceAgent, query: str, ads: list[Ad]
) -> list[RelevanceJudgement | None]:
    return await asyncio.gather(*[predict_relevance(agent, query, ad) for ad in ads])


def unnest_rankings(rankings: dict) -> list[Ad]:
    ads_list = list(chain.from_iterable(rankings.values()))
    ads_dict = {ad["id"]: Ad(**ad) for ad in ads_list}
    return list(ads_dict.values())


def aggregate_serialize_judgements(judgments: list[RelevanceJudgement | None]) -> str:
    return json.dumps(
        {str(judgement.ad_id): judgement.score for judgement in judgments if judgement is not None}
    )


async def run_annotation(row: pd.Series, agent: RelevanceAgent) -> pd.Series:
    """Annotate a single row of the dataset."""
    id = row["id"]
    query = row["query"]
    rankings = row["rankings"]
    ads = unnest_rankings(rankings)
    if not ads:
        return pd.Series()
    results = await batch_predict_relevance(agent, query, ads)
    judgements = aggregate_serialize_judgements(results)
    return pd.Series({"id": id, "query": query, "judgements": judgements})


def list_parquet_files(input: Path) -> list[Path]:
    return list(input.glob("*.parquet"))


def write_data(data: list[pd.Series], filepath: Path) -> None:
    df = pd.DataFrame(data=data)
    df.to_parquet(filepath)


def worker(filepath: Path, output_dir: Path, agent: RelevanceAgent):
    current = current_process()
    if len(current._identity) > 0:
        tqdm_loop_position = current._identity[0]
    else:
        tqdm_loop_position = 1

    df = pd.read_parquet(filepath)
    filename = filepath.stem

    loop = asyncio.get_event_loop()

    futures = tqdm_asyncio.gather(
        *[run_annotation(row, agent) for _, row in df.iterrows()],
        desc=f"Inner Worker Requests [{filename}]",
        position=tqdm_loop_position,
        leave=False,
    )

    results = loop.run_until_complete(futures)
    write_data(results, Path(output_dir, f"{filename}_judgements.parquet"))
