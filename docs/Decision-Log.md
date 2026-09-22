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

````md
# DEC-055 — AI Model Architecture

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** AI / ARCHITECTURE

## Decision

QuantMind will use a provider-agnostic AI architecture.

The application will communicate with AI models through an internal AI interface rather than directly coupling core product logic to a specific model provider.

Conceptually:

```text
QuantMind AI Interface
        ↓
AI Provider Adapter
        ↓
Model Provider
        ↓
Model
````

The AI layer must support:

* Primary model
* Compatible fallback model(s)
* Structured outputs
* Model-specific configuration
* Provider-specific adapters
* Timeout handling
* Retry handling
* Fallback handling
* Usage and cost tracking
* Model evaluation

## AI Responsibilities

The AI layer will be responsible for:

* Research reasoning
* Evidence synthesis
* Financial-context interpretation
* Fact vs interpretation separation
* Response composition
* Uncertainty communication
* Natural-language understanding where required

The AI layer must not become the source of raw financial truth.

It should operate on:

```text
Retrieved Data
+
Evidence
+
Quantitative Results
+
Temporal Context
+
Known Limitations
```

## Model Selection Principle

The initial production model will be selected through evaluation rather than brand preference.

Evaluation should consider:

* Financial research accuracy
* Evidence grounding
* Citation accuracy
* Structured-output reliability
* Reasoning quality
* Context handling
* Latency
* Cost
* Reliability
* Rate limits
* Data/privacy requirements

The exact primary model and fallback model will be recorded as a separate implementation decision after evaluation.

## Reasoning

QuantMind's long-term architecture should not depend on the continued availability, pricing, performance, or API design of one AI provider.

A provider abstraction allows the system to evolve as models improve.

It also allows QuantMind to select different models for different workloads when justified.

## Consequences

Core application modules must not directly depend on provider-specific SDKs.

Provider-specific code must remain inside AI provider adapters.

Prompts, structured output schemas, model configuration, and evaluation logic should be organized so that models can be compared without rewriting the research pipeline.

AI provider failures must follow the existing graceful-degradation strategy:

```text
Retry
↓
Compatible Fallback
↓
Partial Result
↓
Transparent Limitation
```

The system must never fabricate financial information because an AI provider failed.

## Affected Documents

* brain.md
* docs/PRD.md
* docs/MVP-Scope.md
* docs/TRD.md
* docs/Data-Sources.md
* docs/App-Flow.md
* docs/Decision-Log.md

## Notes

This decision intentionally does not select a specific AI provider or model.

The primary and fallback models will be selected after the QuantMind evaluation framework is established.

This decision can be superseded if future product requirements justify a different AI architecture.

```
```


---

# 56. Open Decisions

The following decisions remain unresolved and must be finalized before the corresponding implementation stage.

# DEC-057 — Initial Market Coverage

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** PRODUCT / DATA / SCOPE

## Decision

The QuantMind MVP will initially support:

### Geography

- India
- United States

### Primary Markets

- Indian equity markets
- United States equity markets

### Initial Asset Class

- Listed equities

The MVP will prioritize research and intelligence for publicly listed companies and their associated financial information.

## Initial Research Coverage

The MVP should prioritize the following information categories:

- Company/entity information
- Market and price data
- Financial statements
- Regulatory filings
- Earnings information
- Relevant financial news
- Macro-economic context
- Basic quantitative market analysis

The availability of each category depends on the selected data providers and applicable licensing.

## Historical Coverage

The initial target is:

> **At least 5 years of historical data where reliable and appropriately licensed data is available.**

Five years is a target rather than a guarantee of universal coverage.

The system must communicate when historical coverage is incomplete.

## Market Coverage Boundary

QuantMind must not imply that it supports all global markets during the MVP.

The initial product should clearly communicate its supported coverage.

Additional countries, exchanges, and asset classes may be added after MVP validation.

## Reasoning

India and the United States provide two important and complementary equity markets while keeping the initial product scope manageable.

Supporting both markets also allows QuantMind to validate its research architecture across different financial-data environments rather than optimizing the system for a single geography.

Limiting the initial asset class to listed equities keeps the MVP focused on the core Financial Research Intelligence workflow.

## Consequences

Data-provider evaluation must prioritize reliable coverage for:

- Indian equities
- US equities
- Company fundamentals
- Filings
- Earnings
- Market data
- Relevant news
- Macro information

Provider selection must also consider the historical depth required to support the five-year target.

Quantitative functions must correctly handle differences in:

- Currency
- Exchange
- Trading calendar
- Time zone
- Reporting conventions
- Corporate actions
- Financial periods

## Future Expansion

Future coverage may include:

- Additional countries
- Additional exchanges
- ETFs
- Bonds
- Commodities
- Currencies
- Derivatives
- Digital assets
- Other financial instruments

These remain outside the initial MVP unless explicitly added through a documented scope decision.

## Affected Documents

- brain.md
- docs/PRD.md
- docs/MVP-Scope.md
- docs/TRD.md
- docs/Data-Sources.md
- docs/App-Flow.md
- docs/Decision-Log.md

## Notes

This decision defines the initial MVP market boundary.

It does not finalize the specific data providers required to serve these markets.

Provider selection remains governed by DEC-056 — Financial Data Provider Architecture.

This decision can be superseded when MVP validation or product requirements justify broader market coverage.
---

# DEC-056 — Financial Data Provider Architecture

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** DATA / ARCHITECTURE / INFRASTRUCTURE

## Decision

QuantMind will use a provider-agnostic financial data architecture.

External financial-data providers must be accessed through internal provider interfaces and adapters.

Conceptually:

```text
QuantMind Data Interface
        ↓
Provider Adapter
        ↓
External Data Provider

The application must not make the core research system directly dependent on a single financial-data provider.

Data Categories

The provider architecture should support, where required:

Market data
Company/entity reference data
Financial statements
Regulatory filings
Earnings information
News
Macro-economic data
Corporate actions
Historical data
Reference data

The exact initial coverage will be determined separately.

Provider Selection Criteria

Each candidate provider should be evaluated based on:

Market coverage
Asset-class coverage
Geographic coverage
Historical depth
Data accuracy
Data freshness
API quality
Reliability
Rate limits
Commercial licensing
Storage rights
AI processing rights
Redistribution restrictions
Attribution requirements
Cost
Terms of use

No provider should be selected solely because it offers a convenient API.

Primary and Secondary Sources

QuantMind should maintain appropriate source hierarchy.

When relevant and available:

Primary Source
      ↓
Official / Regulatory Data
      ↓
Validated Secondary Source
      ↓
Derived / Calculated Data

Secondary providers may still be used when they provide useful structured data, historical coverage, aggregation, or context.

Provider Abstraction

The internal data layer should expose normalized interfaces rather than provider-specific formats.

Conceptually:

Research Service
      ↓
QuantMind Data Interface
      ↓
Provider Adapter
      ↓
Provider API

Provider-specific implementation details must remain inside the adapter layer.

Data Normalization

Retrieved data must be normalized into QuantMind's canonical internal representation where appropriate.

Normalization should preserve:

Entity identity
Currency
Unit
Scale
Reporting period
Publication date
Effective date
Retrieval timestamp
Source
Provider
Data status
Relevant corporate-action context

Normalization must not remove information required for provenance or temporal correctness.

Provenance

Important financial data must remain traceable to its source.

Conceptually:

Provider
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

Derived quantitative results should be traceable to their underlying inputs where practical.

Data Quality

Provider data must not automatically be treated as correct.

QuantMind should validate important data for:

Missing values
Invalid values
Unexpected units
Currency inconsistencies
Duplicate records
Date inconsistencies
Entity mismatches
Corporate-action effects
Unexpected revisions

Where credible sources disagree, the disagreement should remain identifiable rather than being silently hidden.

Licensing

Before production use, each provider must be evaluated for:

Commercial usage rights
Storage rights
Historical-data rights
AI processing rights
Redistribution rights
User-display rights
Attribution requirements
Retention requirements

Public accessibility must not be treated as equivalent to commercial permission.

Failure Handling

Provider failures should follow the existing graceful-degradation strategy:

Provider Request
      ↓
Retry
      ↓
Compatible Fallback Provider
      ↓
Partial Result
      ↓
Transparent Limitation

Fallback providers must only be used when their data is sufficiently compatible with the requested analysis.

The system must never silently substitute incompatible data.

Initial Provider Selection

The exact production providers remain a separate implementation decision.

Before implementation, the team must define:

Initial markets
Asset classes
Geographies
Required historical coverage
Freshness requirements
Required data categories
Provider candidates
Licensing constraints
Cost constraints

Provider selection should be documented after evaluation.

Reasoning

Financial data is one of QuantMind's foundational dependencies.

A provider abstraction prevents vendor lock-in and allows QuantMind to change or combine providers as coverage, pricing, licensing, reliability, and product requirements evolve.

It also allows different providers to be used for different categories of financial information when justified.

Consequences

Core research and quant modules must not directly depend on provider-specific SDKs or response formats.

Provider adapters should be independently testable.

The canonical data model must remain controlled by QuantMind rather than being dictated by an external provider.

Affected Documents
brain.md
docs/PRD.md
docs/MVP-Scope.md
docs/TRD.md
docs/Data-Sources.md
docs/App-Flow.md
docs/Decision-Log.md
Notes

This decision establishes the financial-data provider architecture but does not select the exact providers.

Specific provider selection requires separate evaluation of coverage, reliability, licensing, cost, and technical compatibility.

This decision can be superseded if actual MVP requirements justify a different data architecture.


### Commit message

```text
Accept provider-agnostic financial data architecture
---

# DEC-055 — AI Model Architecture

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** AI / ARCHITECTURE

## Decision

QuantMind will use a provider-agnostic AI architecture.

The application will communicate with AI models through an internal AI interface rather than directly coupling core product logic to a specific model provider.

Conceptually:

```text
QuantMind AI Interface
        ↓
AI Provider Adapter
        ↓
Model Provider
        ↓
Model

---

# DEC-054 — Authentication Provider

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** TECHNOLOGY / SECURITY / PRIVACY

## Decision

The QuantMind MVP will use:

> **Supabase Auth**

Supabase Auth will provide the initial authentication foundation while application authorization and product-specific access rules remain under QuantMind's backend/application architecture.

## Authentication Responsibilities

The authentication layer will support:

- User registration
- User sign-in
- Session management
- Secure authentication state
- User identity
- Password/account recovery where applicable
- Authentication state required by the research application

## Authorization

Authentication and authorization are separate concerns.

Supabase Auth establishes user identity.

QuantMind's application/backend layer must determine whether an authenticated user is authorized to perform a specific action or access specific application resources.

Authorization rules must not rely solely on frontend checks.

## Reasoning

Supabase Auth integrates naturally with the selected Supabase PostgreSQL infrastructure and reduces unnecessary authentication infrastructure during the MVP stage.

Using a managed authentication system also allows the team to focus implementation effort on QuantMind's core financial-intelligence workflow.

## Security Principles

The implementation must:

- Never store plaintext passwords
- Never expose authentication secrets to the frontend
- Validate authorization on the backend
- Protect authenticated resources
- Use secure session handling
- Avoid placing sensitive credentials in source control
- Follow appropriate security and privacy practices

## Consequences

Authentication-specific functionality should remain isolated from core research and intelligence modules.

The application should use internal abstractions where practical so authentication implementation can be changed later without rewriting the entire product.

Future enterprise requirements may introduce additional capabilities such as:

- SSO
- Organization accounts
- Role-based access control
- Team permissions
- Audit logging
- Enterprise identity providers

These are not required for the initial MVP unless explicitly added to scope.

## Affected Documents

- brain.md
- docs/PRD.md
- docs/MVP-Scope.md
- docs/TRD.md
- docs/App-Flow.md
- docs/Decision-Log.md

## Notes

This decision establishes Supabase Auth for the MVP.

It does not finalize the complete enterprise identity architecture.

Future authentication requirements may supersede this decision if product scale, enterprise requirements, security requirements, or regulatory requirements justify a change.

---

# DEC-053 — Database Technology

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** TECHNOLOGY / DATA / INFRASTRUCTURE

## Decision

The QuantMind MVP will use:

> **PostgreSQL**

The MVP database will be hosted through:

> **Supabase PostgreSQL**

PostgreSQL will serve as the primary relational database for QuantMind's structured application and financial-intelligence metadata.

## Database Responsibilities

The database will support data such as:

- Users and application accounts
- Research history
- Companies and entities
- Research requests
- Evidence metadata
- Source metadata
- Retrieved financial information
- Quantitative results
- Provider metadata
- AI analysis metadata
- Evaluation records
- Application configuration where appropriate

The database must preserve appropriate:

- Source information
- Timestamps
- Units
- Currency
- Periods
- Relationships
- Provenance
- Data status

## Reasoning

PostgreSQL provides a mature relational foundation for QuantMind's MVP and is well suited to structured financial data, relationships between entities and evidence, transactional application data, and deterministic quantitative workflows.

Supabase provides managed PostgreSQL infrastructure and can reduce operational complexity during the MVP stage.

The choice also leaves room for future expansion without requiring the MVP to adopt a specialized database architecture prematurely.

## Architecture Principle

The MVP will not introduce a dedicated graph database merely for the long-term Evidence Graph vision.

The minimum Evidence Graph structure will be represented using appropriate relational models and relationships.

A specialized graph database may be evaluated later if actual product requirements justify it.

## Consequences

The application must access database functionality through clear repository/data-access boundaries.

Business logic should not be tightly coupled to database-specific implementation details.

Database schemas and migrations must be version controlled.

Production credentials must never be committed to the repository.

Database design must preserve financial data provenance and temporal context where required.

## Affected Documents

- brain.md
- docs/PRD.md
- docs/MVP-Scope.md
- docs/TRD.md
- docs/Data-Sources.md
- docs/App-Flow.md
- docs/Decision-Log.md

## Notes

This decision establishes PostgreSQL as the MVP database technology.

It does not finalize:

- Authentication architecture
- AI provider
- Financial-data providers
- Deployment architecture
- Future graph-database requirements

Those remain separate decisions.

This decision can be superseded if actual MVP requirements provide a material reason to change the database architecture.
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
# DEC-052 — Backend Stack

**Status:** ACCEPTED
**Date:** 2026-09-22
**Category:** TECHNOLOGY / ARCHITECTURE

## Decision

The QuantMind MVP backend will use:

- Python
- FastAPI

The backend will be responsible for:

- API endpoints
- Authentication integration
- Research orchestration
- Intent handling
- Entity resolution
- Task planning
- Data retrieval
- Evidence retrieval
- Quantitative computation
- AI orchestration
- Verification
- Research history
- Provider integrations
- Error handling
- Observability

## Reasoning

Python is well suited to QuantMind's financial intelligence workload because the product requires quantitative computation, data processing, AI/ML integration, financial research workflows, and statistical analysis.

FastAPI provides a lightweight API foundation with strong support for typed request/response contracts and asynchronous operations where appropriate.

The backend should remain a modular monolith rather than being split into premature microservices.

## Consequences

The backend will expose defined API/application interfaces to the Next.js frontend.

Core financial logic must remain inside backend/domain modules rather than the frontend.

Quantitative calculations must remain deterministic and independently testable.

External financial-data and AI providers must be accessed through internal abstraction layers.

The backend should remain modular enough that individual components can later be extracted if actual scale or ownership requirements justify it.

## Affected Documents

- brain.md
- docs/PRD.md
- docs/MVP-Scope.md
- docs/TRD.md
- docs/App-Flow.md
- docs/Data-Sources.md
- docs/Decision-Log.md

## Notes

This decision does not lock QuantMind to a specific AI provider, financial-data provider, database, or deployment platform.

Those decisions remain separate architectural decisions.

This decision can be superseded if MVP validation or technical requirements provide a material reason to change the backend architecture.

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

