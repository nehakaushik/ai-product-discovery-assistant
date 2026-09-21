# Failure States & Observability

The AI Product Discovery Assistant must distinguish between a lack of supporting evidence and a technical system failure.

## Core Failure States

| Failure | User Experience | System Behavior |
|---|---|---|
| Insufficient evidence | Tell the PM there is not enough information in the available research | Do not generate an unsupported answer |
| Document processing failure | Tell the PM the document could not be processed | Mark document as FAILED and allow retry |
| Retrieval failure | Tell the PM the discovery material could not be searched right now | Do not call the LLM with incomplete retrieval |
| LLM failure | Tell the PM the answer could not be generated right now | Preserve the request and allow retry |
| Citation failure | Do not present unsupported citations as valid evidence | Flag the response for citation/evidence failure |
| Unauthorized access | Tell the user they do not have access | Do not retrieve or send restricted content to the LLM |

## Observability

Each Ask AI request should be traceable across the major stages:

Authorization → Retrieval → LLM Generation → Citation Mapping → Response

Useful operational signals include:

- request ID
- project ID
- processing stage
- success/failure status
- error type
- response time
- number of chunks retrieved
- LLM/model used
- token usage and estimated cost

Sensitive customer content should not be unnecessarily stored in logs.