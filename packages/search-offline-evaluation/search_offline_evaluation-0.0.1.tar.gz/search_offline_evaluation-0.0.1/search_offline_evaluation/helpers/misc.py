from collections import defaultdict
from typing import Dict, Any


def get_prefix_before_at(name: str) -> str:
    """
    Extracts the prefix before the "@" character in a string.
    Args:
        name (str): The input string.

    Returns:
        str: The prefix before the "@" character.
    """
    return name.split("@")[0]


def transform_results(
    original_dict: Dict[str, Dict[str, Dict[str, Any]]]
) -> Dict[str, Dict[str, Any]]:
    """
    Transforms a dictionary of metrics to be more compliant with MLFlow.

    Args:
        original_dict (Dict[str, Dict[str, Dict[str, Any]]]): The original dictionary of metrics.

    Returns:
        Dict[str, Dict[str, Any]]: The transformed dictionary.
    """
    # Initialize the transformed dictionary
    transformed_dict = {}

    # Iterate through the original dictionary
    for k, v in original_dict.items():
        for run, metrics in v.items():
            if run not in transformed_dict:
                transformed_dict[run] = {}
            for metric, value in metrics.items():
                transformed_dict[run][metric] = value

    return transformed_dict


# Function to merge dictionaries
def merge_dicts(
    d1: Dict[str, Dict[str, Any]], d2: Dict[str, Dict[str, Any]]
) -> Dict[str, Dict[str, Any]]:
    """
    Merges two dictionaries.

    Args:
        d1 (Dict[str, Dict[str, Any]]): The first dictionary.
        d2 (Dict[str, Dict[str, Any]]): The second dictionary.

    Returns:
        Dict[str, Dict[str, Any]]: The merged dictionary.
    """
    merged_dict = defaultdict(dict)

    for key, value in d1.items():
        if key in d2:
            merged_dict[key].update(value)
        else:
            merged_dict[key] = value
    for key, value in d2.items():
        if key in d1:
            merged_dict[key].update(value)
        else:
            merged_dict[key] = value

    return merged_dict
