# QuantMind AI — Application Flow

> **Status:** Phase 0 — Foundation / Pre-MVP
> **Document Type:** User + System Flow Specification
> **Version:** 1.0
> **Last Updated:** 2026-09-22
> **Product:** QuantMind AI
> **Tagline:** Think Beyond the Market.

---

# 1. Document Purpose

This document defines how users and system components interact throughout the QuantMind AI MVP.

It describes:

* User journeys
* Application navigation
* Research flow
* Data retrieval flow
* Evidence flow
* Quantitative analysis flow
* AI reasoning flow
* Verification flow
* Error handling
* Loading states
* Company research flow
* Comparison flow
* Research history
* Authentication flow where required

The core objective is to ensure that the product experience follows the same intelligence architecture defined in:

```text
brain.md
docs/PRD.md
docs/MVP-Scope.md
docs/TRD.md
docs/Data-Sources.md
docs/UI-UX-Design-Brief.md
```

---

# 2. Core Product Flow

The central QuantMind interaction is:

```text
User
 ↓
Question
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

This is the primary MVP flow.

---

# 3. Application Entry Flow

```text
User opens QuantMind
        ↓
Authentication required?
   ┌────┴────┐
   │         │
  Yes        No
   │         │
Login       Research Home
   │
   ↓
Research Home
```

Authentication requirements should remain minimal during MVP.

---

# 4. Research Home

The Research Home is the primary entry point.

Conceptually:

```text
┌───────────────────────────────────────────────┐
│ QuantMind                                     │
│                                               │
│        What do you want to understand?        │
│                                               │
│ [ Ask a financial research question... ]      │
│                                               │
│ Recent Research                               │
│                                               │
└───────────────────────────────────────────────┘
```

Primary action:

> Ask a financial research question.

---

# 5. User Research Flow

```text
User enters question
        ↓
Submit
        ↓
Validate input
        ↓
Understand intent
        ↓
Resolve entities
        ↓
Create research task
        ↓
Retrieve required data
        ↓
Retrieve evidence
        ↓
Perform calculations
        ↓
Generate analysis
        ↓
Verify response
        ↓
Display research
```

---

# 6. Input Validation

Before processing:

```text
User Input
   ↓
Is input valid?
 ┌─┴─────────┐
No           Yes
│             │
Error         Continue
```

Possible validation conditions:

* Empty request
* Excessively malformed input
* Unsupported request
* Security-related input
* Ambiguous entity

The system should provide a useful explanation where possible.

---

# 7. Intent Understanding Flow

The system determines what the user is trying to accomplish.

Example:

```text
"Why is NVIDIA moving today?"
        ↓
WHY_MOVING
```

```text
"Analyze Reliance."
        ↓
COMPANY_RESEARCH
```

```text
"Compare Apple and Microsoft."
        ↓
FINANCIAL_COMPARISON
```

```text
"How did Tesla revenue change?"
        ↓
METRIC / HISTORICAL_ANALYSIS
```

Unknown intent:

```text
Unknown / Ambiguous
        ↓
Clarify if necessary
```

---

# 8. Entity Resolution Flow

```text
User Question
      ↓
Entity Extraction
      ↓
Entity Search
      ↓
Potential Matches
      ↓
Confidence / Exactness Check
      ↓
Resolved Entity
```

Example:

```text
"NVIDIA"
   ↓
NVIDIA Corporation
   ↓
NVDA
   ↓
Relevant exchange / market
```

If multiple entities could match:

```text
Ambiguous
   ↓
Ask user to clarify
```

The system must not silently select an unrelated entity.

---

# 9. Task Planning Flow

After intent and entity resolution:

```text
Intent
+
Entity
+
Time Context
+
User Question
        ↓
Research Task
```

Example:

```text
Question:
Why is NVIDIA moving today?

Task:
1. Resolve NVDA
2. Determine current market period
3. Retrieve price movement
4. Retrieve relevant recent events
5. Retrieve relevant news
6. Retrieve supporting evidence
7. Calculate movement
8. Analyze possible drivers
9. Verify claims
10. Compose response
```

---

# 10. Retrieval Flow

```text
Research Task
      ↓
Determine required data
      ↓
Query Data Providers
      ↓
Normalize Results
      ↓
Validate Results
      ↓
Rank Results
      ↓
Return Relevant Data
```

The system should retrieve only information relevant to the research task.

---

# 11. Evidence Retrieval Flow

```text
Retrieved Information
        ↓
Identify Evidence
        ↓
Extract Relevant Context
        ↓
Attach Source Metadata
        ↓
Attach Timestamp
        ↓
Create Evidence Records
        ↓
Pass to Analysis
```

Evidence must remain traceable to its source.

---

# 12. Quantitative Analysis Flow

When quantitative analysis is required:

```text
Validated Data
      ↓
Determine Calculation
      ↓
Validate Inputs
      ↓
Quant Engine
      ↓
Calculate
      ↓
Validate Result
      ↓
Store Calculation Context
      ↓
Return Result
```

Example:

```text
Revenue 2024
+
Revenue 2025
        ↓
Revenue Growth
        ↓
Validated Result
```

---

# 13. AI Reasoning Flow

The AI receives structured context:

```text
User Question
+
Intent
+
Entity
+
Retrieved Data
+
Evidence
+
Quantitative Results
+
Temporal Context
+
Known Limitations
        ↓
AI Reasoning
        ↓
Structured Research Response
```

The AI should not independently invent financial facts outside the supplied evidence and data context.

---

# 14. Verification Flow

Before displaying the response:

```text
AI Response
      ↓
Verification
      │
      ├── Entity Check
      ├── Source Check
      ├── Citation Check
      ├── Numerical Check
      ├── Temporal Check
      └── Unsupported Claim Check
      ↓
Verified Response
```

If verification identifies a material issue:

```text
Verification Failure
        ↓
Regenerate / Correct / Remove Unsupported Claim
        ↓
Verify Again
```

If reliable correction is impossible:

```text
Return partial answer
+
Explain limitation
```

---

# 15. Response Composition

The system should compose responses using the appropriate structure.

Typical flow:

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

Not every query requires every section.

---

# 16. Research Result State

The frontend should receive a structured research result.

Conceptually:

```text
Research Result
├── Question
├── Entity
├── Answer
├── Context
├── Evidence
├── Quant Analysis
├── Interpretation
├── Risks
├── Limitations
└── Sources
```

---

# 17. Research Result UI Flow

```text
Research Processing
        ↓
Research Result
        ↓
User reads Direct Answer
        ↓
User explores Evidence
        ↓
User reviews Quant Analysis
        ↓
User inspects Sources
        ↓
User may continue research
```

---

# 18. Evidence Interaction

When the user selects evidence:

```text
Evidence Preview
      ↓
Expand
      ↓
Source Details
      ↓
Relevant Context
      ↓
Publication Date
      ↓
Original Source
```

The user should be able to return to the research response without losing context.

---

# 19. Source Interaction

Selecting a source should expose:

```text
Source Name
Document / Article
Publication Date
Source Type
Relevant Evidence
Original Source Reference
```

The interface should distinguish the source itself from QuantMind's interpretation.

---

# 20. Follow-Up Research

After receiving an answer, users should be able to continue researching.

Example:

```text
User:
Analyze NVIDIA.

        ↓

QuantMind:
Research result.

        ↓

User:
Compare it with AMD.

        ↓

New Research Task
```

The system may use relevant existing context while ensuring the new request is correctly interpreted.

---

# 21. Follow-Up Context

Follow-up queries may depend on previous context.

Example:

```text
User:
Why is NVIDIA moving today?

Assistant:
...

User:
Is this movement larger than usual?
```

The system should understand that:

```text
"This movement"
```

refers to the relevant NVIDIA movement from the previous interaction.

If the reference is ambiguous, clarification should be requested.

---

# 22. “Why Is It Moving?” Flow

```text
User asks:
"Why is NVIDIA moving today?"
        ↓
Resolve NVDA
        ↓
Determine relevant time window
        ↓
Retrieve market movement
        ↓
Calculate movement
        ↓
Retrieve recent news
        ↓
Retrieve corporate / market events
        ↓
Retrieve supporting evidence
        ↓
Evaluate possible drivers
        ↓
Separate confirmed facts from interpretation
        ↓
Communicate uncertainty
        ↓
Return explanation + evidence
```

---

# 23. Movement Analysis Response

Possible structure:

```text
Why NVIDIA Is Moving

Observed movement
↓
Key recent developments
↓
Evidence supporting each development
↓
Possible relationship to the movement
↓
What cannot be confirmed
↓
Sources
```

The interface must not imply that temporal correlation automatically proves causation.

---

# 24. Company Research Flow

```text
User searches company
        ↓
Entity Resolution
        ↓
Company Research Page
        ↓
Overview
        ↓
Market Context
        ↓
Financials
        ↓
Recent Developments
        ↓
Earnings
        ↓
Quantitative Analysis
        ↓
Risks / Watchpoints
        ↓
Evidence / Sources
```

Sections should only appear when meaningful data is available.

---

# 25. Company Search Flow

```text
Search Input
      ↓
Entity Search
      ↓
Matching Entities
      ↓
Select Entity
      ↓
Company Research
```

Search results should display enough information to disambiguate similar entities.

---

# 26. Comparison Flow

```text
User asks for comparison
        ↓
Identify Entity A
        ↓
Identify Entity B
        ↓
Determine comparable metrics
        ↓
Determine compatible period
        ↓
Retrieve data
        ↓
Normalize units / currencies
        ↓
Calculate metrics
        ↓
Generate comparison
        ↓
Show evidence
```

---

# 27. Comparison Validation

Before comparing values:

```text
Metric Definitions Compatible?
        ↓
Period Compatible?
        ↓
Currency Compatible?
        ↓
Units Compatible?
        ↓
Source Quality Acceptable?
```

If not:

```text
Do not silently compare.
Explain limitation or normalize appropriately.
```

---

# 28. Historical Research Flow

```text
User asks historical question
        ↓
Identify target date / period
        ↓
Identify information available at that point
        ↓
Filter future information
        ↓
Retrieve historical data
        ↓
Perform calculations
        ↓
Generate analysis
        ↓
Verify temporal correctness
        ↓
Return result
```

---

# 29. Historical Integrity

For historical analysis:

```text
Analysis Date
        ↓
Information Available By Date
        ↓
Allowed Dataset
        ↓
Calculation
```

Future information must not leak into historical analysis.

---

# 30. Missing Data Flow

```text
Required Data
      ↓
Available?
 ┌────┴────┐
Yes        No
 │          │
Continue    Identify missing data
            ↓
       Can analysis continue?
          ┌──┴──┐
         Yes    No
          │      │
     Partial      Explain
      result      limitation
```

The system must never convert missing data into fabricated values.

---

# 31. Conflicting Data Flow

```text
Source A
   +
Source B
   ↓
Different values
   ↓
Compare:
- Date
- Definition
- Period
- Revision
- Source authority
   ↓
Resolved?
 ┌──┴──┐
Yes    No
 │      │
Use     Show conflict
resolved + limitation
value
```

---

# 32. Provider Failure Flow

```text
Provider Request
      ↓
Success?
 ┌────┴─────┐
Yes         No
 │           │
Continue     Is retryable?
             ├── Yes → Retry
             └── No
                  ↓
              Fallback?
             ┌────┴────┐
            Yes        No
             │          │
          Fallback    Graceful
                      degradation
```

---

# 33. AI Provider Failure

```text
AI Request
    ↓
Success?
 ┌──┴──┐
Yes    No
 │      │
Return  Retry / fallback
        ↓
     Still failing?
        ↓
   Inform user clearly
```

No fabricated answer should be generated to hide an AI failure.

---

# 34. Loading Flow

During research:

```text
User submits
      ↓
Understanding question...
      ↓
Finding relevant data...
      ↓
Retrieving evidence...
      ↓
Running analysis...
      ↓
Verifying research...
      ↓
Preparing answer...
      ↓
Result
```

Loading states should reflect actual system operations where possible.

---

# 35. Partial Result Flow

If some components succeed and others fail:

```text
Market Data ✓
News ✓
Filings ✕
Quant Analysis ✓
        ↓
Partial Research
        ↓
Clearly identify unavailable component
        ↓
Return useful result where reliable
```

The system should prefer a transparent partial result over fabricated completeness.

---

# 36. Error Flow

```text
Error
 ↓
Classify
 ↓
User-safe message
 ↓
Explain relevant limitation
 ↓
Retry option where appropriate
 ↓
Return to Research
```

Internal technical details should not be exposed unnecessarily.

---

# 37. Authentication Flow

Where authentication is required:

```text
Open QuantMind
      ↓
Authenticated?
 ┌────┴────┐
Yes        No
 │          │
Research   Login
           ↓
        Authenticate
           ↓
        Research
```

Authentication should not unnecessarily interrupt research.

---

# 38. Research History Flow

```text
Research completed
      ↓
Save eligible research record
      ↓
Research History
      ↓
User selects previous research
      ↓
Open research result
```

Storage behavior must respect user privacy and product configuration.

---

# 39. Research History Search

```text
User opens history
      ↓
Search / Filter
      ↓
Matching research
      ↓
Open research
```

MVP history should remain simple.

---

# 40. Navigation Flow

Primary application navigation:

```text
QuantMind
│
├── Research
│
├── Companies / Entities
│
├── Research History
│
└── Settings
```

The MVP should not include navigation for deferred modules.

---

# 41. Settings Flow

```text
Settings
│
├── Account
├── Preferences
├── Data / Privacy
└── Sign Out
```

Additional settings may be added as required.

---

# 42. Research Continuation

At the end of research, the user should have clear paths to:

```text
Ask Follow-up
Explore Evidence
Open Company
Compare Entity
Start New Research
```

The product should encourage exploration without becoming a social feed.

---

# 43. Frontend / Backend Boundary

The frontend is responsible for:

```text
Presentation
Interaction
State
Navigation
```

The backend is responsible for:

```text
Financial Data
Retrieval
Evidence
Quantitative Calculations
AI Orchestration
Verification
Persistence
```

Core financial logic must not depend on frontend implementation.

---

# 44. System Flow

The complete backend research pipeline is:

```text
API Request
    ↓
Input Validation
    ↓
Intent Classification
    ↓
Entity Resolution
    ↓
Task Planning
    ↓
Data Retrieval
    ↓
Data Validation
    ↓
Evidence Retrieval
    ↓
Quant Engine
    ↓
AI Reasoning
    ↓
Verification
    ↓
Response Composition
    ↓
Persistence
    ↓
API Response
```

---

# 45. Evidence Flow

```text
External Source
      ↓
Provider Adapter
      ↓
Raw / Canonical Data
      ↓
Validation
      ↓
Evidence Extraction
      ↓
Evidence Record
      ↓
Research Task
      ↓
AI Context
      ↓
Response
      ↓
Source Display
```

---

# 46. Quant Flow

```text
Data Source
     ↓
Validated Data
     ↓
Calculation Request
     ↓
Quant Engine
     ↓
Calculation Result
     ↓
Validation
     ↓
Research Context
     ↓
AI Explanation
```

---

# 47. AI Flow

```text
User Query
    ↓
Structured Context
    ├── Intent
    ├── Entity
    ├── Data
    ├── Evidence
    ├── Quant Results
    ├── Time Context
    └── Limitations
             ↓
          AI Model
             ↓
     Structured Response
             ↓
        Verification
             ↓
        Final Response
```

---

# 48. Verification Flow

Verification should occur before final presentation.

```text
Generated Response
      ↓
Claim Extraction / Inspection
      ↓
Evidence Match
      ↓
Numerical Match
      ↓
Temporal Match
      ↓
Source Match
      ↓
Validation
```

---

# 49. User Trust Flow

The desired user experience is:

```text
User sees insight
      ↓
User sees supporting evidence
      ↓
User inspects source
      ↓
User understands calculation
      ↓
User understands uncertainty
      ↓
User forms their own understanding
```

QuantMind should facilitate informed user judgment rather than require blind trust.

---

# 50. Security Flow

Sensitive operations should follow:

```text
Request
 ↓
Authentication
 ↓
Authorization
 ↓
Input Validation
 ↓
Business Logic
 ↓
Data Access
 ↓
Response Validation
 ↓
Response
```

Secrets should never pass through the frontend unnecessarily.

---

# 51. Data Privacy Flow

```text
User Data
   ↓
Collect only what is required
   ↓
Secure storage
   ↓
Controlled access
   ↓
Use for intended product purpose
```

Personal financial data is outside the MVP unless explicitly introduced through a separately approved scope change.

---

# 52. Performance Flow

The system should avoid unnecessary sequential operations.

Where operations are independent:

```text
                    ┌→ Market Data
Research Task ──────┼→ News
                    ├→ Filings
                    └→ Entity Data
```

Results can then be combined for analysis.

Parallelism should not compromise provider limits, correctness, or evidence ordering.

---

# 53. Research Cancellation

If supported by the implementation, a user may cancel an active research request.

```text
Research Running
      ↓
User Cancels
      ↓
Cancel / Stop expensive work where possible
      ↓
Return to Research
```

Cancellation is an optimization, not a core MVP requirement.

---

# 54. Mobile Flow

On mobile:

```text
Open
 ↓
Research Input
 ↓
Research Processing
 ↓
Direct Answer
 ↓
Evidence
 ↓
Quant Analysis
 ↓
Sources
```

The mobile experience should prioritize the most important information first.

---

# 55. Accessibility Flow

Users must be able to:

```text
Navigate
 ↓
Focus
 ↓
Read
 ↓
Interact
 ↓
Inspect Evidence
 ↓
Understand Results
```

using supported accessibility mechanisms.

Color must not be required to understand important information.

---

# 56. Flow States

Every major research flow should support:

```text
Initial
Loading
Success
Partial Success
Empty
Error
Retry
```

The application must not assume that every external dependency succeeds.

---

# 57. MVP Primary User Journey

The ideal first-time journey:

```text
Landing / Login
      ↓
Research Home
      ↓
Ask:
"Analyze NVIDIA."
      ↓
Research Processing
      ↓
Direct Answer
      ↓
Financial Context
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
      ↓
User asks follow-up
```

This journey represents the product's core value loop.

---

# 58. MVP Success Flow

A successful MVP interaction should demonstrate:

```text
Question
   ↓
Reliable Information
   ↓
Relevant Evidence
   ↓
Correct Calculation
   ↓
Grounded AI Reasoning
   ↓
Transparent Explanation
```

If any of these steps materially fails, the system should expose the limitation rather than hide it.

---

# 59. Future Flow Compatibility

The architecture should eventually support:

```text
Research
   ↓
Quant Research
   ↓
Strategy Builder
   ↓
Backtesting
   ↓
Portfolio Intelligence
   ↓
Personal Finance
   ↓
Agent Ecosystem
```

These are future extensions.

They should not be implemented as part of the MVP flow.

---

# 60. Final Application Flow

The complete QuantMind MVP can be represented as:

```text
                         USER
                           │
                           ▼
                  ┌─────────────────┐
                  │ Research Home   │
                  └────────┬────────┘
                           │
                           ▼
                     User Question
                           │
                           ▼
                  Intent Understanding
                           │
                           ▼
                    Entity Resolution
                           │
                           ▼
                     Task Planning
                           │
                           ▼
                 ┌─────────┴─────────┐
                 │                   │
                 ▼                   ▼
           Data Retrieval      Evidence Retrieval
                 │                   │
                 └─────────┬─────────┘
                           ▼
                    Data Validation
                           │
                           ▼
                     Quant Engine
                           │
                           ▼
                     AI Reasoning
                           │
                           ▼
                      Verification
                           │
                           ▼
                  Response Composition
                           │
                           ▼
                 ┌─────────┴─────────┐
                 │                   │
                 ▼                   ▼
              Answer             Evidence
                 │                   │
                 └─────────┬─────────┘
                           ▼
                      User Research
                           │
                           ▼
                    Follow-up / New
                       Research
```

---

# 61. Final Principle

> **The application flow must mirror the intelligence architecture.**

QuantMind should never become:

```text
Question → LLM → Answer
```

It should remain:

```text
Question
→ Data
→ Evidence
→ Quantitative Analysis
→ Reasoning
→ Verification
→ Explainable Intelligence
```

That flow is the foundation of the QuantMind AI MVP.
