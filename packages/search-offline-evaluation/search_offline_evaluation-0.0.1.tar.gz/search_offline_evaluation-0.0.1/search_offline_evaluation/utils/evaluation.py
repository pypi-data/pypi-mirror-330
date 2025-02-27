import logging
import traceback
import pandas as pd
from tqdm import tqdm
from ranx import Qrels, Run
from ranx import compare
from ranx import evaluate
from collections import OrderedDict
from search_offline_evaluation.utils.logging_config import setup_logging
from search_offline_evaluation.helpers.helpers import save_to_json, load_ranx_objects
from search_offline_evaluation.utils.annotator import Annotator
from search_offline_evaluation.utils.monitoring import log_mlflow


logger = setup_logging(__name__)


def retrieval_with_ranx(logs, vector_store, k):
    # Ground truth dataset
    # FIXME: grd_truth changes if we consider search_id, for now keyword only is not enough;
    # FIXME:,"params_search_id", "id", "order_by"
    grd_truth = (
        logs.astype(dtype={"id": str})
        .groupby(["keyword", "params_search_id", "id"])
        .agg({"label": max, "rank": "mean"})
        .reset_index()
    )

    grd_truth["rel_score"] = 1 / grd_truth["rank"]

    # Filter out rows where label=0
    filtered_df = grd_truth[grd_truth["label"] != 0]

    # Create the desired dictionary
    qrels = OrderedDict()
    baseline_run_dict = OrderedDict()

    # Sorting keywords to ensure consistent order
    sorted_keywords = sorted(logs["keyword"].unique())

    for keyword in sorted_keywords:
        keyword_group = filtered_df[filtered_df["keyword"] == keyword]
        if not keyword_group.empty:
            qrels[keyword] = keyword_group.set_index("id")["label"].to_dict()

        keyword_group_all = grd_truth[grd_truth["keyword"] == keyword]
        if not keyword_group_all.empty:
            baseline_run_dict[keyword] = keyword_group_all.set_index("id")["rel_score"].to_dict()

    # Vector Search results
    vector_dict = OrderedDict()
    for keyword in tqdm(sorted_keywords, desc="Processing keywords"):
        try:
            vector_dict[keyword] = dict(vector_store.get_ranking(text=keyword, k=k))
        except Exception as e:
            logger.error(f"Error when retrieving the ranking for {keyword}. Exception: {e}")
            logger.debug(traceback.format_exc())  # Optionally log the traceback

    # Now qrels_dict and run_dict are ready to be used with ranx
    qrels = Qrels(qrels)
    run_1 = Run(baseline_run_dict)
    run_2 = Run(vector_dict)

    return qrels, run_1, run_2


def metrics_per_query(text, qrels, vector_run, baseline_run):
    # Small adaptation so that we can use evaluate func from ranx
    run_1_sample = dict()
    run_1_sample[text] = baseline_run[text]

    run_2_sample = dict()
    run_2_sample[text] = vector_run[text]

    qrels_sample = dict()
    qrels_sample[text] = qrels[text]

    for at_k in [1, 3, 10]:
        metrics = [f"map@{at_k}", f"mrr@{at_k}", f"ndcg@{at_k}", f"recall@{at_k}"]
        logger.info(evaluate(qrels_sample, run_1_sample, metrics, make_comparable=True))
        logger.info(evaluate(qrels_sample, run_2_sample, metrics, make_comparable=True))


def display_results(results):
    # Assuming 'data' is your original dictionary
    records = []
    run_mapper = {"run_1": "baseline", "run_2": "vector"}
    for k, runs in results.items():
        for run, metrics in runs.items():
            for metric, value in metrics.items():
                # Check if the metric is 'F1' score specifically
                if "f1" in metric:
                    simple_metric = "F1"
                else:
                    # For other metrics, remove digits and '@'
                    simple_metric = "".join([i for i in metric if not i.isdigit()]).replace(
                        "@", ""
                    )
                records.append(
                    {
                        "k": k,
                        "Run": run_mapper[run],
                        "Metric": simple_metric,
                        "Value": value,
                    }
                )

    # Create a DataFrame
    df = pd.DataFrame(records)

    # Ensure 'k' is of type string for plotting purposes
    df["k"] = df["k"].astype(str)
    return df


def reporting(qrels, baseline_run, vector_run, k_values):
    results = {}
    for at_k_eval in k_values:
        report = compare(
            qrels=qrels,
            runs=[baseline_run, vector_run],
            metrics=[
                f"map@{at_k_eval}",
                f"mrr@{at_k_eval}",
                f"ndcg@{at_k_eval}",
                f"recall@{at_k_eval}",
                f"precision@{at_k_eval}",
                f"f1@{at_k_eval}",
            ],
            max_p=0.01,  # P-value threshold
            make_comparable=True,
        )
        results[at_k_eval] = report.results
        logger.info(report)

    return results


def extrinsic_evaluation(country, run_dir, to_mlflow=True):
    logger.info("Extrinsic Evaluation")
    qrels, baseline, run_1 = load_ranx_objects(run_dir)
    extrinsic_metrics = reporting(qrels, baseline, run_1, k_values=[3, 10])
    save_to_json(extrinsic_metrics, "extrinsic_metrics.json", run_dir)

    if to_mlflow:
        log_mlflow(
            country=country,
            metrics=extrinsic_metrics,
            run_dir=run_dir,
            annotation_source="extrinsic",
            nb_queries=len(baseline),
        )

    return extrinsic_metrics


def llm_evaluation(country, ads, data_dir, run_dir, to_mlflow=True):
    logger.info("LLMs Evaluation")
    annotator = Annotator(data_dir=data_dir, ads_data=ads)

    llm_qrels = annotator.llm_annotation(run_dir=run_dir, topk=2)
    _, baseline, vector_run = load_ranx_objects(run_dir)

    metrics = reporting(Qrels(llm_qrels), baseline, vector_run, k_values=[3, 10])
    save_to_json(metrics, "llm_metrics.json", run_dir)

    if to_mlflow:
        log_mlflow(
            country=country,
            metrics=metrics,
            run_dir=run_dir,
            annotation_source="llm",
            nb_queries=len(baseline),
            annotator=annotator,
        )

    return metrics
