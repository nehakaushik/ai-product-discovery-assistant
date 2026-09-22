# Product Decision Log

This document captures key product and technical decisions made while designing and prototyping the AI Product Discovery Assistant.

The goal is not only to document what was built, but why particular decisions were made, what tradeoffs were considered, and what limitations remain.

---

## Decision 1: Use RAG instead of relying only on an LLM

### Problem

Product discovery information comes from customer interviews, notes, and other research sources. A general-purpose LLM does not automatically have access to this project-specific information.

### Decision

Use Retrieval-Augmented Generation (RAG) so relevant discovery evidence is retrieved before the language model generates an answer.

### Why

This allows answers to be based on project-specific research rather than relying only on the model's existing knowledge.

It also makes it possible to show the evidence behind an answer.

### Tradeoff

RAG introduces additional components such as chunking, embeddings, retrieval, relevance thresholds, and evidence mapping.

---

## Decision 2: Make evidence visible to the PM

### Problem

An AI-generated answer alone is difficult for a PM to trust when making product decisions.

### Decision

Return the source, location, exact evidence text, and retrieval score alongside the generated answer.

### Why

The PM should be able to inspect the underlying customer evidence and distinguish source material from AI interpretation.

The AI assists with synthesis; it does not replace product judgment.

---

## Decision 3: Do not trust Top-K retrieval by itself

### Problem

Vector search always returns the closest results even when none of them are actually relevant.

During testing, a pricing question retrieved unrelated onboarding content simply because those chunks were the nearest available matches.

### Decision

Add an experimental relevance threshold in addition to Top-K retrieval.

### Why

If no retrieved chunk meets the threshold, the system should abstain rather than send irrelevant evidence to the language model.

### Limitation

The current threshold was selected using a very small prototype dataset. It is not a production-quality threshold and would require validation against a larger representative evaluation set.

---

## Decision 4: Evaluate retrieval and generation separately

### Problem

A bad final answer does not automatically mean retrieval failed.

During testing, the correct evidence was sometimes retrieved while the language model still produced an incorrect or unhelpful answer.

### Decision

Maintain separate retrieval and generation evaluations.

### Why

This makes failures easier to diagnose:

- Retrieval failure: the correct evidence was not found.
- Generation failure: useful evidence was found, but the model produced a poor answer.
- Validation failure: an answer was generated but did not meet the rules required to show it to the user.

This separation also makes experiments easier to evaluate without changing multiple system components at once.

---

## Decision 5: Select the prototype model using evals, not model size

### Problem

Different language models produced different results when given the same evidence and questions.

### Experiment

A small generation evaluation set was used to compare local models.

| Model | Eval Result |
|---|---:|
| FLAN-T5-base | 2/4 |
| Qwen2.5-0.5B-Instruct | 3/4 |
| Qwen2.5-1.5B-Instruct | 2/4 |

### Decision

Use Qwen2.5-0.5B-Instruct for the current local prototype.

### Why

It provided the best quality/resource tradeoff among the models tested and can run locally without paid API usage.

### Limitation

The evaluation contains only four cases. These results support a prototype decision but are not evidence that one model is generally superior to another.

For production, model evaluation would require a larger representative dataset and comparison of quality, groundedness, latency, cost, privacy, reliability, and enterprise requirements.

---

## Decision 6: Add validation after generation

### Problem

Retrieving relevant evidence does not guarantee that the language model will produce a useful answer.

For example, the system retrieved evidence explaining an account-connection problem but generated only:

> Yes

for the question:

> What problem did the customer have during setup?

### Decision

Add a post-generation validation layer before returning an answer to the user.

Current pipeline:

Question → Retrieval → Relevance Filter → Generation → Validation → Response

### Why

This provides another guardrail between model output and the user.

For the prototype, deterministic rules can catch obvious failures such as a bare "Yes" or "No" response to a descriptive "What", "Why", or "How" question.

### Limitation

The current validator does not prove that an answer is factually correct or fully grounded in the evidence.

A production system would require stronger validation for answer relevance, groundedness, contradictions, unsupported claims, and citation support.

---

## Product Principle

The AI Product Discovery Assistant should optimize for trustworthy assistance rather than maximum answer rate.

When evidence is insufficient or an answer cannot be validated, the system should make uncertainty visible rather than present an unsupported answer as fact.