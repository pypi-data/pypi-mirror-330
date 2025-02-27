import mlflow
from pathlib import Path
from search_offline_evaluation.utils.logging_config import setup_logging
from search_offline_evaluation.helpers.misc import get_prefix_before_at

logger = setup_logging(__name__)

# Define the mapper
run_mapper = {"run_1": "traditional_search", "run_2": "new_approach"}


# TODO: we can read directly from metrics.json instead of passing the variable
def log_mlflow(
    country: str,
    metrics: dict,
    run_dir: str,
    annotation_source: str,
    nb_queries: int,
    annotator: None = 0,
) -> None:
    """
    Logs metrics to MLflow.

    Args:
        country (str): The country code.
        metrics (dict): The metrics to log.
        run_dir (str): The directory where the run artifacts are stored.
        annotation_source (str): The source of the annotations.
        nb_queries (int): The number of queries.
        annotator (None, optional): The annotator object containing cost and sample information. Default is 0.
    """
    # MLFlow
    # TODO: set up dev, stg and prd
    endpoint = "http://127.0.0.1:8080"
    logger.info(f"MLFLOW log metrics into: {endpoint}")

    mlflow.set_tracking_uri(endpoint)
    mlflow.set_experiment("Relevance offline analysis")

    for k, run in metrics.items():
        for run_name, metrics_values in run.items():
            logger.info(f"RUN {run_name}")
            with mlflow.start_run(run_name=f"offline-relevance-evaluation"):
                mapped_run = run_mapper.get(run_name, run)
                mlflow.log_param("country", country)
                mlflow.log_param("run", mapped_run)
                mlflow.log_param("nb_queries", nb_queries)
                mlflow.log_param("at_k", k)
                mlflow.log_param("annotation_source", annotation_source)
                if annotator:
                    mlflow.log_param("cost", annotator.cost)
                    mlflow.log_param("nb_samples", annotator.annotated_samples)

                logger.info(f"MLFLOW log for {mapped_run}")

                # Log individual metrics
                for name, value in metrics_values.items():
                    mlflow.log_metric(f"{get_prefix_before_at(name)}", value)

                # Log artifact
                mlflow.log_artifact(Path(run_dir, f"{annotation_source}_metrics.json"))

            # End the current run
            mlflow.end_run()

    logger.info(f"Metrics logged to MLflow.")
