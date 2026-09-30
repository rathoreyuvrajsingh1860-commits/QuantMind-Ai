from pydantic import BaseModel, ConfigDict, Field


class AIMessage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    content: str
    model: str
    provider: str


class ResearchAnalysis(BaseModel):
    model_config = ConfigDict(extra="forbid")

    executive_summary: str
    key_findings: list[str] = Field(default_factory=list)
    factual_observations: list[str] = Field(default_factory=list)
    interpretation: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    uncertainty: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)


class AIResearchResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    analysis: ResearchAnalysis
    provider: str
    model: str
