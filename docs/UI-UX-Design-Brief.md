# QuantMind AI — UI/UX Design Brief

> **Status:** Phase 0 — Foundation / Pre-MVP
> **Document Type:** UI/UX Design Brief
> **Version:** 1.0
> **Last Updated:** 2026-09-22
> **Product:** QuantMind AI
> **Tagline:** Think Beyond the Market.

---

# 1. Document Purpose

This document defines the visual, interaction, information-architecture, and trust principles for the QuantMind AI MVP.

The goal is to create a financial research product that feels:

* Intelligent
* Professional
* Calm
* Precise
* Evidence-driven
* Modern
* Institutional
* Easy to understand

The interface must communicate that QuantMind is a **financial intelligence system**, not a generic AI chatbot or speculative trading application.

---

# 2. Design Philosophy

QuantMind follows:

> **Quiet Intelligence.**

The interface should not constantly compete for the user's attention.

It should allow the information itself to create the visual hierarchy.

Design priorities:

```text
Clarity
  ↓
Evidence
  ↓
Context
  ↓
Insight
  ↓
Actionable Understanding
```

Avoid visual noise that does not improve understanding.

---

# 3. Product Positioning Through Design

The interface should communicate:

```text
Financial Intelligence
        +
AI Reasoning
        +
Quantitative Analysis
        +
Evidence
```

It should not visually resemble:

* Meme-stock applications
* Crypto trading dashboards
* Gambling interfaces
* Social media feeds
* Generic AI chat applications
* Overly futuristic “AI” landing pages

---

# 4. Visual Direction

Primary visual direction:

> **Light, minimal, premium product interface with a dark, data-rich research environment.**

Reference qualities:

* Apple — simplicity
* Linear — product precision
* Perplexity — research interaction
* Bloomberg — information density
* Modern institutional research platforms — credibility

These are design references, not templates to copy.

---

# 5. Visual Personality

QuantMind should feel:

### Calm

No unnecessary animation or visual noise.

### Intelligent

Complex information should be presented clearly.

### Precise

Numbers, dates, sources, and metrics should be visually structured.

### Trustworthy

Evidence should be visible rather than hidden.

### Premium

Spacing, typography, hierarchy, and interaction should feel intentional.

---

# 6. Design Principles

## 6.1 Evidence Before Decoration

Visual elements should help users understand information.

Do not add decorative UI merely because space exists.

---

## 6.2 Information Density With Hierarchy

Financial research contains significant information.

The solution is not to remove information unnecessarily.

Instead:

```text
High Priority
     ↓
Medium Priority
     ↓
Supporting Detail
     ↓
Deep Evidence
```

Users should be able to progressively explore detail.

---

## 6.3 Progressive Disclosure

Do not expose every piece of technical information immediately.

Example:

```text
Headline Insight
      ↓
Supporting Explanation
      ↓
Evidence
      ↓
Calculation
      ↓
Original Source
```

---

## 6.4 Trust Must Be Visible

The user should be able to understand why a statement exists.

Important claims should have accessible evidence.

---

## 6.5 Numbers Need Context

Never display important financial numbers without appropriate:

* Units
* Currency
* Period
* Date
* Comparison

---

# 7. Color Philosophy

The product should use a restrained palette.

Primary interface direction:

```text
Light Background
Dark Typography
Subtle Borders
Muted Secondary Text
Controlled Accent Color
```

The research/data environment may use a darker interface where it improves information density and focus.

Avoid:

* Neon gradients
* Excessive purple/blue AI aesthetics
* Bright crypto-style colors
* Excessive glassmorphism
* Decorative gradients everywhere

---

# 8. Color Semantics

Color must communicate meaning consistently.

Conceptually:

```text
Neutral
Information

Positive
Improvement / Increase

Negative
Decline / Risk

Warning
Uncertainty / Attention

Critical
System / Data Problem
```

Color should not be the only mechanism for communicating meaning.

Use:

* Labels
* Icons
* Text
* Symbols
* Context

alongside color.

---

# 9. Typography

Typography should prioritize readability.

Recommended hierarchy:

```text
Display
↓
Page Title
↓
Section Heading
↓
Subheading
↓
Body
↓
Metadata
↓
Evidence / Source Text
```

Typography should create hierarchy without requiring excessive font variation.

Avoid using many unrelated typefaces.

---

# 10. Layout Philosophy

The interface should use generous spacing while preserving research density.

Core layout principle:

```text
Structure
  ↓
Hierarchy
  ↓
Content
```

rather than:

```text
Cards
  ↓
Cards
  ↓
Cards
  ↓
More Cards
```

Not every section needs to be contained inside a card.

---

# 11. Navigation

The MVP navigation should remain simple.

Conceptual structure:

```text
QuantMind
│
├── Research
├── Companies / Entities
├── Research History
└── Settings
```

Additional long-term modules should not clutter the MVP navigation.

---

# 12. Primary Research Experience

The research interface is the core MVP experience.

Conceptually:

```text
┌──────────────────────────────────────────────┐
│ QuantMind                         Search     │
├──────────────────────────────────────────────┤
│                                              │
│       What do you want to understand?       │
│                                              │
│  [ Ask a financial research question... ]    │
│                                              │
│      Recent Research / Suggested Queries     │
│                                              │
└──────────────────────────────────────────────┘
```

The primary interaction should immediately communicate:

> **Ask a financial question. Get evidence-backed intelligence.**

---

# 13. Research Input

The input should support natural-language financial research questions.

Examples:

```text
Analyze Reliance Industries.
```

```text
Why is NVIDIA moving today?
```

```text
Compare Apple and Microsoft revenue growth.
```

```text
How has Tesla's operating margin changed?
```

The user should not need to know a proprietary command language.

---

# 14. Research Response Layout

A research response should generally follow:

```text
┌──────────────────────────────────────────────┐
│ Direct Answer                                │
├──────────────────────────────────────────────┤
│ Context                                      │
├──────────────────────────────────────────────┤
│ Key Evidence                                 │
├──────────────────────────────────────────────┤
│ Quantitative Analysis                        │
├──────────────────────────────────────────────┤
│ Interpretation                               │
├──────────────────────────────────────────────┤
│ Risks / Limitations                          │
├──────────────────────────────────────────────┤
│ Sources                                      │
└──────────────────────────────────────────────┘
```

The exact structure should adapt to the question.

---

# 15. Direct Answer

Every research response should attempt to answer the user's question early.

Do not force users to read several paragraphs before discovering the main conclusion.

Example structure:

```text
Short answer

2–4 supporting points

Detailed evidence
```

---

# 16. Evidence UI

Evidence should be visually distinct from AI interpretation.

Conceptually:

```text
CLAIM
│
├── Evidence
│   ├── Source
│   ├── Date
│   └── Relevant context
│
└── Interpretation
```

Users should be able to inspect supporting information without losing their position in the research response.

---

# 17. Source Cards

Source components may contain:

```text
Source Name
Headline / Document Title
Publication Date
Source Type
Relevant Evidence
Open Source
```

Example:

```text
────────────────────────────
SEC Filing
10-K — NVIDIA Corporation
Published: [date]

Relevant evidence...
                        
[Open source]
────────────────────────────
```

Source cards should remain compact.

---

# 18. Evidence Expansion

Evidence should support progressive disclosure.

Default:

```text
Claim
Source
Short evidence preview
```

Expanded:

```text
Claim
Source
Full relevant evidence
Publication information
Calculation relationship
Limitations
```

---

# 19. Quantitative UI

Quantitative information should prioritize readability.

Possible components:

* Metric rows
* Small charts
* Trend lines
* Comparison tables
* Percentage changes
* Historical values
* Period labels

Avoid unnecessary dashboards.

A chart should exist because it improves understanding.

---

# 20. Financial Metric Display

A metric should generally include:

```text
Metric
Value
Unit / Currency
Period
Change
Source
```

Example:

```text
Revenue
$X.XB
FY2025
+X.X% YoY
Source
```

---

# 21. Charts

Charts should be:

* Minimal
* Legible
* Correctly labeled
* Contextual
* Source-attributed where appropriate

Avoid:

* 3D charts
* Decorative charts
* Unlabeled axes
* Misleading scales
* Excessive animation

---

# 22. Company Research Page

A company page may contain:

```text
Company Header
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

The exact sections should depend on data availability.

---

# 23. Company Header

The company header should provide:

```text
Company Name
Ticker
Exchange
Sector / Industry
Current relevant market information
```

Do not overload the header with every available metric.

---

# 24. “Why Is It Moving?” UI

For movement-analysis queries, the interface should visually separate:

```text
Observed Movement
        ↓
Relevant Events
        ↓
Evidence
        ↓
Potential Drivers
        ↓
Uncertainty
```

Important distinction:

> A detected correlation or temporal association should not automatically be presented as a confirmed causal explanation.

---

# 25. Comparison UI

Company comparisons should use structured tables.

Example:

```text
                Company A     Company B
Revenue         X             Y
Growth          X%            Y%
Margin          X%            Y%
Market Cap      X             Y
```

Metrics must use compatible:

* Periods
* Units
* Definitions

---

# 26. Research History

Research history should allow users to return to previous work.

Possible display:

```text
Recent Research

Why is NVIDIA moving today?
Today

Analyze Reliance
Yesterday

Apple vs Microsoft
Sep 20
```

History should prioritize useful context rather than become a social feed.

---

# 27. Search

Search should support:

* Companies
* Tickers
* Previous research
* Relevant entities

Search results should clearly distinguish entity types.

---

# 28. Loading States

Research requests may require multiple backend operations.

Loading should communicate progress without pretending the system has completed work.

Possible states:

```text
Understanding question...
Finding relevant data...
Retrieving evidence...
Running quantitative analysis...
Verifying sources...
Preparing research...
```

These should represent actual system stages where possible.

Do not fake progress.

---

# 29. Error States

Errors should be understandable.

Example:

```text
We couldn't retrieve the required market data.

Available evidence is incomplete, so this analysis
cannot be completed reliably right now.

[Try again]
```

Avoid:

```text
Something went wrong.
```

when more useful information can be provided.

---

# 30. Missing Data UI

When data is unavailable:

```text
Data unavailable
```

should be clearly distinguished from:

```text
Data indicates zero
```

Never display an unavailable metric as zero.

---

# 31. Uncertainty UI

Uncertainty should be visible but not visually overwhelming.

Possible language:

```text
Evidence suggests...
```

```text
The available data indicates...
```

```text
This cannot be confirmed from the available sources.
```

```text
Sources disagree on...
```

The UI should avoid artificial confidence scores unless a validated methodology exists.

---

# 32. Source Freshness

Where relevant, show:

```text
Published
Updated
Retrieved
```

This is particularly important for:

* Market information
* News
* Economic data
* Corporate events

---

# 33. Trust Indicators

Trust UI may communicate:

```text
Source available
Evidence available
Calculation verified
Data timestamp
```

Avoid simplistic labels such as:

```text
AI Confidence: 97%
```

unless such a confidence methodology is properly defined and validated.

---

# 34. AI vs Evidence Visual Distinction

Users should visually understand:

```text
WHAT THE DATA SAYS
```

versus:

```text
WHAT QUANTMIND INTERPRETS
```

This distinction is foundational to the interface.

---

# 35. Interaction Principles

Interactions should be:

* Predictable
* Fast
* Reversible
* Minimal
* Keyboard-friendly where appropriate
* Accessible

Avoid unnecessary modal dialogs.

Use inline expansion when possible.

---

# 36. Motion

Motion should be subtle.

Use animation for:

* Loading
* State transitions
* Expanding evidence
* Navigation
* Data updates

Avoid:

* Constant movement
* Decorative particle effects
* Excessive parallax
* Attention-grabbing animations

---

# 37. Responsive Design

The MVP should support:

```text
Desktop
Tablet
Mobile
```

Desktop should receive primary optimization because financial research benefits from larger information surfaces.

Mobile should remain functional rather than becoming a completely separate product.

---

# 38. Accessibility

The UI should consider:

* Keyboard navigation
* Screen-reader semantics
* Sufficient contrast
* Focus states
* Readable font sizes
* Accessible charts
* Non-color-only information
* Reduced motion preferences

Accessibility should be considered during implementation, not added at the end.

---

# 39. Empty States

Empty states should guide users.

Example:

```text
No research yet.

Ask QuantMind about a company, financial metric,
market movement, or comparison.

[Start Research]
```

Avoid empty screens with no explanation.

---

# 40. Onboarding

MVP onboarding should be minimal.

The user should quickly reach:

```text
Ask a Question
```

Avoid lengthy tutorials before the user can experience the product.

---

# 41. Landing Page Relationship

The public website and product application should share the same design language but serve different purposes.

### Website

Communicates:

* Vision
* Product
* Trust
* Capabilities
* Positioning

### Application

Optimizes for:

* Research
* Evidence
* Analysis
* Speed
* Usability

---

# 42. Design System

The implementation should establish reusable primitives.

Conceptually:

```text
Typography
Colors
Spacing
Buttons
Inputs
Tables
Cards
Charts
Badges
Source Components
Evidence Components
Navigation
Modals
Tooltips
```

Do not build each screen as an isolated design.

---

# 43. Component Philosophy

Components should be:

* Reusable
* Composable
* Accessible
* Consistent
* Data-aware where necessary

Avoid overly generic components that obscure financial-specific semantics.

---

# 44. Data Visualization Rules

Every visualization should answer a question.

Before adding a chart:

```text
What does this chart help the user understand?
```

If the answer is unclear, the chart should not exist.

---

# 45. Table Design

Tables are preferred when exact values matter.

Tables should:

* Align numbers consistently
* Show units
* Show periods
* Support horizontal scrolling where necessary
* Avoid unnecessary borders
* Maintain readable density

---

# 46. Mobile Tables

On small screens:

* Prioritize important columns
* Allow horizontal scrolling
* Preserve metric labels
* Avoid shrinking text to unreadable sizes

Do not remove essential information merely to make a table fit.

---

# 47. Notifications

The MVP should avoid excessive notifications.

Notifications should exist only when they provide meaningful user value.

Real-time alerts and intelligent monitoring belong primarily to future product phases.

---

# 48. Personal Finance UI Boundary

Personal finance should not appear as a major MVP navigation item.

Future modules may eventually include:

```text
Income
Expenses
Goals
Investments
Payday Intelligence
Financial Copilot
```

These belong to later product phases.

---

# 49. Trading UI Boundary

The MVP should not visually resemble a trading terminal.

Do not build:

* Buy/sell buttons
* Order tickets
* Brokerage execution screens
* Autonomous trading controls

Research intelligence comes first.

---

# 50. Design Anti-Patterns

Avoid:

```text
❌ Neon AI aesthetics
❌ Excessive gradients
❌ Crypto-style dashboards
❌ Fake performance claims
❌ Fake testimonials
❌ Fake partner logos
❌ Excessive cards
❌ Unnecessary charts
❌ Gamification
❌ Overloaded dashboards
❌ AI confidence theater
❌ Decorative data
❌ Misleading green/red indicators
```

---

# 51. Trust Anti-Patterns

Never design the interface to imply certainty that the underlying evidence does not support.

Avoid:

```text
"Guaranteed"
"Certain"
"100% accurate"
"AI knows"
```

unless the statement is genuinely appropriate and supported.

---

# 52. Information Hierarchy

The interface should generally prioritize:

```text
1. User Question
2. Direct Answer
3. Key Evidence
4. Quantitative Context
5. Interpretation
6. Risks / Limitations
7. Detailed Evidence
8. Sources
```

This hierarchy may adapt based on query type.

---

# 53. Research Density

The product should support both:

### Quick Understanding

User can understand the main point quickly.

### Deep Research

User can continue into:

* Evidence
* Calculations
* Sources
* Historical information
* Supporting documents

The UI should support both without requiring separate products.

---

# 54. Trust Model

The visual system should reinforce:

```text
Claim
 ↓
Evidence
 ↓
Source
 ↓
Calculation
 ↓
Interpretation
```

The user should be able to move backward through this chain.

---

# 55. Design Quality Standard

Before shipping a screen, evaluate:

```text
Is the hierarchy clear?
Is the primary action obvious?
Can the user understand the data?
Can the user verify important claims?
Are units and dates clear?
Is uncertainty visible?
Is anything visually unnecessary?
Does the interface feel like financial intelligence?
```

---

# 56. MVP Screens

The initial application should focus on a limited set of screens:

```text
1. Research Home
2. Research Results
3. Company / Entity Research
4. Evidence / Source View
5. Research History
6. Search
7. Settings
8. Authentication screens if required
```

Do not create large numbers of screens merely to make the product appear complete.

---

# 57. Screen Priority

## P0

```text
Research Home
Research Results
Evidence / Sources
```

## P1

```text
Company Research
Search
Research History
```

## P2

```text
Advanced Dashboards
Portfolio Views
Strategy Builder
Personal Finance
Trading Interfaces
```

---

# 58. Design-to-Engineering Handoff

Every major UI screen should eventually define:

* Layout
* Components
* States
* Data requirements
* Loading state
* Empty state
* Error state
* Responsive behavior
* Accessibility requirements

Design should not specify only the happy path.

---

# 59. UI States

Every important component should consider:

```text
Default
Loading
Success
Empty
Error
Partial Data
Unavailable Data
Conflicting Data
Expanded
Collapsed
```

Financial applications require strong handling of partial and unavailable information.

---

# 60. Final Design Direction

QuantMind should feel like:

> **A calm, intelligent financial research environment where information is dense but understandable, and every important insight can be traced back to evidence.**

The product should not try to impress users with visual effects.

It should impress them through:

```text
Clarity
+
Depth
+
Speed
+
Evidence
+
Precision
```

---

# 61. Final Design Principle

> **Quiet interface. Deep intelligence. Visible evidence.**

The UI exists to help the user understand financial information—not to make the AI appear more impressive than the underlying evidence supports.
