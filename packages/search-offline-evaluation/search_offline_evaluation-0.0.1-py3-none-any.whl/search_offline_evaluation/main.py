import pandas as pd
from pathlib import Path
from search_offline_evaluation.helpers.helpers import load_ranx_objects
from search_offline_evaluation.utils.annotator import Annotator
from search_offline_evaluation.utils.evaluation import reporting
from search_offline_evaluation.helpers.helpers import save_to_json


def main(
    start: str = "2024-03-15",
    end: str = "2024-04-15",
    country: str = "pt",
    ads_snapshot_date: str = "2024-04-01",
) -> None:

    data_dir = Path(__file__).parent.parent / "data"
    run_dir = Path(data_dir, "external", "test")
    Path(run_dir).mkdir(parents=True, exist_ok=True)

    ads_details = pd.DataFrame.from_dict(
        {
            "id": [123, 224, 225],
            "ad_info": ["iphone 13 blue, perfect condition", "dog bed", "springer spaniel"],
        }
    )
    ads_details.set_index("id", inplace=True)

    # Setting up the catalog, LLM needs access to ads dataset to make judgments based on text and description
    annotator = Annotator(data_dir=run_dir, ads_data=ads_details)

    # Evaluation on promoted section
    _ = annotator.llm_annotation(run_dir=run_dir, topk=3)

    #
    qrels, baseline, vector_run = load_ranx_objects(run_dir)

    metrics = reporting(qrels, baseline, vector_run, k_values=[3])
    save_to_json(metrics, "llm_metrics.json", run_dir)


if __name__ == "__main__":
    main()
