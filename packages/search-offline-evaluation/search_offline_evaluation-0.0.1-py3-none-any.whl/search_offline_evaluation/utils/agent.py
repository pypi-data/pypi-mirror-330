"""Relevance Agent LLM provided by GenAI Team."""

import logging
import os
import json
import litellm
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Union
from dotenv import dotenv_values
from pydantic import BaseModel, ValidationError, field_validator
from asynciolimiter import Limiter

from search_offline_evaluation.schemas import Ad
from search_offline_evaluation.utils.logging_config import setup_logging

_LOGGER = _LOGGER = setup_logging(__name__)

ALLOWED_MODELS = [
    "gpt-4o",
    "gpt-4o-mini",
]

MODEL_COSTS: Dict[str, Dict[str, float]] = {
    "gpt-4o": {
        "prompt_tokens": 2.5,
        "completion_tokens": 10,
    },
    "gpt-4o-mini": {
        "prompt_tokens": 0.15,
        "completion_tokens": 0.6,
    },
}


def compute_completion_cost(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    return (
        prompt_tokens * MODEL_COSTS[model]["prompt_tokens"] / 1_000_000
        + completion_tokens * MODEL_COSTS[model]["completion_tokens"] / 1_000_000
    )


class ModelConfig(BaseModel):
    model_name: str = "gpt-4o-mini"
    max_tokens: int = 512
    temperature: float = 0.0
    top_p: float = 1.0

    @field_validator("model_name")
    @classmethod
    def validate_model_name_is_allowed(cls, model_name: str) -> str:
        if model_name not in ALLOWED_MODELS:
            raise ValueError(
                f"Model {model_name} is not supported. Suported models are {ALLOWED_MODELS}"
            )
        return model_name


class Metadata(BaseModel):
    cost: float
    prompt_tokens: int
    completion_tokens: int
    timestamp: str


class LLMRelevanceAnnotationOutput(BaseModel):
    score: int
    reasoning: str


class RelevanceOutput(BaseModel):
    score: int
    reasoning: str
    metadata: Metadata


class ChatMessage(BaseModel):
    role: str
    content: Union[str, list]


def prepare_ad_prompt(ad: Ad) -> str:
    _ad_str = f"""
        title: {ad.title} 
    """

    if ad.price is not None:
        _ad_str += f"price: {ad.price} "

    if ad.state is not None:
        _ad_str += f"state: {ad.state} "

    if ad.params is not None:
        _ad_str += f"params: {ad.params} "

    _ad_str += f"description: {ad.description} "
    return _ad_str


class RelevanceAgent:

    @staticmethod
    def get_key():
        script_dir = Path(__file__).resolve().parents[2]
        env_path = Path(script_dir, ".env")
        config = dotenv_values(env_path)
        return config["OPENAI_API_KEY"]

    @staticmethod
    def get_base_url():
        return os.environ.get("BASE_URL")

    def __init__(
        self,
        system_prompt: str,
        model_configuration: ModelConfig,
        base_url: str | None = None,
        rate_limiter: int | None = None,
    ):

        self.system_prompt = system_prompt
        self.model_configuration = model_configuration
        self.key = self.get_key()
        if base_url is not None:
            self._base_url = base_url
        else:
            self._base_url = self.get_base_url()

        self._rate_limiter: Limiter | None = None
        if rate_limiter is not None:
            self._rate_limiter = Limiter(rate_limiter)

    def prepare_messages(self, query: str, ad: Ad) -> List[ChatMessage]:
        user_messages: List[Dict[str, Any]] = [
            {"type": "text", "text": f"Query: {query}"},
            {"type": "text", "text": f"Ad: {prepare_ad_prompt(ad)}"},
        ]
        return [
            ChatMessage(role="system", content=self.system_prompt),
            ChatMessage(role="user", content=user_messages),
        ]

    def _parse_response(self, response: litellm.ModelResponse) -> RelevanceOutput | None:
        metadata = Metadata(
            cost=compute_completion_cost(
                model=self.model_configuration.model_name,
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
            ),
            prompt_tokens=response.usage.prompt_tokens,
            completion_tokens=response.usage.completion_tokens,
            timestamp=datetime.now().isoformat(),
        )

        # probably not needed since we are using the response format constraint
        try:
            data = LLMRelevanceAnnotationOutput.model_validate_json(
                response.choices[0].message.content
            )
        except ValidationError as e:
            _LOGGER.error(f"Error parsing : {e}")
            return None

        return RelevanceOutput(score=data.score, reasoning=data.reasoning, metadata=metadata)

    async def _limit(self):
        if self._rate_limiter is not None:
            await self._rate_limiter.wait()

    async def arun(self, query: str, ad: Dict[str, Any]) -> RelevanceOutput | None:
        messages = self.prepare_messages(query, ad)
        await self._limit()
        response = await litellm.acompletion(
            model=self.model_configuration.model_name,
            base_url=self._base_url,
            api_key=self.key,
            messages=[message.model_dump() for message in messages],
            response_format=LLMRelevanceAnnotationOutput,
            max_tokens=self.model_configuration.max_tokens,
            temperature=self.model_configuration.temperature,
            top_p=self.model_configuration.top_p,
        )
        return self._parse_response(response)

    def run(self, query: str, ad: Dict[str, Any]) -> RelevanceOutput | None:
        messages = self.prepare_messages(query, ad)
        response = litellm.completion(
            model=self.model_configuration.model_name,
            base_url=self._base_url,
            api_key=self.key,
            messages=[message.model_dump() for message in messages],
            response_format=LLMRelevanceAnnotationOutput,
            max_tokens=self.model_configuration.max_tokens,
            temperature=self.model_configuration.temperature,
            top_p=self.model_configuration.top_p,
        )
        return self._parse_response(response)


class ImageRelevanceAgent(RelevanceAgent):

    def prepare_messages(self, query: str, ad: Ad) -> List[ChatMessage]:

        _ad_image_url = ad.images[0] if ad.images else None

        if _ad_image_url is None:
            _LOGGER.warning(f"Ad {ad.id} has no images! Using prompt without image.")
            return super().prepare_messages(query, ad)

        user_messages: List[Dict[str, Any]] = [
            {"type": "text", "text": f"Query: {query}"},
            {"type": "text", "text": f"Ad: {prepare_ad_prompt(ad)}"},
            {"type": "image_url", "image_url": {"url": _ad_image_url}},
        ]
        return [
            ChatMessage(role="system", content=self.system_prompt),
            ChatMessage(role="user", content=user_messages),
        ]
