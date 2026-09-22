# QuantMind AI — Decision Log

> **Status:** Phase 0 — Foundation / Pre-MVP
> **Document Type:** Architectural + Product Decision Log
> **Version:** 1.0
> **Last Updated:** 2026-09-22
> **Product:** QuantMind AI
> **Tagline:** Think Beyond the Market.

---

# 1. Purpose

This document records important decisions made during the design and development of QuantMind AI.

Its purpose is to:

* Preserve architectural context
* Prevent repeated debates
* Prevent accidental reversal of decisions
* Explain why important decisions were made
* Track approved scope changes
* Record unresolved decisions
* Maintain consistency between product and engineering

This document is not a general notes file.

Only meaningful product, technical, data, design, security, regulatory, and architectural decisions should be recorded.

---

# 2. Decision Authority

Decisions must be interpreted alongside:

```text
brain.md
docs/PRD.md
docs/MVP-Scope.md
docs/TRD.md
docs/Data-Sources.md
docs/UI-UX-Design-Brief.md
docs/App-Flow.md
```

The source-of-truth hierarchy is:

```text
brain.md
    ↓
PRD.md
    ↓
MVP-Scope.md
    ↓
Technical / Data / UX / Flow Documents
    ↓
Implementation
```

If a lower-level decision conflicts with a higher-level document, the conflict must be resolved explicitly.

---

# 3. Decision Statuses

Each decision should have one of the following statuses:

```text
PROPOSED
UNDER REVIEW
ACCEPTED
IMPLEMENTED
SUPERSEDED
REJECTED
DEFERRED
```

---

# 4. Decision Format

New decisions should use:

```text
## DEC-XXX — Decision Title

Status:
Date:
Category:
Decision:

Context:

Reasoning:

Alternatives Considered:

Consequences:

Affected Documents:

Notes:
```

---

# 5. Decision Categories

Use one of:

```text
PRODUCT
SCOPE
ARCHITECTURE
TECHNOLOGY
DATA
AI
QUANT
UX
SECURITY
PRIVACY
REGULATORY
BUSINESS
INFRASTRUCTURE
```

---

# 6. DEC-001 — QuantMind Product Identity

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** PRODUCT

## Decision

QuantMind AI will be positioned as an:

> **AI-powered Financial Intelligence Platform**

The long-term product is intended to become financial intelligence infrastructure rather than a generic AI chatbot or simple stock-prediction application.

## Context

The product requires a clear identity that can support both professional financial research and future personal financial intelligence.

## Reasoning

The core product differentiator is the combination of:

```text
Financial Data
+
Evidence
+
Quantitative Analysis
+
AI Reasoning
+
Explainability
```

## Consequences

All major product decisions should reinforce the financial intelligence positioning.

---

# 7. DEC-002 — Product Tagline

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** PRODUCT / BRAND

## Decision

The official working tagline is:

> **Think Beyond the Market.**

## Consequences

The tagline may be used across:

* Website
* Product
* Brand materials
* Documentation

unless later superseded by an explicit brand decision.

---

# 8. DEC-003 — Evidence Before Trust

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** PRODUCT / AI

## Decision

QuantMind will follow:

> **Evidence Before Trust.**

Important financial intelligence should be traceable to supporting evidence wherever possible.

## Context

AI-generated financial analysis can otherwise become difficult to verify.

## Consequences

The product must prioritize:

```text
Source
↓
Evidence
↓
Calculation
↓
Interpretation
```

rather than presenting unsupported AI conclusions.

---

# 9. DEC-004 — MVP Focus

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** SCOPE

## Decision

The MVP will focus on:

> **Financial Research Intelligence**

The MVP will not attempt to implement the entire QuantMind vision.

## Core MVP Loop

```text
Financial Data
→ Research
→ Evidence
→ AI Analysis
→ Explainable Intelligence
```

## Consequences

Capabilities such as advanced trading, personal finance, strategy marketplaces, and enterprise automation remain deferred.

---

# 10. DEC-005 — Three-Horizon Scope Model

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** SCOPE

## Decision

QuantMind documentation will use:

```text
NOW
NEXT
VISION
```

### NOW

Current MVP requirements.

### NEXT

Capabilities expected after MVP validation.

### VISION

Long-term platform capabilities.

## Consequences

Future ideas must not automatically become MVP requirements.

---

# 11. DEC-006 — Documentation Before Major Implementation

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** PROCESS / ARCHITECTURE

## Decision

Major implementation begins only after the foundational product and architecture documentation has been established.

Required foundational documents:

```text
brain.md
PRD.md
MVP-Scope.md
TRD.md
Data-Sources.md
UI-UX-Design-Brief.md
App-Flow.md
Decision-Log.md
```

## Reasoning

The project is complex enough that implementation before architectural agreement would create unnecessary rework and scope drift.

---

# 12. DEC-007 — Modular Monolith for MVP

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** ARCHITECTURE

## Decision

The initial QuantMind implementation should use a:

> **Modular monolith with clear internal service boundaries.**

## Context

The product is pre-MVP and does not yet require a distributed microservice architecture.

## Reasoning

A modular monolith provides:

* Faster development
* Lower infrastructure complexity
* Easier debugging
* Clear boundaries
* Future extraction paths

## Consequences

Internal modules should remain well separated even though they may initially run within the same application.

---

# 13. DEC-008 — Intelligence Architecture

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** ARCHITECTURE / AI

## Decision

QuantMind must not be architected as:

```text
User → LLM → Answer
```

The core architecture is:

```text
User
↓
Intent Understanding
↓
Task Planning
↓
Data Retrieval
↓
Evidence Retrieval
↓
Quantitative Computation
↓
AI Reasoning
↓
Verification
↓
Explainable Response
```

## Consequences

AI reasoning must operate within a structured research pipeline.

---

# 14. DEC-009 — Deterministic Quant Engine

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** QUANT / ARCHITECTURE

## Decision

Important financial calculations must be performed by deterministic computation rather than relying on LLM arithmetic.

## Examples

* Percentage changes
* Growth rates
* Returns
* Volatility
* Historical comparisons
* Statistical calculations

## Consequences

The Quant Engine must be independently testable.

---

# 15. DEC-010 — AI Does Not Become the Source of Financial Truth

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** AI

## Decision

The AI model should synthesize and interpret retrieved information rather than act as the primary source of financial facts.

## Consequences

The AI should receive:

```text
Retrieved Data
+
Evidence
+
Quantitative Results
+
Temporal Context
+
Limitations
```

before generating important financial analysis.

---

# 16. DEC-011 — Evidence Graph MVP Boundary

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** ARCHITECTURE / DATA

## Decision

The full Evidence Graph is a long-term capability.

The MVP will implement only the minimum evidence/provenance structure required to support the concept.

## Core Relationship

```text
CLAIM
↓
SOURCE
↓
EVIDENCE
↓
TIMESTAMP
↓
CALCULATION / METHODOLOGY
↓
CONFIDENCE / LIMITATION
```

## Consequences

A dedicated graph database is not required for MVP.

---

# 17. DEC-012 — Provider Abstraction

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** DATA / ARCHITECTURE

## Decision

External data providers must be accessed through internal provider interfaces.

Conceptually:

```text
QuantMind Data Interface
        ↓
Provider Adapter
        ↓
External Provider
```

## Reasoning

This prevents the application from becoming tightly coupled to a single provider.

---

# 18. DEC-013 — Data Provenance

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** DATA

## Decision

Important financial data should preserve provenance.

Conceptually:

```text
Source
↓
Raw Data
↓
Validation
↓
Canonical Data
↓
Evidence
↓
Calculation
↓
Analysis
```

## Consequences

Important derived results should be traceable back to their inputs where practical.

---

# 19. DEC-014 — Public Availability ≠ Commercial Permission

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** DATA / REGULATORY

## Decision

QuantMind will not assume that publicly accessible financial information is automatically licensed for commercial use.

## Consequences

Production data providers must be evaluated for:

* Commercial use
* Storage rights
* AI processing rights
* Redistribution rights
* Attribution requirements
* Rate limits
* Retention restrictions

---

# 20. DEC-015 — No Unrestricted Scraping by Default

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** DATA / LEGAL

## Decision

Unrestricted scraping will not be treated as the default data acquisition strategy.

## Consequences

Any scraping-based source must undergo separate evaluation of:

* Terms
* Copyright considerations
* Commercial usage
* Technical stability
* Rate limits
* Redistribution rights

---

# 21. DEC-016 — Temporal Correctness

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** QUANT / DATA / AI

## Decision

QuantMind must preserve temporal correctness.

Historical analysis must not use information that would not have been available at the relevant historical point.

## Consequences

Data should preserve appropriate:

* Publication date
* Effective date
* Reporting period
* Retrieval date
* Update date

---

# 22. DEC-017 — No Fabricated Missing Data

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** AI / DATA

## Decision

If required information is unavailable, QuantMind must not fabricate it.

The system should instead:

```text
Identify Missing Data
↓
Determine Whether Analysis Can Continue
↓
Return Partial Result if Reliable
↓
Explain Limitation
```

---

# 23. DEC-018 — Contradictory Sources Must Remain Visible

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** DATA / AI

## Decision

When credible sources disagree, QuantMind should not silently select one without considering the reason for the disagreement.

## Consequences

The system should evaluate:

* Date
* Period
* Definition
* Revision status
* Methodology
* Source authority

If unresolved, the disagreement should be communicated.

---

# 24. DEC-019 — AI Uncertainty Handling

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** AI

## Decision

QuantMind must explicitly communicate uncertainty when evidence is incomplete, conflicting, stale, or insufficient.

## Consequences

The product should avoid artificial certainty.

The UI should not expose arbitrary AI confidence percentages without a validated methodology.

---

# 25. DEC-020 — Fact vs Interpretation

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** AI / UX

## Decision

The system should distinguish:

```text
FACT
DERIVED RESULT
INTERPRETATION
UNCERTAINTY
```

## Consequences

The user should be able to understand what is directly supported versus what is analytical interpretation.

---

# 26. DEC-021 — MVP Does Not Execute Trades

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** SCOPE / REGULATORY

## Decision

The MVP will not include:

* Automated trading
* Brokerage execution
* Autonomous order placement
* Trading bots

## Reasoning

The MVP objective is financial research intelligence, not execution infrastructure.

---

# 27. DEC-022 — Personal Finance Is Future Scope

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** PRODUCT / SCOPE

## Decision

Personal Finance Intelligence is part of the long-term QuantMind vision but is not part of the initial MVP.

Future capabilities may include:

```text
Income Intelligence
Expense Intelligence
Goal Planning
Investment Planning
Payday Intelligence
Personal Financial Copilot
```

## Consequences

These capabilities must not expand the initial MVP scope without an explicit decision.

---

# 28. DEC-023 — No Full Backtesting in MVP

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** QUANT / SCOPE

## Decision

The MVP will not include a full production backtesting engine.

Basic quantitative research is in scope.

Advanced strategy construction and backtesting are deferred.

---

# 29. DEC-024 — No Full Strategy Builder in MVP

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** PRODUCT / SCOPE

## Decision

Natural-language strategy creation and advanced strategy validation are future capabilities.

The MVP may provide quantitative context but will not implement the full strategy-building platform.

---

# 30. DEC-025 — Research-First User Experience

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** UX

## Decision

The primary MVP interaction is:

> **Ask a financial research question.**

The product should optimize for research rather than dashboards, trading, or social interaction.

---

# 31. DEC-026 — Quiet Intelligence Design

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** UX / BRAND

## Decision

The UI should follow a:

> **Quiet Intelligence**

design philosophy.

## Characteristics

* Minimal
* Premium
* Information-dense
* Calm
* Evidence-focused
* Professional

## Avoid

* Neon AI aesthetics
* Excessive gradients
* Crypto-style visuals
* Excessive cards
* Decorative data
* Fake social proof
* Excessive animation

---

# 32. DEC-027 — Evidence UI Is a Core Feature

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** UX / PRODUCT

## Decision

Evidence and sources must be visible parts of the research experience.

They should not be hidden behind a secondary interface.

## Consequences

Users should be able to move from:

```text
Insight
↓
Evidence
↓
Source
```

without leaving the research context.

---

# 33. DEC-028 — No Artificial AI Confidence

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** AI / UX

## Decision

QuantMind will not display arbitrary AI confidence percentages such as:

```text
97% confidence
```

unless a defensible and validated methodology exists.

## Reasoning

A visually precise confidence number can create false certainty.

---

# 34. DEC-029 — Modular AI Provider Architecture

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** AI / ARCHITECTURE

## Decision

The application should not become permanently dependent on one AI provider.

An internal AI interface should allow model/provider replacement.

## Consequences

Model selection can evolve based on:

* Accuracy
* Cost
* Latency
* Context capability
* Reliability
* Structured-output support

---

# 35. DEC-030 — Graceful Degradation

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** RELIABILITY

## Decision

External provider failures must result in:

```text
Retry
↓
Fallback where compatible
↓
Partial Result
↓
Transparent Limitation
```

rather than fabricated information.

---

# 36. DEC-031 — Modular Repository Structure

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** ENGINEERING

## Decision

The codebase will use clear modules for:

```text
api
auth
research
entities
retrieval
evidence
quant
ai
verification
data
storage
config
observability
shared
```

The exact framework and language remain an implementation decision unless separately finalized.

---

# 37. DEC-032 — Evaluation Infrastructure Is a Moat

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** AI / PRODUCT

## Decision

QuantMind should build evaluation infrastructure early.

Evaluation should eventually measure:

```text
Factual Accuracy
Evidence Grounding
Citation Accuracy
Quantitative Accuracy
Temporal Correctness
Hallucination
Uncertainty Handling
```

## Reasoning

A financial AI product requires measurable reliability rather than subjective demo quality.

---

# 38. DEC-033 — Financial Arithmetic Must Be Testable

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** QUANT

## Decision

Every production quantitative function must be independently testable.

Tests should cover:

* Normal inputs
* Missing inputs
* Invalid inputs
* Boundary conditions
* Precision
* Units
* Large values
* Applicable negative values

---

# 39. DEC-034 — Financial Data Must Preserve Units and Context

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** DATA / QUANT

## Decision

Financial values must preserve relevant:

* Currency
* Unit
* Scale
* Period
* Timestamp
* Source

A number without context must not be treated as a complete financial fact.

---

# 40. DEC-035 — Do Not Build Microservices Prematurely

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** ARCHITECTURE

## Decision

QuantMind will not adopt a distributed microservice architecture merely for architectural appearance.

The MVP should use modular boundaries within a simpler deployment architecture.

## Consequences

Future services may be extracted when actual scale or ownership requirements justify them.

---

# 41. DEC-036 — Scope Freeze During MVP

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** SCOPE

## Decision

Once MVP implementation begins, scope is considered frozen unless a change is explicitly approved and documented.

## Required Process

```text
Feature Request
↓
Scope Evaluation
↓
Impact Analysis
↓
Decision
↓
Update Documentation
↓
Implementation
```

No silent scope expansion.

---

# 42. DEC-037 — AI Coding Agent Must Read Documentation First

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** ENGINEERING

## Decision

Any AI coding agent working on QuantMind must first understand:

```text
brain.md
PRD.md
MVP-Scope.md
```

and consult relevant technical documents before modifying architecture.

## Consequences

Agents must not invent competing architecture or silently rewrite established decisions.

---

# 43. DEC-038 — Documentation Is Part of the Architecture

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** PROCESS

## Decision

Documentation is not treated as optional project administration.

The documentation itself defines architectural intent and scope.

## Golden Rule

> **Build what is documented. Document what is decided. Validate what is assumed. Never silently change the architecture.**

---

# 44. DEC-039 — MVP Data Coverage Must Be Explicit

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** DATA / SCOPE

## Decision

QuantMind will not claim universal financial-market coverage by default.

Before production implementation, the team must explicitly define:

```text
Markets
Asset Classes
Geographies
Historical Coverage
Data Providers
Freshness Requirements
```

---

# 45. DEC-040 — Primary Sources Receive Strong Evidentiary Preference

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** DATA / RESEARCH

## Decision

When relevant and available, primary sources should generally receive stronger evidentiary preference for factual claims.

Examples include:

* Regulatory filings
* Official company disclosures
* Government datasets
* Central-bank publications
* Official financial statements

Secondary sources remain valuable for context and interpretation.

---

# 46. DEC-041 — Research Is Not Automatically Investment Advice

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** REGULATORY / PRODUCT

## Decision

The MVP is designed around financial research and intelligence.

Capabilities that may constitute regulated personalized investment advice, portfolio management, or execution require separate legal and compliance review before implementation.

## Consequences

A disclaimer alone must not be treated as a substitute for evaluating the actual product behavior and applicable regulations.

---

# 47. DEC-042 — No Guaranteed Financial Outcomes

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** PRODUCT / REGULATORY

## Decision

QuantMind must not market or represent:

* Guaranteed returns
* Guaranteed predictions
* Guaranteed trading outcomes
* Certainty about future market movements

Research should communicate evidence and uncertainty.

---

# 48. DEC-043 — No Fake Product Proof

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** BRAND / UX

## Decision

The website and product must not use fabricated:

* Testimonials
* Customer logos
* Performance results
* Partnerships
* Usage statistics
* Investor claims

If proof does not exist, the product should not imply that it does.

---

# 49. DEC-044 — Depth Before Breadth

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** PRODUCT / ENGINEERING

## Decision

The MVP should prioritize depth and reliability of the core research workflow over the number of available features.

## Principle

```text
One reliable intelligence loop
>
Many shallow features
```

---

# 50. DEC-045 — Research Quality Before Automation

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** PRODUCT / AI

## Decision

QuantMind will first establish reliable research intelligence before introducing increasingly autonomous financial agents.

## Progression

```text
Research
↓
Reliable Intelligence
↓
Quantitative Research
↓
Workflow Automation
↓
Agents
↓
Advanced Autonomy
```

Automation must not precede reliability.

---

# 51. DEC-046 — Personal Financial Intelligence Requires Separate Architecture

**Status:** DEFERRED
**Date:** 2026-09-22
**Category:** PRODUCT / DATA / REGULATORY

## Decision

Future personal finance capabilities will require separate architecture for:

* User financial data
* Consent
* Privacy
* Security
* Financial accounts
* Goals
* Investment information
* Regulatory requirements

## Consequence

Personal financial data must not be casually added to the MVP architecture.

---

# 52. DEC-047 — Evidence Graph Is a Long-Term Moat

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** PRODUCT / ARCHITECTURE

## Decision

The Evidence Graph is considered a foundational long-term QuantMind capability.

The MVP should establish its provenance foundations without attempting to build the entire graph.

## Long-Term Concept

```text
Entity
↓
Data
↓
Evidence
↓
Claim
↓
Calculation
↓
Interpretation
↓
Relationship
```

---

# 53. DEC-048 — QuantMind Is Not a Generic Chatbot

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** PRODUCT

## Decision

QuantMind should not be designed as a generic conversational AI interface with financial prompts layered on top.

The product's intelligence must be grounded in:

```text
Financial Data
+
Retrieval
+
Evidence
+
Quantitative Computation
+
Domain Reasoning
```

---

# 54. DEC-049 — Research Output Must Be Explainable

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** PRODUCT / AI

## Decision

Important outputs should provide enough context for users to understand how the conclusion was reached.

This does not require exposing private model reasoning.

It requires exposing:

* Relevant evidence
* Calculations
* Sources
* Assumptions
* Limitations

---

# 55. DEC-050 — No Silent Architectural Overrides

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** GOVERNANCE

## Decision

No developer, AI agent, or implementation process may silently override documented architecture.

If a conflict exists:

```text
Identify Conflict
↓
Explain Conflict
↓
Propose Change
↓
Approve Decision
↓
Update Documentation
↓
Implement
```

---

# 56. Open Decisions

The following decisions remain unresolved and must be finalized before the corresponding implementation stage.

## OPEN-001 — Initial Market Coverage

**Status:** OPEN

Need to determine:

* Initial countries
* Exchanges
* Markets
* Asset classes

---

## OPEN-002 — Initial Data Providers

**Status:** OPEN

Need to evaluate:

* Market-data provider
* News provider
* Filing provider
* Financial-statement provider
* Macro provider

Selection must consider coverage, reliability, licensing, cost, and API quality.

---

## OPEN-003 — AI Model Provider

**Status:** OPEN

Need to determine:

* Primary model
* Fallback model
* Structured-output approach
* Cost controls
* Context requirements
* Evaluation methodology

---

## OPEN-004 — Authentication Provider

**Status:** OPEN

Need to determine:

* Authentication method
* Session architecture
* User persistence
* Authorization model

---

## OPEN-005 — Database Technology

**Status:** OPEN

Need to finalize the production database and deployment configuration.

---

# DEC-051 — Frontend Stack

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** TECHNOLOGY / UX

## Decision

The QuantMind MVP frontend will use:

- Next.js
- TypeScript
- Tailwind CSS

The frontend will be responsible for:

- Research interface
- Company/entity research pages
- Evidence and source presentation
- Quantitative result visualization
- Research history
- Comparison workflows
- Loading and error states
- Responsive user experience

## Reasoning

Next.js provides a strong foundation for the research-first web application while TypeScript improves maintainability and type safety.

Tailwind CSS supports the project's Quiet Intelligence design system without introducing unnecessary UI complexity.

The frontend should remain focused on presenting intelligence and evidence rather than implementing core financial computation or business logic.

## Consequences

The frontend communicates with the backend through defined application/API interfaces.

Financial calculations, data retrieval, evidence processing, and AI orchestration must remain outside the presentation layer.

The exact component library remains an implementation detail and should not be introduced as an architectural dependency without justification.

## Affected Documents

- brain.md
- docs/PRD.md
- docs/MVP-Scope.md
- docs/TRD.md
- docs/UI-UX-Design-Brief.md
- docs/App-Flow.md

## Notes

This decision can be superseded if MVP validation or technical requirements provide a material reason to change the frontend architecture.

---

## OPEN-007 — Backend Stack

**Status:** OPEN

Need to finalize the backend framework and language.

---

## OPEN-008 — Evaluation Dataset

**Status:** OPEN

Need to establish:

* Research questions
* Ground-truth answers
* Expected evidence
* Quantitative expected results
* Temporal test cases
* Failure cases

---

## OPEN-009 — MVP Accuracy Thresholds

**Status:** OPEN

Need to define measurable acceptance thresholds for:

* Factual accuracy
* Citation accuracy
* Quantitative accuracy
* Evidence grounding
* Temporal correctness
* Hallucination

---

## OPEN-010 — Data Retention Policy

**Status:** OPEN

Need to define retention based on:

* Provider terms
* Product requirements
* Privacy requirements
* Storage cost
* Research reproducibility

---

# 57. Superseding Decisions

When a decision changes, do not delete the original record.

Instead:

```text
Original Decision
↓
New Decision
↓
Mark Original as SUPERSEDED
↓
Reference New Decision
```

This preserves architectural history.

---

# 58. Decision Review Rules

A decision should be reconsidered when:

* New evidence materially changes assumptions.
* A provider becomes unavailable.
* A technical limitation is discovered.
* Regulatory requirements change.
* MVP validation contradicts the assumption.
* Product scope changes.
* Scaling requirements materially change.

Decisions should not be revisited merely because a different technology appears interesting.

---

# 59. Decision Quality Criteria

Before accepting a major decision, ask:

```text
Does it support the product?
Does it support the MVP?
Does it preserve correctness?
Does it preserve evidence?
Does it create unnecessary complexity?
Is it reversible?
Does it introduce regulatory risk?
Does it introduce vendor lock-in?
Does it block future expansion?
Can it be tested?
```

---

# 60. Final Architectural Decisions Summary

Current foundational decisions:

| Area                 | Decision                                                            |
| -------------------- | ------------------------------------------------------------------- |
| Product              | AI-powered Financial Intelligence Platform                          |
| Tagline              | Think Beyond the Market.                                            |
| MVP                  | Financial Research Intelligence                                     |
| Core Principle       | Evidence Before Trust                                               |
| Core Loop            | Data → Research → Evidence → AI Analysis → Explainable Intelligence |
| Architecture         | Modular monolith                                                    |
| AI                   | Structured research pipeline, not direct chatbot                    |
| Quant                | Deterministic calculation engine                                    |
| Evidence             | Traceable provenance                                                |
| Data                 | Provider abstraction + validation                                   |
| Historical Analysis  | Temporal correctness required                                       |
| Missing Data         | Never fabricate                                                     |
| Conflicts            | Preserve and explain                                                |
| Trading              | Out of MVP                                                          |
| Personal Finance     | Future phase                                                        |
| Advanced Backtesting | Future phase                                                        |
| Full Evidence Graph  | Future phase                                                        |
| UI                   | Quiet Intelligence                                                  |
| Scope                | Frozen during MVP unless explicitly changed                         |
| Documentation        | Source of truth for implementation                                  |

---

# 61. Final Rule

> **A decision is not complete until its reasoning and consequences are documented.**

> **A documented decision must not be silently reversed.**

> **If the architecture needs to change, change the documentation first.**

> **QuantMind AI should evolve deliberately, not accidentally.**

