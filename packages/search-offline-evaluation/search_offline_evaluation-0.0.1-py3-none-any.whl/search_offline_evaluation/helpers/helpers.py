import os
import json
import numpy as np
from pathlib import Path
from ranx import Run, Qrels
from typing import Tuple


class NumpyEncoder(json.JSONEncoder):
    """Custom encoder for numpy data types"""

    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def convert_ranx_obj_to_dict(ranx_obj, obj_type: str = None):
    """Converts a Ranx object (either Qrels or Run) to a dictionary format suitable for serialization.

    Args:
        ranx_obj: The Ranx object to convert.
        obj_type (str): Specifies the type of Ranx object ('qrels' or 'run').

    Returns:
        dict: A dictionary representation of the Ranx object."""
    if obj_type == "qrels":
        # For Qrels, we assume relevance is binary and just keep the doc IDs
        return {
            query_id: {doc_id: score for doc_id, score in docs_scores.items()}
            for query_id, docs_scores in ranx_obj.qrels.items()
        }
    elif obj_type == "run":
        # For Run, preserve both doc IDs and their scores
        return {
            query_id: {doc_id: score for doc_id, score in docs_scores.items()}
            for query_id, docs_scores in ranx_obj.run.items()
        }


def convert_dict_to_ranx_obj(data_dict, obj_type: str = None):
    """Converts a dictionary back to a Ranx object (either Qrels or Run).

    Args:
        data_dict (dict): The dictionary representation of the Ranx object.
        obj_type (str): Specifies the type of Ranx object ('qrels' or 'run').

    Returns:
        Qrels or Run: The reconstructed Ranx object from the dictionary."""
    if obj_type == "qrels":
        # Convert dictionary back to Qrels object
        return Qrels(data_dict)
    elif obj_type == "run":
        # Convert dictionary back to Run object
        return Run(data_dict)


def save_to_json(data: dict, filename: str, directory: str):
    """
    Saves a dictionary to a JSON file in the specified directory using a custom Numpy encoder.

    Args:
        data (dict): The data to save.
        filename (str): The name of the file to create.
        directory (str): The directory in which to save the file.
    """
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, filename)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4, cls=NumpyEncoder)


def get_image_name(s3_url: str):
    """
    Extracts the filename from an S3 URL.

    Args:
        s3_url (str): The S3 URL from which to extract the filename.

    Returns:
        str: The filename extracted from the URL.
    """

    return s3_url.split("/")[-1]


def get_apollo_url(filename: str):
    """
    Constructs a URL for accessing an image stored on Apollo with specific parameters.

    Args:
        filename (str): The filename of the image to access.

    Returns:
        str: A URL constructed to access the image with specified parameters.
    """
    return f"https://ireland.apollo.olxcdn.com/v1/files/{filename}/image;s=300x0;q=50"


def load_ranx_objects(run_dir: str) -> Tuple[Qrels, Run, Run]:
    """
    Loads Qrels and Run objects from JSON files in the specified directory.

    Args:
        run_dir (str): Directory where the JSON files are stored.

    Returns:
        Tuple[Qrels, Run, Run]: Loaded Qrels, baseline Run, and vector Run objects.
    """

    with open(Path(run_dir, "qrels.json"), "r") as f:
        labels = json.load(f)

    # Remove parent keys if any of their values are null
    filtered_labels = {
        k: v for k, v in labels.items() if not any(value is None for value in v.values())
    }

    with open(Path(run_dir, "llm_control.json"), "r") as f:
        baseline = json.load(f)

    with open(Path(run_dir, "llm_test.json"), "r") as f:
        run_1 = json.load(f)

    return Qrels(filtered_labels), Run(baseline), Run(run_1)


def save_results(qrels: Qrels, baseline_run: Run, vector_run: Run, output_dir: str) -> None:
    """
    Saves Qrels and Run objects to JSON files in the specified directory.

    Args:
        qrels (Qrels): Qrels object to save.
        baseline_run (Run): Baseline Run object to save.
        vector_run (Run): Vector Run object to save.
        output_dir (str): Directory where the JSON files will be saved.
    """

    # Convert objects to dictionaries
    qrels_dict = convert_ranx_obj_to_dict(qrels, obj_type="qrels")
    baseline_dict = convert_ranx_obj_to_dict(baseline_run, obj_type="run")
    vector_dict = convert_ranx_obj_to_dict(vector_run, obj_type="run")

    # Save to JSON files
    save_to_json(qrels_dict, "qrels.json", output_dir)
    save_to_json(baseline_dict, "baseline_run_results.json", output_dir)
    save_to_json(vector_dict, "vector_run_results.json", output_dir)


def load_file(dir_path: Path, filename) -> dict:
    # TODO: From S3 in the future (SEARCH-1129)
    file_path = Path(dir_path, filename)
    if file_path.is_file():
        with open(file_path, "r") as f:
            annotations = json.load(f)
            return annotations
    else:
        return {}
