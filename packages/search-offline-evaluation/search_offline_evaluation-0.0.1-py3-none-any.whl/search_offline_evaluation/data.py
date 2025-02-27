from pathlib import Path
from typing import Iterator
from search_offline_evaluation.schemas import Ad, Query
from pydantic import BaseModel

import pyarrow.parquet as pq


class RetrievalFileRow(BaseModel):
    id: int
    query: Query
    rankings: dict[str, list[Ad]]


def read_retrieval_file(file: Path) -> Iterator[RetrievalFileRow]:
    table = pq.read_table(file)

    for row in table.to_pylist():
        yield RetrievalFileRow(**row)


def read_retrieval_file_only_query_ids(file: Path) -> Iterator[int]:
    table = pq.read_table(file, columns=["id"])

    for row in table.to_pylist():
        yield row["id"]
