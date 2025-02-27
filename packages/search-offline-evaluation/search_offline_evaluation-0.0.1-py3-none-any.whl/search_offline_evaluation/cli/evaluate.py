from pathlib import Path
from ranx import Qrels, Run, compare
from typer import Typer
from pydantic import BaseModel
import pyarrow.parquet as pq

from search_offline_evaluation.labeling.simple import list_parquet_files
from search_offline_evaluation.utils.logging_config import setup_logging

evaluate_app = Typer()
_logger = setup_logging(__name__)


class RankedAd(BaseModel):
    id: int
    score: float | None = None


class RankingRow(BaseModel):
    query_id: int
    ranking: list[RankedAd]


# RankingRows indexed by query id
RankingData = dict[int, RankingRow]


def _load_ranking_data(ranking: Path) -> RankingData:
    if ranking.is_file():
        file_paths = [ranking]
    else:
        file_paths = list_parquet_files(ranking)

    output: dict[int, RankingRow] = {}
    for file in file_paths:
        table = pq.read_table(file, columns=["query_id", "ranking"])

        for row in table.to_pylist():
            ranking_row = RankingRow.model_validate(row)
            if ranking_row.query_id in output:
                _logger.warning(
                    f"Duplicate query id {ranking_row.query_id} found in ranking {file}!"
                )
            output[ranking_row.query_id] = ranking_row
    return output


def _create_qrels(judgement_data: RankingData) -> Qrels:
    qrels: dict[str, dict[str, float]] = {}

    for query, judgement in judgement_data.items():
        _query = str(query)
        qrels[_query] = {}
        for position, ad in enumerate(judgement.ranking):
            _ad_id = str(ad.id)
            _score = 1 / (position + 1)
            if ad.score is not None:
                _score = ad.score

            qrels[_query][_ad_id] = _score

    return Qrels(qrels, name="ground_truth")


def _create_runs(rankings: list[tuple[str, RankingData]]) -> list[Run]:
    runs: dict[str, dict[str, dict[str, float]]] = {}

    for ranking_name, ranking_data in rankings:
        runs[ranking_name] = {}
        for query, ranking_row in ranking_data.items():
            _query = str(query)
            runs[ranking_name][_query] = {}
            for position, ad in enumerate(ranking_row.ranking):
                _ad_id = str(ad.id)
                _score = 1 / (position + 1)
                if ad.score is not None:
                    _score = ad.score
                runs[ranking_name][_query][_ad_id] = _score

    return [Run(run=run, name=name) for name, run in runs.items()]


def _validate_data(
    judgement: RankingData,
    rankings: list[tuple[str, RankingData]],
) -> None:
    for ranking in judgement.values():
        for ad in ranking.ranking:
            if ad.score is None:
                raise ValueError("Judgement data must have scores for all ads!")

    for name, ranking in rankings:
        if ranking.keys() != judgement.keys():
            raise ValueError(f"Query ids in ranking {name} and judgement data do not match!")


def _load_rankings(rankings: list[Path]) -> list[tuple[str, RankingData]]:
    rankings_data = []
    for path in rankings:
        ranking_name = path.stem
        ranking_data = _load_ranking_data(path)
        rankings_data.append((ranking_name, ranking_data))
    return rankings_data


@evaluate_app.command()
def ranking(judgments: Path, rankings: list[Path]) -> dict:

    judgement_data = _load_ranking_data(judgments)
    rankings_data = _load_rankings(rankings)

    _validate_data(judgement_data, rankings_data)

    qrels = _create_qrels(judgement_data)
    runs = _create_runs(rankings_data)

    report = compare(
        qrels=qrels,
        runs=runs,
        metrics=["ndcg", "mrr", "map", "ndcg@10", "mrr@10", "map@10"],
    )
    print(report)
    return report.to_dict()


if __name__ == "__main__":

    out = ranking(
        Path("data/golden_evalset_o1.parquet"),
        [Path("data/golden_evalset_o1.parquet"), Path("data/golden_evalset_4o.parquet")],
    )

    assert out
