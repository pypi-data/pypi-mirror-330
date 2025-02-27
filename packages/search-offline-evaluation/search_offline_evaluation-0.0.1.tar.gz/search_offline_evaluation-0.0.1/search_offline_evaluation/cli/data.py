from functools import lru_cache
from pathlib import Path
import duckdb
import typer
import pyarrow.parquet as pq
import shutil

app = typer.Typer()


@lru_cache
def get_duckdb_connection() -> duckdb.DuckDBPyConnection:
    conn = duckdb.connect(":memory:")
    return conn


def create_view_queries(queries_file: Path, conn: duckdb.DuckDBPyConnection | None = None) -> None:
    if conn is None:
        conn = get_duckdb_connection()
    queries_file = str(queries_file) + "/*.parquet"
    conn.execute(f"CREATE OR REPLACE VIEW queries AS SELECT * FROM '{queries_file}'")


def create_view_relevances(
    relevances_file: Path, conn: duckdb.DuckDBPyConnection | None = None
) -> None:
    if conn is None:
        conn = get_duckdb_connection()
    relevances_file = str(relevances_file) + "/**/*.parquet"
    conn.execute(f"CREATE OR REPLACE VIEW relevances AS SELECT * FROM '{relevances_file}'")


def create_view_dim_ad(conn: duckdb.DuckDBPyConnection | None = None) -> None:
    if conn is None:
        conn = get_duckdb_connection()
    # TODO get the ranking names dynamically
    _query = """
        CREATE OR REPLACE VIEW dim_ad AS (
            WITH all_ads AS (
                SELECT UNNEST(rankings.olx_search) AS ad FROM queries
                UNION ALL
                SELECT UNNEST(rankings.qdrant_mclip_image_openai_512_text_concatenation) AS ad FROM queries
            )
            SELECT ad.id AS id, ad FROM all_ads QUALIFY ROW_NUMBER() OVER (PARTITION BY id ORDER BY ad.created_time DESC) = 1
        )
    """
    conn.execute(_query)


def create_final_view(conn: duckdb.DuckDBPyConnection | None = None) -> None:
    if conn is None:
        conn = get_duckdb_connection()
    _query = """
        CREATE OR REPLACE VIEW final AS (
            SELECT
                r.*,
                dim_ad.ad AS ad,
                queries.query AS query
            FROM relevances AS r
            LEFT JOIN dim_ad ON r.ad_id = dim_ad.id
            LEFT JOIN queries ON r.query_id = queries.id
        )
    """
    conn.execute(_query)


def export_final_view(output_file: Path, conn: duckdb.DuckDBPyConnection | None = None) -> None:

    output_file.mkdir()

    if conn is None:
        conn = get_duckdb_connection()
    _query = f"""
        COPY (SELECT * FROM final) 
        TO '{output_file}'
        (FORMAT PARQUET, PARTITION_BY agent)
    """
    conn.execute(_query)


@app.command()
def merge_files(queries_file: Path, relevances_file: Path, output_file: Path) -> None:
    if output_file.exists():
        typer.secho(f"Output file {output_file} already exists!", fg=typer.colors.RED)
        raise typer.Abort()

    create_view_queries(queries_file)
    create_view_relevances(relevances_file)
    create_view_dim_ad()
    create_final_view()
    export_final_view(output_file)


@app.command()
def transform_hive_partition(input: Path, output: Path) -> None:
    # Transforms a Hive partition into a multi-file parquet directory
    # This shouldn't be needed, once we update the read/write to use arrow
    dataset = pq.ParquetDataset(str(input))
    fragments = [(Path(fragment.path), idx) for idx, fragment in enumerate(dataset.fragments)]

    if output.exists():
        raise FileExistsError(f"Output directory {output} already exists!")

    output.mkdir()

    for fragment_path, idx in fragments:
        new_path = output / f"part={idx}.parquet"
        shutil.copy(str(fragment_path), str(new_path))
