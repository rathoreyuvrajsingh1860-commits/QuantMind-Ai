# QuantMind AI — Data Sources Strategy

> **Status:** Phase 0 — Foundation / Pre-MVP
> **Document Type:** Data Strategy / Source-of-Truth Definition
> **Version:** 1.0
> **Last Updated:** 2026-09-22
> **Product:** QuantMind AI
> **Tagline:** Think Beyond the Market.

---

# 1. Document Purpose

This document defines how QuantMind AI will acquire, validate, normalize, store, retrieve, and attribute financial data.

Data is a foundational component of QuantMind AI.

The product must not treat financial data as an interchangeable commodity.

Every important financial output should be connected to:

```text
Source
↓
Data
↓
Timestamp / Period
↓
Transformation
↓
Calculation
↓
Evidence
↓
AI Interpretation
```

The objective is to create a reliable financial data foundation that can support the MVP and eventually expand into QuantMind's broader financial intelligence infrastructure.

---

# 2. Data Philosophy

QuantMind follows:

> **Evidence Before Trust.**

The system should prefer:

```text
Reliable source
+
Correct context
+
Correct timestamp
+
Validated data
+
Transparent provenance
```

over simply retrieving the largest amount of information.

More data does not automatically mean better intelligence.

---

# 3. Data Strategy Principles

## 3.1 Source First

Every production data source must have a documented origin.

## 3.2 Provenance

Important data must retain information about where it came from.

## 3.3 Temporal Correctness

Data must preserve the date or period to which it belongs.

## 3.4 Licensing Awareness

QuantMind must not assume that publicly accessible data is automatically free for commercial use.

## 3.5 Validation

External data must be validated before being used in important calculations.

## 3.6 Normalization

Different providers should be normalized into internal formats where practical.

## 3.7 Provider Independence

The product should avoid unnecessary dependence on a single external provider.

## 3.8 Graceful Degradation

If a provider becomes unavailable, the system should fail safely rather than invent information.

---

# 4. MVP Data Categories

The MVP may require the following categories:

```text
1. Market Data
2. Company / Entity Data
3. Financial Statement Data
4. Filing / Regulatory Documents
5. Earnings Information
6. News / Events
7. Macro / Economic Data
8. Reference Data
9. Evidence / Source Metadata
10. Quantitative Derived Data
```

The exact provider set will be finalized after evaluation of coverage, reliability, licensing, cost, and API capabilities.

---

# 5. Market Data

Market data may include:

* Price
* Open
* High
* Low
* Close
* Adjusted close where supported
* Volume
* Returns
* Market capitalization
* Trading dates
* Corporate-action information where available

Conceptual structure:

```text
Entity
↓
Instrument
↓
Timestamp
↓
OHLCV / Market Metric
↓
Source
```

---

# 6. Market Data Requirements

Market data must preserve:

* Instrument
* Exchange / market
* Currency
* Timestamp
* Timezone
* Price type
* Adjustment status
* Source
* Retrieval time

The system must not silently mix adjusted and unadjusted prices.

---

# 7. Company / Entity Data

Entity data may include:

* Legal/company name
* Common name
* Ticker
* Exchange
* Country
* Sector
* Industry
* Currency
* Entity identifiers
* Corporate relationships where supported

Entity identifiers should be normalized internally.

Example:

```text
NVIDIA
NVDA
NVIDIA Corporation
```

should resolve consistently when they refer to the same entity.

---

# 8. Financial Statement Data

Where available and appropriately licensed, QuantMind may retrieve:

* Revenue
* Gross profit
* Operating income
* Net income
* EPS
* Assets
* Liabilities
* Equity
* Cash
* Debt
* Cash flow
* Capital expenditure
* Other relevant financial metrics

Each financial value must preserve:

```text
Metric
Value
Currency
Period
Period Type
Reporting Date
Source
```

---

# 9. Financial Periods

Financial data must distinguish:

```text
Annual
Quarterly
Trailing Twelve Months
Year-to-Date
Monthly
Daily
```

The system must not compare values across incompatible periods without explicitly handling the difference.

---

# 10. Filings and Regulatory Documents

Where available, filings can provide primary evidence for financial research.

Potential document categories include:

* Annual reports
* Quarterly reports
* Current reports
* Regulatory disclosures
* Prospectuses
* Earnings-related filings
* Other official corporate disclosures

Primary documents should generally receive higher evidentiary priority than secondary commentary when answering factual questions about the company itself.

---

# 11. Filing Metadata

Each document should preserve:

```text
Document ID
Entity
Document Type
Publication Date
Period
Source
Source URL / Reference
Retrieval Time
Content Location
```

Where possible, the system should retain a stable reference to the original document.

---

# 12. Earnings Data

Earnings-related information may include:

* Earnings date
* Reported revenue
* Reported EPS
* Guidance
* Management commentary
* Earnings-call information
* Relevant financial changes

The system must distinguish:

```text
Reported Results
Management Guidance
Analyst Estimates
AI Interpretation
```

These categories must not be silently merged.

---

# 13. News Data

News can provide context around:

* Company events
* Market movements
* Earnings
* Product announcements
* Regulatory events
* Mergers and acquisitions
* Management changes
* Macro developments
* Industry developments

News should be treated as contextual evidence rather than automatically as ground truth.

---

# 14. News Metadata

A news record should preserve, where available:

```text
Headline
Publisher
Author
Publication Time
URL / Reference
Entity
Topic
Retrieved Time
Source Type
```

News must retain publication timestamps.

---

# 15. News Recency

Different research questions require different freshness windows.

For example:

```text
"Why is the stock moving today?"
        ↓
Highly recent information

"How did revenue change over five years?"
        ↓
Historical financial information

"What happened during the previous earnings cycle?"
        ↓
Relevant historical event window
```

The retrieval system must choose the time window according to the query rather than applying one universal freshness rule.

---

# 16. Macro / Economic Data

Macro information may eventually include:

* Inflation
* Interest rates
* GDP
* Employment
* Currency rates
* Commodity prices
* Economic indicators
* Central-bank information

Macro data should only be included in the MVP when it directly contributes to the requested research workflow and a suitable source is available.

---

# 17. Primary vs Secondary Sources

QuantMind should distinguish source types.

## Primary Sources

Examples:

* Regulatory filings
* Official company releases
* Official government datasets
* Central-bank publications
* Official financial statements

## Secondary Sources

Examples:

* Financial news organizations
* Research publications
* Industry analysis
* Market commentary

Primary sources should generally be preferred for establishing factual claims when available and relevant.

Secondary sources can provide context, interpretation, and additional information.

---

# 18. Source Reliability Model

The system should consider:

```text
Source Authority
+
Directness
+
Recency
+
Relevance
+
Data Quality
+
Temporal Validity
```

Source quality should not be reduced to a single universal numerical score unless a validated methodology is established.

---

# 19. Source Registry

QuantMind should maintain an internal source registry.

Conceptually:

```text
Source
├── Name
├── Provider
├── Category
├── Coverage
├── Markets
├── Data Types
├── Access Method
├── License
├── Rate Limits
├── Cost
├── Reliability Notes
└── Status
```

This registry becomes the operational source of truth for data integrations.

---

# 20. Provider Evaluation Criteria

Before integrating a provider, evaluate:

### Coverage

Does it contain the required:

* Markets
* Companies
* Assets
* Historical periods
* Data categories?

### Reliability

Does it provide:

* Consistent availability
* Stable APIs
* Correct data
* Predictable schemas?

### Freshness

How quickly does data become available?

### Licensing

Can the data be used for:

* Research
* Commercial products
* AI processing
* Storage
* Redistribution?

### Cost

Consider:

* Free tier
* Development pricing
* Production pricing
* Usage-based pricing
* Enterprise pricing

### Technical Quality

Consider:

* API design
* Documentation
* Rate limits
* Authentication
* Webhooks
* SDK support

---

# 21. Provider Abstraction

External providers should be accessed through internal interfaces.

Conceptually:

```text
Internal QuantMind Interface
            │
     ┌──────┼──────┐
     ▼      ▼      ▼
 Provider A Provider B Provider C
```

Example:

```text
MarketDataProvider
NewsProvider
FilingProvider
CompanyProvider
MacroProvider
```

Application code should depend primarily on the internal interface rather than directly on provider-specific APIs.

---

# 22. Provider Selection Rule

No provider should be selected solely because it is:

* Popular
* Cheap
* Free
* Easy to integrate

Selection should consider the complete combination of:

```text
Coverage
+
Accuracy
+
Reliability
+
Freshness
+
Licensing
+
Cost
+
Technical Quality
```

---

# 23. Development vs Production Sources

A provider acceptable for experimentation may not be acceptable for production.

Maintain separate classifications:

```text
Development
Prototype
Evaluation
Production
```

A development source must not automatically become a production source.

---

# 24. Data Normalization

External providers may represent the same concept differently.

Example:

```text
Provider A:
revenue

Provider B:
totalRevenue

Provider C:
sales
```

QuantMind should map these into a common internal representation where they represent the same concept.

---

# 25. Canonical Data Model

A canonical financial data record should conceptually contain:

```text
Entity
Metric
Value
Unit
Currency
Period
Timestamp
Source
Provider
Retrieved At
Quality / Validation Status
```

Additional metadata may be added where required.

---

# 26. Data Quality Validation

Before data is used:

```text
Raw Data
 ↓
Schema Validation
 ↓
Type Validation
 ↓
Unit Validation
 ↓
Currency Validation
 ↓
Temporal Validation
 ↓
Range / Consistency Checks
 ↓
Canonical Representation
```

Invalid data should be rejected or explicitly marked.

---

# 27. Data Lineage

Derived information should preserve lineage.

Example:

```text
Revenue 2024
       +
Revenue 2025
       ↓
Growth Calculation
       ↓
Revenue Growth
       ↓
AI Interpretation
```

The system should be able to explain how an important derived metric was produced.

---

# 28. Quantitative Derived Data

Derived data may include:

* Returns
* Growth rates
* Volatility
* Drawdown
* Moving averages
* Ratios
* Historical comparisons
* Statistical relationships

Derived values must preserve:

```text
Input Data
Formula / Method
Calculation Time
Result
Unit
```

---

# 29. Calculation Provenance

Example:

```text
Metric:
Revenue Growth

Inputs:
Revenue FY2024
Revenue FY2025

Formula:
((FY2025 - FY2024) / FY2024) × 100

Result:
X%

Source:
Underlying financial statement data
```

This enables evidence-backed quantitative explanations.

---

# 30. Data Freshness Metadata

Each data record should preserve:

```text
Published At
Effective At
Retrieved At
Updated At
```

These timestamps have different meanings and must not be treated as interchangeable.

---

# 31. Historical Data

Historical datasets should preserve the original time context.

The system must avoid:

* Replacing historical values without tracking revisions
* Mixing revised data with original data without disclosure
* Using future information in historical analysis
* Losing the reporting period

Where revisions are relevant, they should be represented explicitly.

---

# 32. Corporate Actions

Where relevant, market data may be affected by:

* Stock splits
* Dividends
* Mergers
* Spin-offs
* Symbol changes
* Other corporate actions

The system must understand whether a dataset is adjusted or unadjusted before performing historical calculations.

---

# 33. Currency Handling

All financial values must include currency where applicable.

The system must not silently convert currencies.

When conversion is performed:

```text
Original Currency
+
Exchange Rate
+
Exchange Rate Timestamp
+
Conversion Method
=
Converted Value
```

The conversion should be traceable.

---

# 34. Units

Financial values should preserve their scale.

Examples:

```text
USD
USD thousands
USD millions
USD billions
INR
INR crore
INR lakh
```

A value of:

```text
500
```

is not meaningful without knowing its unit and scale.

---

# 35. Data Storage

Stored data should be divided conceptually into:

```text
Raw / Source Data
Canonical Data
Evidence
Derived Data
Application Data
```

The architecture should avoid mixing raw provider payloads with user-facing canonical records.

---

# 36. Raw Data

Where licensing permits storage, raw provider responses may be retained for:

* Debugging
* Reprocessing
* Auditability
* Schema migration
* Data-quality analysis

Retention must follow provider terms and applicable policies.

---

# 37. Evidence Storage

Evidence records should preserve enough context to allow the system to identify:

* Source
* Relevant content
* Publication date
* Retrieval time
* Related entity
* Related claim

Evidence storage must not imply that QuantMind owns the underlying source content.

---

# 38. Data Licensing

Before production use, document:

```text
Provider
License / Terms
Allowed Usage
Storage Rights
AI Processing Rights
Redistribution Rights
Attribution Requirements
Commercial Restrictions
Retention Rules
```

Public accessibility is not equivalent to commercial redistribution permission.

---

# 39. Scraping Policy

Unrestricted scraping is not part of the default QuantMind data strategy.

Before scraping any source, evaluate:

* Terms of service
* robots directives where relevant
* Copyright considerations
* Commercial-use restrictions
* Rate limits
* Technical stability
* Data redistribution rights

Approved sources should be documented.

---

# 40. AI Training vs AI Retrieval

QuantMind should distinguish:

```text
Using data as retrieval context
```

from:

```text
Using data to train / fine-tune a model
```

A source permitted for retrieval is not automatically permitted for model training.

These rights must be evaluated separately.

---

# 41. Data Access Security

Provider credentials must:

* Never be committed to Git
* Never appear in frontend code
* Never be included in client-side bundles
* Be stored in secure environment configuration
* Be rotated when necessary

---

# 42. Rate Limits

Each provider should document:

```text
Requests per minute
Requests per day
Concurrent requests
Historical-data limits
Endpoint-specific restrictions
```

The retrieval layer should enforce appropriate controls.

---

# 43. Retry Strategy

Provider failures may be retried when appropriate.

Conceptually:

```text
Request
 ↓
Failure
 ↓
Determine Retryable?
 ├── No → Fail / Fallback
 └── Yes
       ↓
     Backoff
       ↓
     Retry
       ↓
     Fallback / Fail Gracefully
```

Retries must not create excessive provider load.

---

# 44. Fallback Sources

Fallbacks should preserve semantic compatibility.

For example:

```text
Market Price
Provider A
   ↓ unavailable
Provider B
```

is only acceptable when Provider B provides sufficiently compatible information.

The system should not substitute an unrelated metric merely to produce an answer.

---

# 45. Data Availability States

Each data request should conceptually support:

```text
AVAILABLE
PARTIALLY_AVAILABLE
STALE
UNAVAILABLE
INVALID
CONFLICTING
```

The AI layer should receive these states where relevant.

---

# 46. Contradictory Data

If two sources disagree:

```text
Source A → Value X
Source B → Value Y
```

the system should not silently overwrite one.

It should evaluate:

* Publication time
* Reporting period
* Definition
* Source authority
* Revision status
* Methodology

If unresolved, the disagreement should remain visible.

---

# 47. Source Attribution in UI

Where data materially contributes to a response, users should be able to inspect the relevant source.

The UI should provide enough information to distinguish:

```text
Source
Date
Data / Evidence
```

from:

```text
AI Interpretation
```

---

# 48. Data Access Architecture

Conceptually:

```text
                    QUANTMIND
                        │
                Data Access Layer
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
   Market Data      Documents         News
        │               │               │
        └───────────────┼───────────────┘
                        ▼
                 Normalization
                        │
                        ▼
                   Validation
                        │
                        ▼
                    Storage
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
         Retrieval             Quant
              │                   │
              └─────────┬─────────┘
                        ▼
                   AI Analysis
```

---

# 49. MVP Data Priorities

## P0

Required for the core research loop:

* Entity/reference data
* Market data
* Relevant financial metrics
* News / event context
* Source metadata
* Evidence
* Historical data required by supported calculations

## P1

Important where supported:

* Filings
* Earnings information
* Macro data
* Expanded financial statement data

## P2

Future expansion:

* Alternative data
* Institutional flows
* Options intelligence
* Satellite / geospatial data
* Proprietary datasets
* Advanced real-time feeds

---

# 50. Data Scope Control

QuantMind should not attempt to support every financial market at launch.

Initial coverage should be explicitly documented:

```text
Markets:
[To be finalized]

Asset Classes:
[To be finalized]

Geographies:
[To be finalized]

Historical Coverage:
[To be finalized]
```

These decisions must be recorded before production data architecture is finalized.

---

# 51. Data Evaluation Before Integration

Every candidate provider should go through:

```text
Coverage Test
      ↓
Accuracy Test
      ↓
Freshness Test
      ↓
API Stability Test
      ↓
Licensing Review
      ↓
Cost Analysis
      ↓
Integration Test
      ↓
Production Decision
```

The result should be recorded in the source registry or `Decision-Log.md`.

---

# 52. Data Quality Monitoring

QuantMind should eventually monitor:

* Missing data
* Provider failures
* Unexpected values
* Duplicate records
* Delayed updates
* Schema changes
* Timestamp anomalies
* Currency inconsistencies
* Unit inconsistencies

Data quality should be treated as an ongoing process.

---

# 53. Provider Schema Changes

External providers may change their APIs.

Provider adapters should isolate these changes.

If a provider changes:

```text
Provider API
      ↓
Adapter
      ↓
Canonical QuantMind Model
```

the rest of the system should ideally remain unaffected.

---

# 54. Data Versioning

Where important, QuantMind should track changes to:

* Provider schemas
* Canonical schemas
* Data transformations
* Calculation methods
* Evidence extraction
* AI interpretation pipelines

Major changes should be recorded in `Decision-Log.md`.

---

# 55. Data Retention

Retention requirements should be determined by:

* Provider license
* Product requirements
* User requirements
* Regulatory requirements
* Storage cost
* Research reproducibility

No universal retention period should be assumed before these constraints are evaluated.

---

# 56. Privacy

QuantMind should minimize collection of unnecessary personal information.

Financial research data should remain separate from sensitive personal financial data until the Personal Finance phase is intentionally implemented.

The MVP should not collect personal banking information merely because future versions may require it.

---

# 57. Personal Finance Data Boundary

Personal finance data is **not an MVP data requirement**.

Future data sources may include:

* Income
* Expenses
* Bank transactions
* Investments
* Goals
* Liabilities

These require separate:

* Data architecture
* Privacy architecture
* Security model
* Consent model
* Regulatory review

They must not be casually added to the MVP.

---

# 58. Evidence Graph Future Direction

Long term, data should support a richer relationship structure:

```text
ENTITY
  │
  ├── MARKET DATA
  ├── FINANCIAL DATA
  ├── FILINGS
  ├── EARNINGS
  ├── NEWS
  ├── MACRO CONTEXT
  │
  └── EVIDENCE
          │
          ▼
        CLAIM
          │
          ▼
    CALCULATION
          │
          ▼
    INTERPRETATION
```

The MVP should establish the provenance foundations for this future system.

---

# 59. Data Source Decision Record

For every production provider, maintain a record containing:

```text
Provider Name
Category
Coverage
Markets
API / Access Method
License
Commercial Usage
Storage Permission
Redistribution Permission
Rate Limits
Pricing
Reliability
Known Limitations
Fallback Provider
Decision
Decision Date
```

---

# 60. Open Data Decisions

The following must be finalized before production implementation:

* Initial market coverage
* Initial geography
* Initial asset classes
* Market-data provider
* News provider
* Filing provider
* Financial-statement provider
* Macro-data provider
* Historical data depth
* Data refresh frequency
* Data storage policy
* Licensing requirements
* Provider fallback strategy
* Production data budget

These decisions should be documented rather than assumed.

---

# 61. Data Quality Acceptance Criteria

A data source should not be considered production-ready unless:

* Required coverage exists.
* Data can be retrieved reliably.
* Important fields are validated.
* Timestamps are available where required.
* Units and currencies are identifiable.
* Source attribution is possible.
* Licensing is understood.
* Provider limitations are documented.
* Failure behavior is defined.

---

# 62. Final Data Architecture Principle

QuantMind should treat financial data as a chain of provenance:

```text
SOURCE
  ↓
RAW DATA
  ↓
VALIDATION
  ↓
CANONICAL DATA
  ↓
EVIDENCE
  ↓
CALCULATION
  ↓
ANALYSIS
  ↓
INTELLIGENCE
```

At every stage, the system should preserve enough context to answer:

> **“Where did this information come from, what happened to it, and why should the user trust this result?”**

---

# 63. Final Rule

> **Never sacrifice data provenance for convenience.**
>
> **Never treat public availability as automatic permission for commercial use.**
>
> **Never silently mix incompatible financial data.**
>
> **Never fabricate missing information.**
>
> **Build QuantMind's data foundation so that every important financial insight can ultimately be traced back to evidence.**
