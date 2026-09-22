# QuantMind AI — MVP Scope

> **Status:** Phase 0 — Foundation / Pre-MVP
> **Document Type:** MVP Scope Definition / Scope Boundary
> **Version:** 1.0
> **Last Updated:** 2026-09-22
> **Product:** QuantMind AI
> **Tagline:** Think Beyond the Market.

---

# 1. Purpose

This document defines the exact boundary of the QuantMind AI MVP.

Its purpose is to prevent scope expansion, premature implementation, and accidental movement of long-term platform capabilities into the first product release.

The MVP must prove one core product loop:

```text
Financial Data
      ↓
Research
      ↓
Evidence
      ↓
AI Analysis
      ↓
Explainable Intelligence
```

The MVP is **not** intended to build the complete QuantMind AI platform.

It is the first validated implementation of the QuantMind intelligence architecture.

---

# 2. Scope Authority

The MVP scope must be interpreted together with:

1. `brain.md`
2. `docs/PRD.md`
3. `docs/MVP-Scope.md`
4. `docs/TRD.md`
5. `docs/Data-Sources.md`
6. `docs/UI-UX-Design-Brief.md`
7. `docs/App-Flow.md`
8. `docs/Decision-Log.md`

The hierarchy is:

```text
brain.md
    ↓
PRD.md
    ↓
MVP-Scope.md
    ↓
TRD.md / Data-Sources.md / UI-UX-Design-Brief.md / App-Flow.md
    ↓
Implementation
```

If implementation conflicts with this scope, implementation must not silently redefine the scope.

---

# 3. Current Product Phase

```text
Phase: 0 — Foundation / Pre-MVP
Development Status: Documentation First
MVP Status: Not Yet Implemented
```

The project must complete its foundational documentation before major implementation begins.

The immediate objective is to define the MVP precisely enough that engineering can begin without repeatedly redefining the product.

---

# 4. MVP Definition

The QuantMind MVP is:

> **An AI-powered financial research intelligence system that retrieves relevant financial information, connects supporting evidence, performs validated quantitative analysis, and produces explainable research intelligence with transparent sourcing and uncertainty handling.**

The MVP focuses on **financial research intelligence**.

It does not attempt to become a complete financial operating system in the first release.

---

# 5. MVP Core Loop

The MVP must implement the following core loop:

```text
USER QUESTION
     ↓
INTENT UNDERSTANDING
     ↓
RELEVANT FINANCIAL DATA
     ↓
EVIDENCE RETRIEVAL
     ↓
QUANTITATIVE ANALYSIS
     ↓
AI REASONING
     ↓
VERIFICATION
     ↓
EXPLAINABLE RESPONSE
     ↓
SOURCES / EVIDENCE
```

Every major MVP feature should strengthen this loop.

Features that do not contribute meaningfully to this loop should be deferred unless explicitly approved.

---

# 6. NOW / NEXT / VISION

## NOW — MVP

Build the minimum system capable of delivering:

* Financial research
* Relevant financial data retrieval
* News and event context where supported
* Filing/document intelligence where supported
* Evidence retrieval
* Source attribution
* Explainable AI analysis
* Fact vs interpretation separation
* Basic quantitative analysis
* Temporal awareness
* Uncertainty handling
* Missing-data handling
* Contradictory-source handling
* Research history where required
* Company/entity research
* Basic comparison workflows
* Trust/evidence UI
* Reliable research responses

---

## NEXT — Post-MVP

Do not include these in the initial MVP unless specifically approved:

* Advanced quant research
* Full strategy builder
* Advanced backtesting
* Portfolio intelligence
* Paper trading
* Personal finance intelligence
* Goal planning
* Payday intelligence
* Personal financial copilot
* Advanced agent orchestration
* Expanded knowledge graph
* API platform
* Quant marketplace
* Advanced institutional workflows

---

## VISION — Long-Term QuantMind Platform

The long-term platform may include:

* Financial intelligence infrastructure
* Professional quantitative research
* AI research agents
* Portfolio intelligence
* Personal financial intelligence
* Goal intelligence
* Automated financial workflows
* Agent ecosystem
* Knowledge graph
* Evidence graph
* Financial APIs
* Enterprise intelligence
* Institutional workflows
* Marketplace ecosystem

These capabilities are part of the product vision but are **not MVP scope**.

---

# 7. MVP IN SCOPE

## 7.1 Financial Data Retrieval

The MVP must have a reliable mechanism for retrieving relevant financial information.

It should support, where available and properly licensed:

* Company information
* Market information
* Financial metrics
* Historical data
* Relevant events
* Financial documents
* News
* Earnings-related information
* Macro information where directly relevant

Data providers must be explicitly documented in:

```text
docs/Data-Sources.md
```

No undocumented or unauthorized data source should be treated as production infrastructure.

---

# 8. Evidence Retrieval

The system must retrieve evidence supporting important claims.

Evidence should preserve, where available:

```text
Source
↓
Document / Article / Dataset
↓
Relevant Evidence
↓
Timestamp / Date
↓
Claim
```

The MVP does not need a fully distributed knowledge graph.

However, its architecture must be compatible with the future Evidence Graph.

---

# 9. Source Attribution

Important financial claims should be traceable to their sources.

The user should be able to understand:

* Where information came from
* When the information was published or measured
* What evidence supports the claim
* Whether the information is directly sourced or derived
* What limitations apply

The system must not create fictional citations.

---

# 10. Evidence Graph — MVP Boundary

The full Evidence Graph is a long-term capability.

The MVP should implement only the minimum structure required to establish the foundation.

Conceptually:

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

The MVP does not require:

* Full graph database infrastructure
* Complete entity relationship graph
* Global financial knowledge graph
* Automated graph discovery
* Marketplace access to the graph

The architecture should avoid decisions that make future Evidence Graph implementation unnecessarily difficult.

---

# 11. AI Analysis

The AI layer should transform retrieved information and evidence into structured research intelligence.

The AI must distinguish between:

### Facts

Directly supported information.

### Derived Quantitative Results

Calculations generated from validated data.

### Interpretation

Reasoned explanation based on available evidence.

### Uncertainty

Areas where evidence is incomplete, conflicting, stale, or insufficient.

The system must not present unsupported inference as established fact.

---

# 12. Quantitative Analysis

The MVP includes a **foundational Quant Engine**, not a full institutional-grade quant platform.

Potential MVP calculations include:

* Percentage change
* Growth rates
* Historical comparisons
* Returns
* Basic volatility
* Trend analysis
* Basic statistical relationships
* Selected valuation-related metrics where reliable inputs exist
* Simple comparative analysis

Calculations should be deterministic and validated.

The LLM must not be responsible for performing important financial arithmetic when a deterministic calculation can be used.

---

# 13. Quant Engine Boundary

### MVP

```text
Basic validated financial calculations
        +
Basic statistical analysis
        +
Historical comparisons
        +
Research-oriented quantitative context
```

### Post-MVP

```text
Advanced factor models
        +
Portfolio optimization
        +
Advanced risk models
        +
Strategy construction
        +
Backtesting
        +
Simulation systems
        +
Execution infrastructure
```

---

# 14. Temporal Awareness

The MVP must respect time.

The system should distinguish between:

* Current information
* Historical information
* Publication date
* Measurement date
* Event date
* Data availability date

The system must avoid using information that would not have been available at the relevant historical point when performing historical analysis.

This prevents accidental look-ahead bias.

---

# 15. Uncertainty Handling

The MVP must explicitly handle uncertainty.

Examples:

```text
Insufficient data
Conflicting sources
Stale information
Unavailable historical data
Low-confidence interpretation
Incomplete financial information
```

The system should communicate uncertainty rather than inventing missing information.

---

# 16. Missing Data Behavior

When required information is unavailable:

```text
DO NOT:
- fabricate values
- estimate without disclosure
- silently substitute unrelated data
- create fictional sources
```

Instead:

```text
Identify missing information
        ↓
Explain its relevance
        ↓
Continue with available evidence where possible
        ↓
State limitations
```

---

# 17. Contradictory Sources

When credible sources disagree, the system should not silently choose one.

The MVP should:

1. Identify the disagreement.
2. Present the relevant source information.
3. Identify differences in date, methodology, or definitions where possible.
4. Explain what can and cannot be established.
5. Preserve uncertainty when unresolved.

---

# 18. Research Response Structure

A standard research response should generally follow:

```text
Direct Answer
      ↓
Context
      ↓
Evidence
      ↓
Quantitative Analysis
      ↓
Interpretation
      ↓
Risks / Limitations
      ↓
Sources
```

The exact structure may vary depending on the user query.

The system should not force irrelevant sections into every answer.

---

# 19. Company / Entity Research

The MVP should support a focused research workflow around financial entities.

Example:

```text
User
 ↓
Searches company
 ↓
Company research page
 ↓
Financial context
 ↓
Recent developments
 ↓
Evidence
 ↓
Quantitative analysis
 ↓
AI interpretation
```

The initial implementation should prioritize a focused set of supported entities and markets rather than attempting universal coverage immediately.

---

# 20. “Why Is It Moving?” Workflow

The MVP should support a research workflow for questions such as:

> “Why is NVIDIA moving today?”

Conceptually:

```text
User Question
      ↓
Identify Entity
      ↓
Identify Relevant Time Window
      ↓
Retrieve Market Data
      ↓
Retrieve Relevant News / Events
      ↓
Retrieve Supporting Evidence
      ↓
Quantify Movement
      ↓
Compare Relevant Context
      ↓
AI Analysis
      ↓
Explain Drivers + Uncertainty
      ↓
Sources
```

The system must not present speculative explanations as confirmed causes.

---

# 21. Research Comparison

The MVP may support basic comparison workflows.

Examples:

```text
Company A vs Company B
```

```text
Company performance across periods
```

```text
Historical financial comparison
```

Comparisons must use clearly defined metrics and time periods.

The MVP does not require advanced portfolio construction or optimization.

---

# 22. Trust UI

Trust is a core MVP requirement.

The interface should make it easy to inspect:

* Sources
* Evidence
* Dates
* Calculations
* Important assumptions
* Uncertainty
* Limitations

Core principle:

> **Evidence Before Trust.**

The product should not depend on users blindly trusting the AI.

---

# 23. Search and Retrieval

The MVP requires reliable retrieval.

The system should prioritize:

1. Relevance
2. Recency where appropriate
3. Source quality
4. Temporal correctness
5. Entity correctness
6. Evidence traceability

Retrieval quality is a core product capability, not merely an infrastructure detail.

---

# 24. Reliability Requirements

The MVP should degrade gracefully.

If a provider fails:

```text
Provider Failure
      ↓
Fallback / Retry where appropriate
      ↓
Alternative supported source
      ↓
Partial result if possible
      ↓
Transparent limitation
```

The system must not fabricate an answer merely because a data provider is unavailable.

---

# 25. MVP User Experience

The initial UX should prioritize:

* Fast research
* Clean information hierarchy
* Minimal cognitive load
* Clear evidence
* Readable quantitative information
* Transparent sourcing
* Professional financial-research aesthetics

The MVP should feel like a serious research product rather than:

* A generic chatbot
* A social trading app
* A crypto dashboard
* A gamified finance application

---

# 26. MVP Security

Security is in scope from the beginning.

Minimum requirements include:

* Secure secrets handling
* Environment-based configuration
* Authentication architecture where required
* Authorization boundaries
* Input validation
* API security
* Protection of user research data
* Protection against prompt injection where external documents are processed
* Logging without exposing sensitive secrets

Security must not be treated as a post-MVP feature.

---

# 27. Data Licensing

Only data sources with an appropriate legal basis may be used in production.

The MVP must document:

* Provider
* Data type
* Access method
* License / terms
* Usage limitations
* Attribution requirements
* Rate limits
* Commercial-use restrictions

Unrestricted scraping must not be assumed to be acceptable.

---

# 28. Regulatory Boundary

The MVP is a financial intelligence and research product.

The initial system should avoid automatically:

* Executing trades
* Connecting to brokerage accounts for autonomous execution
* Making autonomous investment decisions
* Guaranteeing financial returns
* Presenting predictions as certainty
* Automatically managing user portfolios
* Performing regulated personalized investment advisory activity without appropriate review and compliance

The exact regulatory boundary must be validated separately with qualified legal/compliance professionals before relevant features are launched.

---

# 29. Explicit MVP Exclusions

The following are **OUT OF MVP SCOPE**:

### Trading

* Automated trading
* Brokerage execution
* Autonomous order placement
* Trading bots

### Portfolio Automation

* Autonomous portfolio management
* Automatic rebalancing
* Automated investment execution

### Advanced Quant

* Full quantitative strategy platform
* Advanced factor research platform
* Institutional portfolio optimization
* Complex simulation infrastructure

### Strategy Builder

* Full natural-language strategy builder
* Production backtesting platform
* Strategy marketplace

### Personal Finance

* Full personal finance platform
* Bank automation
* Expense automation
* Payday automation
* Goal automation
* Personal financial copilot
* Automated asset allocation

### Advanced AI Agents

* Autonomous multi-agent ecosystem
* Agent marketplace
* Self-directed financial agents
* Fully autonomous research operations

### Enterprise

* Enterprise SSO
* Enterprise administration
* Enterprise billing
* Private deployments
* Custom institutional agents
* Advanced audit infrastructure

### Infrastructure

* Full global knowledge graph
* Public financial API marketplace
* Third-party developer ecosystem
* Global financial data coverage

These capabilities belong to NEXT or VISION unless the scope is formally changed.

---

# 30. MVP Priority Levels

## P0 — Required

These capabilities are required for the MVP:

* Financial data retrieval
* Evidence retrieval
* Source attribution
* AI financial research
* Basic quantitative analysis
* Temporal awareness
* Uncertainty handling
* Missing-data handling
* Trust/evidence UI
* Reliable research responses
* Security foundations
* Data-source documentation

---

## P1 — Important

These should be included if they can be implemented without delaying the core loop:

* Company research page
* Research history
* Basic comparison workflow
* “Why is it moving?” workflow
* Contradictory-source handling
* Additional quantitative metrics
* Improved retrieval ranking
* Research response customization

---

## P2 — Deferred

These should normally wait until after MVP validation:

* Advanced strategy builder
* Advanced backtesting
* Portfolio intelligence
* Personal finance intelligence
* Goal engine
* Payday intelligence
* Paper trading
* Agent ecosystem
* Knowledge graph expansion
* Marketplace
* Enterprise features

---

# 31. MVP Minimum Shippable Product

The smallest meaningful version of QuantMind should allow a user to:

```text
Ask a financial research question
        ↓
Identify the relevant entity / context
        ↓
Retrieve reliable information
        ↓
Retrieve supporting evidence
        ↓
Perform validated quantitative analysis
        ↓
Generate an explainable AI response
        ↓
Inspect supporting sources
        ↓
Understand uncertainty and limitations
```

If this loop does not work reliably, additional features should not be prioritized.

---

# 32. MVP Success Criteria

The MVP should demonstrate that:

### Product

* Users can complete meaningful financial research tasks.
* Research is faster and easier to verify than manually gathering fragmented information.
* Evidence is visible and understandable.
* AI responses remain grounded in available information.

### Technical

* Retrieval works reliably.
* Quantitative calculations are deterministic.
* Temporal constraints are respected.
* Failures are handled gracefully.
* Important claims can be traced to evidence.

### Trust

* Unsupported claims are minimized.
* Sources are transparent.
* Uncertainty is communicated.
* Users can inspect evidence instead of blindly trusting the AI.

### Validation

The MVP should be tested with real users before major expansion of scope.

---

# 33. Scope Freeze Rule

Once implementation begins, MVP scope should be treated as frozen unless a change is explicitly approved.

A proposed new feature must answer:

```text
1. Does it strengthen the core MVP loop?
2. Is it required for the primary user job?
3. Can the MVP work without it?
4. What existing scope does it replace or delay?
5. Does it introduce new data, regulatory, or infrastructure complexity?
```

If the feature does not materially strengthen the core MVP, it should normally be deferred.

---

# 34. Scope Change Protocol

A scope change must not happen silently.

The process is:

```text
Feature Request
      ↓
Document Reason
      ↓
Check Against brain.md
      ↓
Check Against PRD.md
      ↓
Evaluate MVP Impact
      ↓
Update MVP-Scope.md
      ↓
Update Relevant Technical/Product Documents
      ↓
Record Decision in Decision-Log.md
      ↓
Implement
```

No major feature should be implemented first and documented later.

---

# 35. AI Coding Agent Rules

Any AI coding agent working on QuantMind must:

1. Read `brain.md` first.
2. Read `docs/PRD.md`.
3. Read `docs/MVP-Scope.md`.
4. Identify whether the requested work is within MVP scope.
5. Follow existing architectural decisions.
6. Never silently expand MVP scope.
7. Never invent financial data.
8. Never invent sources.
9. Never bypass evidence requirements.
10. Never replace deterministic financial calculations with unsupported LLM reasoning.
11. Preserve temporal correctness.
12. Surface conflicts before implementation.
13. Update documentation when an approved architectural decision changes.
14. Keep deferred capabilities out of the implementation unless explicitly approved.

---

# 36. Definition of “Done” for MVP Scope

MVP scope is considered complete when:

```text
Core Research Workflow
        +
Evidence Retrieval
        +
Source Attribution
        +
Validated Quant Analysis
        +
AI Explanation
        +
Temporal Awareness
        +
Uncertainty Handling
        +
Trust UI
        +
Security Foundations
        +
Data Strategy
```

are implemented sufficiently to support real-world validation.

The MVP is not considered complete merely because the interface exists.

The underlying intelligence loop must function.

---

# 37. Scope Philosophy

QuantMind should not attempt to win by having the largest number of features.

The initial product should prove one important capability:

> **Turn fragmented financial information into evidence-backed, explainable financial intelligence.**

Depth comes before breadth.

Reliability comes before autonomy.

Evidence comes before confidence.

Validation comes before expansion.

---

# 38. Final MVP Boundary

```text
                         QUANTMIND AI
                              │
                    ┌─────────┴─────────┐
                    │                   │
                  MVP               FUTURE
                    │                   │
          Financial Research       Portfolio Intelligence
          Intelligence             Personal Finance
                    │               Strategy Builder
          ┌─────────┴─────────┐     Backtesting
          │                   │     Paper Trading
       Data + Evidence        │     Agents
          │                   │     Marketplace
          ↓                   ↓     Enterprise
     Quant Analysis      AI Analysis
          │                   │
          └─────────┬─────────┘
                    ↓
          Explainable Intelligence
                    │
                    ↓
             Evidence + Sources
```

The MVP exists to prove this loop before QuantMind expands into the broader financial intelligence platform.

---

# 39. Final Rule

> **Build the smallest product that proves QuantMind's core intelligence loop.**
>
> **Do not build the entire vision inside the MVP.**
>
> **If a capability is not required to deliver evidence-backed financial research intelligence, defer it unless explicitly approved.**
