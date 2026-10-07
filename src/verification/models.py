from pydantic import BaseModel, ConfigDict


class VerificationIssue(BaseModel):
    model_config = ConfigDict(extra="forbid")

    field: str
    message: str


class VerificationResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    passed: bool
    issues: list[VerificationIssue]
