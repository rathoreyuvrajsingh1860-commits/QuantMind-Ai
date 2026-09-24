# QuantMind AI

> **Think Beyond the Market.**

**Status:** Phase 0 — Foundation / Pre-MVP
**Document Type:** Developer Entry Point
**Version:** 1.0
**Last Updated:** 2026-09-22

---

## 1. What Is QuantMind AI?

QuantMind AI is an **AI-powered Financial Intelligence Platform** designed to turn fragmented financial information into continuously updated, explainable intelligence.

QuantMind combines:

* Financial data
* Market information
* News
* Filings
* Earnings
* Macro data
* Quantitative analysis
* AI reasoning
* Evidence and provenance

into a unified research experience.

QuantMind is not intended to be a generic financial chatbot.

Its core philosophy is:

> **Evidence Before Trust.**

The system should not ask users to blindly trust AI-generated conclusions. It should show the evidence, sources, calculations, assumptions, uncertainty, and relevant limitations behind its outputs.

---

# 2. Current Phase

QuantMind AI is currently in:

> **Phase 0 — Foundation / Pre-MVP**

The immediate objective is **not** to build the entire long-term platform.

The immediate objective is to establish:

1. Correct product architecture
2. Clear MVP boundaries
3. Reliable financial data foundations
4. Evidence-backed research
5. Deterministic quantitative calculations
6. Explainable AI analysis
7. Evaluation infrastructure
8. A clean research-first user experience

Documentation must precede major implementation.

---

# 3. MVP Definition

The QuantMind MVP is:

> **An AI-powered Financial Research Intelligence system that retrieves relevant financial information, connects evidence, performs supported quantitative analysis, and produces explainable intelligence with transparent sourcing and uncertainty handling.**

The MVP is **not** the complete QuantMind platform.

### Core MVP Loop

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

The product should optimize for **research quality before automation**.

---

# 4. Product Philosophy

## Evidence Before Trust

Every meaningful AI-generated conclusion should be supported by appropriate evidence whenever evidence is available.

The system should distinguish between:

* Facts
* Derived calculations
* Interpretation
* Assumptions
* Uncertainty
* Limitations
* Conflicting information

AI is **not the source of truth**.

Financial data, validated calculations, and cited evidence form the foundation of truth.

---

# 5. Three-Horizon Product Model

All product decisions use three horizons.

| Horizon    | Meaning                       |
| ---------- | ----------------------------- |
| **NOW**    | What we are actually building |
| **NEXT**   | What follows after the MVP    |
| **VISION** | Long-term QuantMind platform  |

### NOW

Financial Research Intelligence:

* Financial data retrieval
* Evidence retrieval
* Source attribution
* AI research analysis
* Company/entity research
* Quantitative analysis
* Temporal awareness
* Uncertainty handling
* Contradictory-source handling
* Why-moving research
* Comparison workflows
* Evidence/trust UI

### NEXT

Capabilities such as:

* Advanced quant research
* Strategy builder
* Backtesting
* Portfolio intelligence
* Paper trading
* Expanded market intelligence
* Personal finance intelligence
* Goal planning
* Payday intelligence

### VISION

The long-term QuantMind ecosystem:

* Financial intelligence platform
* Knowledge Graph
* Evidence Graph
* Agent ecosystem
* Enterprise intelligence
* APIs
* Marketplace
* Personal financial copilot
* Financial automation where legally and technically appropriate

Future capabilities must not leak into the MVP without an explicit scope decision.

---

# 6. MVP Features

The MVP should support the following core capabilities.

## Financial Data

Retrieve relevant financial information from approved and appropriately licensed sources.

## Research

Allow users to investigate companies, securities, events, and financial questions.

## Evidence

Connect conclusions to supporting evidence.

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
CONFIDENCE / UNCERTAINTY
  ↓
LIMITATION / COUNTERARGUMENT
```

## Quantitative Analysis

The MVP may perform supported deterministic calculations such as:

* Percentage changes
* Growth rates
* Historical comparisons
* Returns
* Volatility
* Basic statistical relationships
* Trend analysis
* Supported financial metrics

Financial arithmetic must be deterministic and testable.

LLMs must not be treated as the authoritative calculator.

## AI Analysis

AI should:

* Understand research intent
* Retrieve relevant information
* Connect evidence
* Interpret validated information
* Explain relationships
* Surface risks and limitations
* Clearly distinguish fact from interpretation
* Communicate uncertainty

AI should not fabricate unavailable information.

---

# 7. Core Intelligence Architecture

The conceptual intelligence flow is:

```text
User
 ↓
Intent Understanding
 ↓
Entity Resolution
 ↓
Task Planning
 ↓
Data Retrieval
 ↓
Evidence Retrieval
 ↓
Quantitative Analysis
 ↓
AI Reasoning
 ↓
Verification
 ↓
Response Composition
 ↓
Evidence + Sources
 ↓
User Understanding
```

The system must not become:

```text
User
 ↓
LLM
 ↓
Answer
```

The architecture exists to make financial intelligence **traceable, testable, and explainable**.

---

# 8. Technical Architecture

The MVP uses a **modular monolith** architecture.

## Locked Technology Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js + TypeScript + Tailwind CSS |
| Backend | Python + FastAPI |
| Database | PostgreSQL |
| Database Hosting | Supabase PostgreSQL |
| Authentication | Supabase Auth |
| AI Architecture | Provider-agnostic AI interface / adapters |
| Financial Data Architecture | Provider-agnostic data interfaces / adapters |

The exact AI model/provider and financial-data providers are intentionally not locked to a single vendor. They must be selected through evaluation of reliability, accuracy, coverage, licensing, cost, and technical compatibility.

Conceptually:

```text
Presentation
     ↓
API / Application Layer
     ↓
Intelligence Orchestration
     ↓
Data Services
     ↓
Evidence Services
     ↓
Quant Engine
     ↓
AI / Reasoning Layer
     ↓
Persistence

Major logical modules include:

src/
├── api/
├── auth/
├── research/
├── entities/
├── retrieval/
├── evidence/
├── quant/
├── ai/
├── verification/
├── data/
├── storage/
├── config/
├── observability/
└── shared/

The MVP remains a modular monolith even though its internal modules have clear boundaries.

Technology decisions are governed by docs/Decision-Log.md.

Do not introduce competing frameworks, providers, databases, or architectural patterns without documenting the change first.
---

# 9. Repository Structure

The current documentation architecture is:

```text
QuantMind-AI/
│
├── brain.md
│
├── docs/
│   ├── PRD.md
│   ├── MVP-Scope.md
│   ├── TRD.md
│   ├── Data-Sources.md
│   ├── UI-UX-Design-Brief.md
│   ├── App-Flow.md
│   └── Decision-Log.md
│
├── README.md
├── .env.example
├── .gitignore
│
└── src/
```

The `src/` implementation structure becomes active after the documentation foundation is sufficiently defined.

---

# 10. Documentation Hierarchy

Before making major implementation decisions, read the documentation in this order:

```text
brain.md
   ↓
docs/PRD.md
   ↓
docs/MVP-Scope.md
   ↓
docs/TRD.md
   ↓
docs/Data-Sources.md
   ↓
docs/UI-UX-Design-Brief.md
   ↓
docs/App-Flow.md
   ↓
docs/Decision-Log.md
   ↓
Implementation
```

### Responsibilities

| Document                | Responsibility                         |
| ----------------------- | -------------------------------------- |
| `brain.md`              | Project constitution / source of truth |
| `PRD.md`                | Product specification                  |
| `MVP-Scope.md`          | NOW / NEXT / VISION boundary           |
| `TRD.md`                | Technical architecture                 |
| `Data-Sources.md`       | Data strategy and provenance           |
| `UI-UX-Design-Brief.md` | Design system and UX direction         |
| `App-Flow.md`           | User and system flows                  |
| `Decision-Log.md`       | Architectural/product decisions        |
| `README.md`             | Developer entry point                  |

If documents conflict, do not silently choose one.

Follow the documented change-control process and update the appropriate source document first.

---

# 11. AI Coding Agent Protocol

Any AI coding agent working on QuantMind must first understand the project constitution and current scope.

Before writing code:

1. Read `brain.md`
2. Read `docs/PRD.md`
3. Read `docs/MVP-Scope.md`
4. Read relevant technical/product documents
5. Identify the requested feature
6. Determine whether it belongs to NOW, NEXT, or VISION
7. Check existing architectural decisions
8. Identify dependencies and constraints
9. Implement only the documented scope
10. Validate the implementation
11. Update documentation when a decision changes

### Golden Rule

> **Build what is documented. Document what is decided. Validate what is assumed. Never silently change the architecture.**

---

# 12. Development Principles

## 12.1 Evidence Before Trust

Research outputs should be traceable to evidence.

## 12.2 Deterministic Quant Before Generative Interpretation

Calculations must be handled by deterministic systems where possible.

## 12.3 Data Before AI

AI should operate on validated information rather than inventing financial facts.

## 12.4 Provenance Is a First-Class Feature

Every important piece of financial information should retain appropriate source and temporal context.

## 12.5 Temporal Correctness

Historical analysis must respect what information was actually available at the relevant point in time.

Avoid look-ahead bias.

## 12.6 No Fabrication

If information is unavailable:

```text
Do not invent it.
Do not silently substitute it.
Do not present an assumption as fact.
```

Instead, communicate the limitation.

## 12.7 Contradictions Remain Visible

When credible sources disagree, the system should not silently hide the disagreement.

## 12.8 Explainability

Users should be able to understand:

* What the system concluded
* Why it reached that conclusion
* What evidence supports it
* What calculations were performed
* What assumptions exist
* What remains uncertain

## 12.9 Graceful Degradation

A provider failure should not unnecessarily break the entire research experience.

Use appropriate fallbacks where permitted.

## 12.10 Security by Design

Secrets, credentials, user data, financial information, and internal system information must be handled securely.

---

# 13. Data Principles

QuantMind follows these rules:

```text
Source First
     ↓
Provenance
     ↓
Validation
     ↓
Normalization
     ↓
Storage
     ↓
Retrieval
     ↓
Analysis
```

Important principles:

* Public availability does not automatically mean commercial permission.
* Data licensing must be evaluated.
* Unrestricted scraping is not assumed.
* Source provenance must be preserved.
* Units and currencies must be explicit.
* Corporate actions must be handled correctly.
* Data freshness must be tracked.
* Provider failures must be handled.
* Conflicting data must remain identifiable.

See `docs/Data-Sources.md` for the complete strategy.

---

# 14. Financial Safety Boundary

QuantMind is being built as a financial intelligence and research platform.

The MVP must not provide:

* Guaranteed returns
* Guaranteed predictions
* Autonomous investment decisions
* Automated brokerage execution
* Automated trading
* Uncontrolled portfolio management
* Fabricated financial certainty

Research and analysis must not automatically be treated as personalized investment advice.

Any future capability involving personalized financial advice, execution, or automated financial actions requires separate legal, regulatory, product, and technical review.

---

# 15. Explicit MVP Exclusions

The following are intentionally outside the current MVP unless the scope is formally changed:

```text
Automated Trading
Brokerage Execution
Autonomous Portfolio Management
Advanced Backtesting
Full Strategy Builder
Paper Trading
Full Personal Finance Platform
Automated Bank Management
Advanced Agent Marketplace
Enterprise Platform
Public API Marketplace
Full Knowledge Graph
Unrestricted Web Scraping
Full Financial Automation
```

These are future capabilities, not missing MVP features.

---

# 16. Testing and Evaluation

QuantMind must be evaluated as a financial intelligence system, not simply as a chatbot.

Evaluation should cover:

### Data

* Retrieval correctness
* Source validity
* Freshness
* Entity correctness
* Temporal correctness

### Quant

* Arithmetic correctness
* Formula correctness
* Unit correctness
* Historical correctness
* No-lookahead behavior

### AI

* Factual grounding
* Evidence alignment
* Hallucination rate
* Fact/interpretation separation
* Uncertainty handling
* Contradiction handling

### System

* Reliability
* Failure recovery
* Latency
* Security
* Provider fallback behavior

### UX

* Research usability
* Evidence discoverability
* Source transparency
* Error clarity
* Loading states
* Missing-data handling

Evaluation infrastructure is expected to become part of QuantMind's long-term moat.

---

# 17. Development Workflow

The development process follows:

```text
Question / Requirement
        ↓
Documentation Check
        ↓
Scope Check
        ↓
Architecture Check
        ↓
Implementation
        ↓
Testing
        ↓
Evaluation
        ↓
Documentation Update
        ↓
Review
```

Do not begin by blindly writing code.

First establish what should be built and why.

---

# 18. Environment

Environment-specific configuration must be handled through environment variables.

Use:

```text
.env.example
```

as the documented template.

Never commit:

* API keys
* Authentication secrets
* Database credentials
* Private tokens
* Production secrets
* User financial information

Exact providers and infrastructure should be documented before being treated as permanent architecture.

---

# 19. Scope Change Protocol

A feature or architectural change should not be silently added.

When a new requirement appears:

```text
New Requirement
      ↓
Does it fit MVP Scope?
      ↓
YES ─────────────→ Implement
      │
      NO
      ↓
NOW / NEXT / VISION Classification
      ↓
Decision
      ↓
Documentation Update
      ↓
Implementation if approved
```

If a change conflicts with existing architecture, update the relevant documentation before implementation.

---

# 20. Current Open Decisions

The foundational technology and product decisions below have been formally documented in `docs/Decision-Log.md`.

### Accepted / Established Decisions

- Initial market coverage: India + United States
- Initial asset class: Listed equities
- Initial historical target: At least 5 years where reliable and appropriately licensed data is available
- Financial-data architecture: Provider-agnostic
- AI architecture: Provider-agnostic
- Authentication: Supabase Auth
- Database: PostgreSQL hosted through Supabase PostgreSQL
- Frontend: Next.js + TypeScript + Tailwind CSS
- Backend: Python + FastAPI
- Evaluation: Dedicated MVP evaluation dataset
- Quality: Category-specific accuracy and quality thresholds
- Retention: Data-retention policy framework

### Still Requiring Implementation-Level Decisions

The following details remain intentionally open where the Decision Log does not yet select a specific vendor or numerical value:

- Exact financial-data providers
- Exact AI model/provider
- Exact fallback AI model/provider
- Final evaluation-dataset size
- Final numerical production thresholds
- Exact retention periods by data category
- Exact historical coverage beyond the five-year target
- Provider-specific licensing arrangements
- Deployment/infrastructure configuration

These decisions must be evaluated and documented before the corresponding production implementation.

See:

```text
docs/Decision-Log.md

for the authoritative decision record.

Do not invent unresolved implementation details or treat them as permanent architecture without an explicit documented decision.

---

# 21. Product Roadmap

The long-term roadmap expands from research intelligence toward a broader financial intelligence platform.

Conceptually:

```text
Foundation
    ↓
Financial Data
    ↓
Market Intelligence
    ↓
News Intelligence
    ↓
Macro Intelligence
    ↓
Filing Intelligence
    ↓
Earnings Intelligence
    ↓
Quant Engine
    ↓
AI Research Assistant
    ↓
Evidence Graph
    ↓
Strategy Builder
    ↓
Backtesting
    ↓
Portfolio Intelligence
    ↓
Personal Finance Intelligence
    ↓
Goal Intelligence
    ↓
Payday Intelligence
    ↓
Personal Financial Copilot
    ↓
Paper Trading
    ↓
Agent Ecosystem
    ↓
Knowledge Graph / API / Marketplace
    ↓
Enterprise Financial Intelligence
```

The roadmap describes the direction of the company.

It does not override the current MVP scope.

---

# 22. Definition of a Good QuantMind Feature

A feature should be evaluated against:

1. Does it solve a real financial research/intelligence problem?
2. Is it within the current scope?
3. Can its data be sourced appropriately?
4. Can its outputs be verified?
5. Can its calculations be tested?
6. Can uncertainty be represented?
7. Does it preserve provenance?
8. Does it improve user understanding?
9. Does it introduce unnecessary complexity?
10. Does it fit the long-term architecture?

If a feature cannot satisfy these requirements, it should be reconsidered before implementation.

---

# 23. What QuantMind Is Not

QuantMind is not:

* A generic chatbot with financial prompts
* A stock-tip generator
* A guaranteed-return system
* A black-box prediction engine
* A collection of disconnected dashboards
* A crypto-style trading interface
* A replacement for evidence
* A system that hides uncertainty behind an AI confidence score

The product should feel like **financial intelligence infrastructure**, not an AI wrapper.

---

# 24. Current Success Definition

The MVP is successful when a user can ask a meaningful financial research question and receive:

```text
Relevant Information
        +
Evidence
        +
Validated Quantitative Analysis
        +
AI Interpretation
        +
Clear Uncertainty
        +
Transparent Sources
        =
Explainable Financial Intelligence
```

The system should help users understand **what happened, what the evidence says, what the numbers show, what it may mean, and what remains uncertain.**

---

# 25. Final Principle

QuantMind AI is being built around one central idea:

> **Don't ask users to trust AI. Give them the evidence to verify it.**

The goal is not to build the most complicated financial AI system.

The goal is to build a system where:

**Data is reliable.
Evidence is visible.
Calculations are correct.
Reasoning is explainable.
Uncertainty is honest.
Architecture is disciplined.
Scope is controlled.**

> **QuantMind AI — Think Beyond the Market.**
