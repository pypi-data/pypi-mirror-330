from pydantic import BaseModel


class Query(BaseModel):
    id: int
    text: str
    filter_params: list[tuple[str, str]] | None = None

    def get_query_w_filters(self) -> str:
        if self.filter_params is not None:
            out = self.text
            for key, value in self.filter_params:
                out += f" {key}:{value}"
        else:
            out = self.text

        return out


class Ad(BaseModel):
    """
    Ad schema.
    The following arguments are required:
    - id: int
    - title: str
    Other arguments are allowed.
    """

    id: int
    title: str
    description: str
    images: list[str]
    price: float | None = None
    state: str | None = None
    params: str | None = None

    class Config:
        arbitrary_types_allowed = True
        extra = "allow"


class RelevanceJudgement(BaseModel):
    ad_id: int
    score: int
    reasoning: str | None = None
