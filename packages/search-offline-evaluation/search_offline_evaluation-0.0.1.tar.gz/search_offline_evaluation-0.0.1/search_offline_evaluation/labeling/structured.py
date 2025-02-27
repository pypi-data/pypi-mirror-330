import asyncio
from multiprocessing import current_process
from typing import NamedTuple

import pandas as pd
from tqdm import tqdm
from search_offline_evaluation.data import (
    RetrievalFileRow,
    read_retrieval_file,
    read_retrieval_file_only_query_ids,
)


import random
from pathlib import Path

from search_offline_evaluation.schemas import Ad, Query, RelevanceJudgement
from search_offline_evaluation.utils.agent import RelevanceAgent, RelevanceOutput
from search_offline_evaluation.utils.logging_config import setup_logging

_LOGGER = setup_logging(__name__)


def decide_query_scores(input_path: Path, possible_scores: list[int]) -> dict[int, int]:
    all_queries = list(read_retrieval_file_only_query_ids(input_path))
    query_scores = random.choices(possible_scores, k=len(all_queries))
    return dict(zip(all_queries, query_scores))


class _StructuredAnnotation(NamedTuple):
    small_model: list[tuple[Ad, RelevanceOutput]]
    big_model: tuple[Ad, RelevanceOutput] | None = None


async def annotate_ad(agent: RelevanceAgent, query: Query, ad: Ad) -> RelevanceOutput | None:
    _query = query.text
    if query.filter_params is not None:
        _query = query.get_query_w_filters()
    try:
        relevance = await agent.arun(_query, ad)
    except Exception as e:
        _LOGGER.error(f"Error while annotating ad {ad.id} with query {query.id}: {e}")
        relevance = None

    return relevance if relevance is not None else None


async def structured_annotation(
    query: Query,
    ads: list[Ad],
    needed_relevance: int,
    small_agent: RelevanceAgent,
    big_agent: RelevanceAgent,
    big_agent_fallback: RelevanceAgent | None,
) -> _StructuredAnnotation:

    small_model_annotations = await asyncio.gather(
        *(annotate_ad(small_agent, query, ad) for ad in ads)
    )

    big_agent_ad = None
    for ad, relevance in zip(ads, small_model_annotations):
        if relevance is not None and relevance.score == needed_relevance:
            big_agent_ad = ad
            break
    if big_agent_ad is None:
        big_agent_ad = random.choice(ads)

    big_model_annotation = None
    big_model_annotation = await annotate_ad(big_agent, query, big_agent_ad)
    if big_model_annotation is None and big_agent_fallback is not None:
        _LOGGER.warning(
            "Annotating query: %d, ad: %d with big_agent_fallback!", query.id, big_agent_ad.id
        )
        big_model_annotation = await annotate_ad(big_agent_fallback, query, big_agent_ad)

    return _StructuredAnnotation(
        small_model=[
            (ad, relevance)
            for ad, relevance in zip(ads, small_model_annotations)
            if relevance is not None
        ],
        big_model=(ad, big_model_annotation) if big_model_annotation is not None else None,
    )


def _get_all_ads_wo_repetition(row: RetrievalFileRow) -> list[Ad]:
    all_ads: list[Ad] = []
    all_ads_ids: set[int] = set()
    for ranking_name in row.rankings.keys():
        for ad in row.rankings[ranking_name]:
            if ad.id not in all_ads_ids:
                all_ads_ids.add(ad.id)
                all_ads.append(ad)

    return all_ads


def _get_ads_sample(ads: list[Ad], num_ads_sample: int) -> list[Ad]:
    ads_sample: list[Ad]
    if len(ads) < num_ads_sample:
        ads_sample = ads
    else:
        ads_sample = random.sample(ads, num_ads_sample)

    return ads_sample


def file_row_worker(
    row: RetrievalFileRow,
    score: int,
    num_ads_sample: int,
    small_agent: RelevanceAgent,
    big_agent: RelevanceAgent,
    big_agent_fallback: RelevanceAgent | None,
) -> tuple[list[RelevanceJudgement], RelevanceJudgement | None] | None:
    all_ads = _get_all_ads_wo_repetition(row)
    ads_sample = _get_ads_sample(all_ads, num_ads_sample)

    if len(ads_sample) == 0:
        return None

    annotations = asyncio.run(
        structured_annotation(
            row.query, ads_sample, score, small_agent, big_agent, big_agent_fallback
        )
    )

    _small_agent_judgments = [
        RelevanceJudgement(ad_id=ad.id, score=relevance.score, reasoning=relevance.reasoning)
        for ad, relevance in annotations.small_model
    ]

    _big_agent_judgement = None
    if annotations.big_model is not None:
        _big_agent_judgement = RelevanceJudgement(
            ad_id=annotations.big_model[0].id,
            score=annotations.big_model[1].score,
            reasoning=annotations.big_model[1].reasoning,
        )

    return _small_agent_judgments, _big_agent_judgement


def write_judgments(path: Path, query: list[int], judgments: list[RelevanceJudgement]) -> None:

    df = pd.DataFrame(
        {
            "query_id": query,
            "ad_id": [judgment.ad_id for judgment in judgments],
            "score": [judgment.score for judgment in judgments],
            "reasoning": [judgment.reasoning for judgment in judgments],
        }
    )

    df.to_parquet(path)


def _write_file_judgments(
    input: Path,
    output: Path,
    small_agent_ids: list[int],
    small_agent_judgments: list[RelevanceJudgement],
    big_agent_ids: list[int],
    big_agent_judgments: list[RelevanceJudgement],
) -> None:

    output_small = output / "agent=small"
    if not output_small.exists():
        output_small.mkdir()

    output_big = output / "agent=big"
    if not output_big.exists():
        output_big.mkdir()

    if small_agent_judgments:
        write_judgments(
            output / f"agent=small/{input.stem}.parquet",
            small_agent_ids,
            small_agent_judgments,
        )

    if big_agent_judgments:
        write_judgments(
            output / f"agent=big/{input.stem}.parquet",
            big_agent_ids,
            big_agent_judgments,
        )


def file_worker(
    input: Path,
    output: Path,
    possible_scores: list[int],
    small_agent_num_ads: int,
    small_agent: RelevanceAgent,
    big_agent: RelevanceAgent,
    big_agent_fallback: RelevanceAgent = None,
) -> None:
    worker_num = current_process()
    if len(worker_num._identity) > 0:
        worker_num = worker_num._identity[0]
    else:
        worker_num = 1

    query_scores = decide_query_scores(input, possible_scores)
    all_queries = read_retrieval_file(input)

    small_agent_query_ids: list[int] = []
    small_agent_judgments: list[RelevanceJudgement] = []

    big_agent_judgments: list[RelevanceJudgement] = []
    big_agent_query_ids: list[int] = []
    for query in tqdm(
        all_queries,
        desc=f"Worker {worker_num} queries",
        position=worker_num,
        total=len(query_scores),
    ):

        row_output = file_row_worker(
            query,
            query_scores[query.id],
            small_agent_num_ads,
            small_agent,
            big_agent,
            big_agent_fallback,
        )

        if row_output is None:
            continue

        small_judgment, big_judgment = row_output

        small_agent_judgments.extend(small_judgment)
        small_agent_query_ids.extend([query.id] * len(small_judgment))

        if big_judgment is not None:
            big_agent_judgments.append(big_judgment)
            big_agent_query_ids.append(query.id)

    _write_file_judgments(
        input,
        output,
        small_agent_query_ids,
        small_agent_judgments,
        big_agent_query_ids,
        big_agent_judgments,
    )
