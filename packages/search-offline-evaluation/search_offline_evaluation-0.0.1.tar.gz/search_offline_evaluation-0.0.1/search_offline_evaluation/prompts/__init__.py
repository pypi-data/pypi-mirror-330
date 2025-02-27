from functools import lru_cache
from pathlib import Path

prompt_dir = Path(__file__).parent


def read_prompt(prompt_path: str) -> str:
    with open(prompt_path, "r") as f:
        return f.read().strip()


MULTI_DEGREE_RELEVANCE_PROMPT_SCORES: list[int] = [0, 1, 2, 3, 4]


@lru_cache
def multi_degree_relevance_prompt() -> str:
    return read_prompt(prompt_dir / "multi_degree_relevance.prompt")


@lru_cache
def binary_relevance_prompt() -> str:
    return read_prompt(prompt_dir / "binary_relevance.prompt")


@lru_cache
def multi_degree_relevance_magic_prompt() -> str:
    return read_prompt(prompt_dir / "multi_degree_relevance_magic.prompt")
