# AI Product Discovery Assistant

> A RAG-powered product concept that helps Product Managers turn unstructured customer discovery material into structured, source-backed product insights.

## The Problem

Product Managers collect valuable information across customer interviews, discovery workshops, stakeholder conversations, and research notes.

The challenge isn't simply collecting this information. It's turning large amounts of unstructured discovery material into useful product insights without losing important context or spending hours manually reviewing notes.

Existing AI summarization can reduce that effort, but for product decisions, a summary alone isn't enough. PMs need to understand:

- What problems are appearing repeatedly?
- What do users actually need?
- What decisions have been made?
- What questions remain unanswered?
- What potential requirements are emerging?
- What evidence supports each AI-generated insight?

This creates an additional trust problem: if AI generates an insight, the PM needs a quick way to verify that the conclusion is actually supported by the original research.

## Target User

**Primary user:** Product Manager / Product Owner / Business Analyst
## MVP Scope

The MVP focuses on a simple discovery workflow:

1. Upload discovery material such as customer interviews, workshop notes, or stakeholder interviews.
2. Process and organize the material using AI.
3. Surface structured insights across:
   - Problems
   - User Needs
   - Decisions
   - Open Questions
   - Potential Requirements
4. Ask natural-language questions across the discovery material.
5. Generate answers grounded in retrieved source evidence.
6. Show citations and the exact supporting passage so the PM can verify the AI's interpretation.
7. Allow the PM to validate an insight as:
   - Supported
   - Needs more research
   - Not supported

### Deliberately Out of Scope for the MVP

The first version does not include:

- Slack or Google Docs integrations
- Autonomous agents
- Figma integration
- Automated engineering or sprint tracking
- Large enterprise workflow integrations

These are potential future capabilities. The MVP first tests whether AI-assisted organization, retrieval, and source-backed insights provide meaningful value to Product Managers.

## Key Product Decisions

### 1. AI suggests; the PM decides

The product surfaces **Potential Requirements** rather than treating AI-generated suggestions as confirmed requirements.

This keeps the Product Manager responsible for interpreting evidence, considering business context, and making product decisions.

### 2. Evidence is part of the product experience

AI-generated insights include source citations and access to the exact supporting passage with surrounding context.

The goal is not only to generate an answer, but to make that answer traceable and verifiable.

### 3. Insufficient evidence is a valid answer

When the available discovery material does not support a conclusion, the product should say that there is insufficient evidence rather than generating a plausible-sounding answer.

For example:

> "I couldn't find enough information in the discovery material to determine which pricing model customers prefer."

### 4. Human validation creates a feedback signal

PMs can mark AI insights as **Supported**, **Needs more research**, or **Not supported**.

This feedback could later be used for evaluation and system improvement, but it should not be assumed to automatically retrain or correct the AI model.
The initial use case focuses on PMs working with customer interviews, workshop notes, stakeholder interviews, and other discovery material.

## Product Hypothesis
If Product Managers have one place to collect unstructured discovery information and AI can organize and retrieve relevant information with traceable source evidence, they can spend less time processing research while maintaining confidence in the insights used for product decisions.

## Interactive Prototype

A clickable prototype was created to explore the end-to-end product experience from uploading discovery material through AI-generated insights and source verification.

**Prototype flow:**

Upload → Processing → Discovery Overview → Ask AI → Loading → Answer → Evidence → Human Validation

[View the interactive Figma prototype](https://www.figma.com/proto/cYwOFlbz4S3V1XFJJ4C2jM/AI-Product-Discovery-Assistant-%E2%80%94-MVP?node-id=7-2&p=f&viewport=514%2C162%2C0.28&t=ACTsLhdxgJbmpg8T-1&scaling=min-zoom&content-scaling=fixed&starting-point-node-id=7%3A2&page-id=2%3A25)

### Discovery Overview
![Discovery Overview](assets/discovery-overview.png)
