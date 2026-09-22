# AI Product Discovery Assistant

## Turning fragmented customer research into traceable product evidence

Product teams collect valuable information across customer interviews, meeting transcripts, notes, and research documents. But as discovery grows, the challenge is no longer simply capturing information — it is finding the right evidence later and connecting it back to product decisions.

Product Managers often need to answer questions such as:

- What problems are customers repeatedly experiencing?
- What evidence supports this requirement?
- Which customer interview mentioned this issue?
- Are we making a product decision based on research or assumption?

General-purpose AI tools can summarize documents and answer questions, but product discovery requires more than generating a plausible response.

The answer needs to be **traceable to the underlying customer evidence**, and the product needs to behave safely when the available research cannot support a reliable answer.

## The Product Hypothesis

If Product Managers have one workspace where unstructured discovery research can be organized and queried with AI, while keeping answers connected to their original evidence, they can spend less time manually processing research and make product decisions with better context.

## Target User

The primary user is a Product Manager, Product Owner, or Business Analyst working with customer discovery information from sources such as:

- interview transcripts
- meeting notes
- research documents
- product ideas and observations

## The MVP

The MVP focuses on a narrow workflow:

**Discovery research → retrieval → AI answer → supporting evidence → human validation**

A user can ask a question about collected research. The system retrieves relevant evidence, uses that evidence to generate an answer, and preserves the connection between the answer and its source material.

The product intentionally does not attempt to autonomously make product decisions.

The AI helps organize and synthesize evidence. The Product Manager remains responsible for interpreting that evidence and deciding what to build.
## Why Not Just Use a General-Purpose AI Assistant?

A general-purpose AI assistant can summarize uploaded documents and answer questions about them. That capability alone is not enough to justify a separate product.

The opportunity for the AI Product Discovery Assistant is to build a workflow specifically around product discovery.

The product is designed around several needs that matter in this context:

- **Evidence-first answers:** AI responses remain connected to the customer research that supports them.
- **Product-specific structure:** Research can be organized into problems, user needs, assumptions, decisions, open questions, and potential requirements.
- **Persistent project knowledge:** Discovery information can accumulate within a project rather than being treated as an isolated conversation.
- **Human validation:** PMs can inspect the original evidence instead of accepting an AI-generated interpretation at face value.
- **Explicit uncertainty:** The product distinguishes between missing evidence and failure to generate a reliable answer.
- **Cross-source synthesis:** The longer-term product direction is to connect discovery information from multiple sources while preserving traceability.

The differentiation is therefore not the use of an LLM or RAG itself.

It is the product workflow around the AI:

**fragmented research → structured evidence → grounded synthesis → traceable product decisions**

## Product Scope

The first prototype deliberately focuses on the smallest workflow needed to test the core hypothesis.

### In Scope

- Ask questions about customer discovery research
- Retrieve semantically relevant evidence
- Generate answers using retrieved evidence
- Show the source material behind answers
- Handle insufficient evidence safely
- Detect basic generation failures before presenting an answer
- Allow users to review evidence when generation fails

### Out of Scope for the Current Prototype

- Autonomous product decisions
- Automatic prioritization of features
- Slack, Google Docs, or other live integrations
- Production authentication and authorization
- Persistent vector database infrastructure
- Production-scale ingestion pipelines
- Enterprise deployment and certification

These capabilities may be relevant to a future product, but they are not required to test the core value proposition.
## Product Experience

The prototype follows a simple end-to-end discovery workflow:

**Upload research → Process content → Review discovery → Ask a question → Receive an answer → Inspect supporting evidence**

The UX was designed around a key principle:

> AI output should not be treated as evidence. The underlying customer research is the evidence.

When an answer is successfully generated, the PM can inspect the source, location, exact passage, and surrounding context rather than relying only on the AI's summary.

## Designing for AI Failure

During prototype development, testing revealed that "the AI could not answer" can represent different technical situations.

The product therefore distinguishes three states:

### 1. Answered

Relevant evidence was retrieved and the generated answer passed validation.

**UX behavior:** Show the answer together with its supporting evidence.

### 2. Insufficient Evidence

Retrieval could not find research sufficiently relevant to the question.

**UX behavior:** Do not generate an unsupported answer. Explain that there is not enough evidence and suggest rephrasing the question or adding research.

### 3. Answer Validation Failed

Potentially relevant evidence was retrieved, but the generated answer did not pass validation.

**UX behavior:** Do not show the rejected AI answer. Preserve the retrieved evidence so the PM can review the original research directly.

This distinction became important during testing.

For example, when asked:

> What problem did the customer have during setup?

the retrieval system found relevant customer evidence, but the generation model returned only:

> Yes

The evidence retrieval had succeeded, but answer generation had failed.

Rather than presenting the poor answer or incorrectly telling the user that no evidence existed, the API returns:

`answer_validation_failed`

The interface can then direct the PM to the underlying evidence.

This creates a clearer relationship between the technical failure mode and the user experience.
## Technical Architecture

The prototype uses a retrieval-augmented generation (RAG) architecture to keep AI answers connected to customer research.

![Technical Architecture](assets/technical-architecture.png)

At a high level:

**Discovery sources → ingestion and processing → retrieval → grounded generation → validation → answer and evidence**

The current implementation is intentionally lightweight. It uses local sample discovery data and in-memory semantic retrieval rather than production infrastructure.

This allowed the prototype to test the highest-risk product questions first:

- Can relevant customer evidence be retrieved?
- Can the model answer using that evidence?
- What happens when retrieval fails?
- What happens when generation fails?
- How should those failures appear to the user?

Production concerns such as persistent vector storage, scalable ingestion, authentication, authorization, monitoring, and enterprise deployment remain future implementation work.
## Experiments and Evaluation

Building the prototype revealed that evaluating an AI product requires testing different parts of the system separately.

I therefore separated evaluation into two areas:

1. **Retrieval evaluation** — Did the system find the right customer evidence?
2. **Generation evaluation** — Given relevant evidence, did the model produce a useful answer?

This separation helped identify whether a poor response originated in retrieval or generation.

### Retrieval Evaluation

A small evaluation set was created containing questions with expected evidence sources, including a negative case where the research did not contain relevant information.

Examples included:

- "Did customers have trouble connecting their account?"
- "Were users unclear about what they needed to do?"
- "What pricing concerns did customers report?"

The pricing question was intentionally unsupported by the available research.

Semantic retrieval initially returns the most similar chunks even when none are genuinely relevant. To reduce this risk, I introduced an experimental relevance threshold.

If no retrieved chunk meets the threshold, the system returns:

`insufficient_evidence`

rather than sending weak evidence to the generation model.

The current threshold is a prototype decision based on a very small dataset. It would need to be calibrated using a larger, representative evaluation set before production use.

### Generation Model Evaluation

I tested several small open-source models locally against the same small generation evaluation set.

| Model | Prototype Eval Result |
|---|---:|
| FLAN-T5-base | 2/4 |
| Qwen2.5-0.5B-Instruct | 3/4 |
| Qwen2.5-1.5B-Instruct | 2/4 |

Qwen2.5-0.5B-Instruct was selected for the current prototype because it produced the best result on this limited evaluation set while remaining practical to run locally.

This is not a claim that it is generally a better model.

A production model-selection process would use a much larger representative dataset and evaluate dimensions such as answer quality, groundedness, latency, cost, privacy, reliability, and deployment constraints.

### A Bigger Model Was Not Automatically Better

One useful result was that the larger Qwen2.5-1.5B model did not outperform the smaller 0.5B model on the prototype task.

This reinforced an important product principle:

**Model selection should be driven by task-specific evaluation rather than model size alone.**

### The Evaluation Can Fail Too

The experiments also exposed a weakness in the evaluation itself.

For one test, the model generated:

> Yes. The customer encountered a connectivity issue during setup and needed assistance from support.

The answer was substantively relevant, but the initial evaluation expected the exact word "connecting" and marked the response as a failure.

The evaluation was then adjusted to accept related wording such as "connecting", "connection", or "connectivity".

This demonstrated another important lesson:

**An evaluation result is only as reliable as the evaluation criteria behind it.**

The current keyword-based generation evaluation remains intentionally simple and can still produce false positives or false negatives. More robust semantic or criteria-based evaluation would be required for a production system.
## Key Product and Technical Decisions

The prototype evolved through a series of product and technical decisions rather than treating the AI model as the entire product.

### Use RAG Instead of Asking the Model From Memory

Customer research is project-specific information that the model was not trained on.

The system therefore retrieves relevant project evidence first and provides that evidence to the generation model.

This keeps the answer grounded in the available discovery material rather than relying on the model's general knowledge.

### Make Evidence Part of the Product Experience

A generated answer alone is not sufficient for product discovery.

The PM needs to understand what customer research supports the answer.

The experience therefore preserves source information and allows the PM to inspect the underlying evidence.

### Do Not Trust Top-K Retrieval Alone

Semantic search will return the most similar results even when none are sufficiently relevant.

A relevance threshold was introduced so weak retrieval results can be rejected rather than automatically passed to the generation model.

This trades some answer coverage for greater protection against unsupported answers.

### Evaluate Retrieval and Generation Separately

A poor final response can have different causes.

If retrieval finds the wrong evidence, changing the generation model may not solve the problem. If retrieval succeeds but generation fails, changing retrieval may not solve it either.

Separating these evaluations makes failures easier to diagnose.

### Select Models Using Task-Specific Evidence

The prototype compared multiple local generation models instead of assuming that a larger model would perform better.

The selected model was based on the observed prototype evaluation results and local resource constraints, not model size alone.

### Validate Answers Before Showing Them

Even when retrieval succeeds, the generation model can still produce an unusable response.

A deterministic post-generation validation layer was therefore added to catch basic failures before an answer reaches the user.

The current validator is deliberately narrow and should not be interpreted as full factual or groundedness verification.

### Prefer Transparent Failure Over Unsupported Confidence

The system does not optimize for answering every question.

When evidence is insufficient or an answer fails validation, the product exposes that uncertainty rather than presenting an unreliable answer as if it were trustworthy.

This led to a broader product principle:

> Optimize for trustworthy assistance rather than maximum answer rate.
## Security, Privacy, and Enterprise Readiness

Customer discovery material may contain confidential business information, customer identifiers, or other sensitive data.

The current prototype does not implement production security infrastructure, but an enterprise version would need these concerns designed into the product architecture rather than added only at the end.

Key considerations include:

- **Authentication and authorization:** Only approved users should be able to access a project and its research.
- **Retrieval-level access control:** Authorization should apply before or during retrieval so the AI cannot retrieve evidence the user is not permitted to access.
- **Data minimization:** Store and send only the information required for the product workflow.
- **PII handling:** Identify and appropriately protect personal information contained in customer research.
- **Encryption:** Protect sensitive data in transit and at rest.
- **Retention and deletion:** Enterprises may require configurable policies for how long research, embeddings, generated answers, and logs are retained.
- **AI provider data policies:** Model providers would need to be evaluated for how submitted data is stored, processed, and used.
- **Auditability:** Important AI actions and access to sensitive research may need traceable records without logging unnecessary sensitive content.
- **Prompt injection and untrusted content:** Uploaded research should be treated as data, not trusted instructions to the AI.
- **Embedding lifecycle:** Deleting or restricting a source document must also be reflected in derived data such as chunks, embeddings, and indexes.

## Compliance Considerations

Enterprise requirements vary by customer, industry, geography, and the type of data being processed.

Depending on the deployment, organizations may evaluate requirements related to frameworks or regulations such as SOC 2, ISO 27001, or GDPR.

The prototype does **not** claim compliance or certification with these standards.

Instead, the product architecture should be designed so that enterprise controls such as access management, data governance, retention, auditability, and vendor assessment can be supported when required.

Security and compliance requirements would therefore be part of enterprise product discovery, not simply a technical checklist applied after the product is built.
## What the Prototype Demonstrated

The goal of this prototype was not to build a production-ready platform. It was to test the riskiest assumptions behind an evidence-first AI product discovery workflow.

The prototype demonstrated that:

- Customer research can be converted into embeddings and retrieved semantically.
- A relevance threshold can prevent obviously weak retrieval results from automatically reaching the generation model.
- Retrieved customer evidence can be passed to a local language model to generate grounded responses.
- Retrieval and generation failures can be evaluated separately.
- Different generation models can produce materially different results on the same task.
- A larger model does not necessarily produce better results for a specific product workflow.
- Simple automated evaluations can themselves be misleading and need validation.
- Post-generation checks can prevent some obviously unusable responses from reaching the user.
- Different AI failure modes can be represented as explicit API states and mapped to different UX experiences.
- Supporting evidence can remain available even when the generated answer is rejected.

The prototype therefore moved the product hypothesis beyond a Figma concept and allowed product decisions to be tested against actual AI behavior.

## Current Limitations

The implementation remains intentionally small and has several important limitations:

- Discovery research is currently represented by hardcoded sample data rather than a real upload and ingestion pipeline.
- Retrieval runs in memory rather than through a production vector database.
- The current embedding implementation is simplified and would require improvement before production use.
- `project_id` is accepted by the API but is not yet used to isolate or filter project data.
- The generation evaluation set contains only a few test cases and is not representative of production usage.
- Generation evaluation currently relies on simple phrase matching rather than robust semantic or criteria-based evaluation.
- The post-generation validator catches only a narrow class of obvious failures and does not guarantee factual correctness or groundedness.
- Authentication, authorization, persistent storage, monitoring, and production security controls are not implemented.
- Live integrations with research sources such as collaboration or document tools are not implemented.
- The prototype has not been tested with real enterprise-scale research datasets.

These limitations are important because a successful prototype result should not be interpreted as evidence of production readiness.

## What I Would Build Next

The next phase would focus on validating the product with more realistic data and strengthening the system where the prototype exposed the greatest uncertainty.

Priorities would include:

1. Replace hardcoded research with a real document ingestion workflow.
2. Introduce project-scoped storage and retrieval.
3. Expand the evaluation dataset using representative product-discovery questions and failure cases.
4. Improve retrieval evaluation and calibrate relevance thresholds using the expanded dataset.
5. Strengthen answer validation for groundedness, relevance, unsupported claims, and citation support.
6. Test the workflow with Product Managers to understand whether evidence visibility improves trust and decision-making.
7. Measure product outcomes such as time saved processing research, repeat usage, answer usefulness, evidence-review behavior, and failure rates.
8. Add enterprise capabilities such as access controls, auditability, retention policies, and appropriate data governance as customer requirements become clearer.

Only after validating the core workflow would I prioritize broader integrations and automation.

## Key Takeaway

The main lesson from the project was that building an AI product is not primarily about connecting an interface to a language model.

The difficult product questions appear around the model:

**What evidence should the model receive? How do we know retrieval worked? How do we evaluate the generated answer? What should happen when the AI fails? What does the user need to see in order to trust — or challenge — the result?**

The AI Product Discovery Assistant prototype was designed to explore those questions while keeping the Product Manager, rather than the model, responsible for the final product decision.