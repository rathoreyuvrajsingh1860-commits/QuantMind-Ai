import json
from typing import Any

from src.ai.base import AIProvider, AIProviderError
from src.ai.models import AIResearchResult, ResearchAnalysis
from src.research.models import ResearchResult


SYSTEM_PROMPT = """
You are QuantMind AI's financial research intelligence engine.

Your job is to analyze the supplied structured research data and produce
careful, evidence-grounded financial research.

NON-NEGOTIABLE RULES:

1. Use ONLY the information supplied in the research context.
2. Never invent financial facts, news, filings, prices, events, or sources.
3. Deterministic numerical metrics supplied by the system are authoritative.
4. Clearly separate factual observations from interpretation.
5. Do not present interpretation as fact.
6. Do not provide personalized investment advice.
7. Do not issue buy, sell, hold, or target-price recommendations.
8. Explicitly acknowledge missing information.
9. If evidence is insufficient, say so.
10. Preserve uncertainty instead of manufacturing confidence.
11. Do not imply that historical price performance predicts future returns.
12. Treat the source and retrieval timestamps as part of the evidence context.

Return ONLY valid JSON matching this structure:

{
  "executive_summary": "string",
  "key_findings": ["string"],
  "factual_observations": ["string"],
  "interpretation": ["string"],
  "risks": ["string"],
  "uncertainty": ["string"],
  "limitations": ["string"]
}
""".strip()


class AIResearchService:
    def __init__(self, provider: AIProvider) -> None:
        self.provider = provider

    def analyze(self, research: ResearchResult) -> AIResearchResult:
        context = self._build_context(research)

        message = self.provider.generate(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=context,
        )

        analysis = self._parse_analysis(message.content)

        return AIResearchResult(
            analysis=analysis,
            provider=message.provider,
            model=message.model,
        )

    @staticmethod
    def _build_context(research: ResearchResult) -> str:
        payload = research.model_dump(mode="json")

        return (
            "Analyze the following QuantMind research context.\n\n"
            "IMPORTANT: This is the complete available research context. "
            "Do not assume information that is not present.\n\n"
            f"{json.dumps(payload, indent=2, default=str)}"
        )

    @staticmethod
    def _parse_analysis(content: str) -> ResearchAnalysis:
        cleaned = content.strip()

        if cleaned.startswith("```"):
            lines = cleaned.splitlines()

            if lines and lines[0].startswith("```"):
                lines = lines[1:]

            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            cleaned = "\n".join(lines).strip()

        try:
            payload: Any = json.loads(cleaned)
        except json.JSONDecodeError as exc:
            raise AIProviderError(
                "AI provider returned non-JSON research analysis"
            ) from exc

        if not isinstance(payload, dict):
            raise AIProviderError(
                "AI provider returned an invalid research analysis object"
            )

        try:
            return ResearchAnalysis.model_validate(payload)
        except Exception as exc:
            raise AIProviderError(
                "AI provider returned an invalid research analysis schema"
            ) from exc
