# Data Model

This document describes the core application data required for the AI Product Discovery Assistant.

## Projects

| Field | Purpose |
|---|---|
| project_id | Unique identifier for the project |
| project_name | Name displayed to the PM |
| created_by | User who created the project |
| created_at | When the project was created |
| status | Whether the project is active, archived, etc. |
## Documents

| Field | Purpose |
|---|---|
| document_id | Unique identifier for the document |
| project_id | Project the document belongs to |
| document_name | Name of the uploaded document |
| source_type | Source such as interview, workshop notes, PDF, DOCX, or TXT |
| processing_status | Current processing state: PROCESSING, READY, or FAILED |
| version | Current version of the document |
| uploaded_by | User who uploaded the document |
| uploaded_at | When the document was uploaded |
| source_reference | Reference to the original source or file |
## Chunks

| Field | Purpose |
|---|---|
| chunk_id | Unique identifier for the chunk |
| document_id | Document the chunk came from |
| chunk_text | Text contained in the chunk |
| source_location | Location in the original document, such as page, paragraph, or section |
| version | Document version the chunk belongs to |
| created_at | When the chunk was created |
## Questions and Answers

| Field | Purpose |
|---|---|
| question_id | Unique identifier for the question |
| project_id | Project the question belongs to |
| asked_by | User who asked the question |
| question_text | Question entered by the PM |
| answer_text | AI-generated answer |
| answer_status | ANSWERED or INSUFFICIENT_EVIDENCE |
| created_at | When the question was asked |
| response_time_ms | Time taken to generate the response |

## Answer Evidence

| Field | Purpose |
|---|---|
| evidence_id | Unique identifier for the evidence record |
| question_id | Question/answer this evidence supports |
| chunk_id | Retrieved chunk used as supporting evidence |
| validation_status | SUPPORTED, NEEDS_RESEARCH, or NOT_SUPPORTED |
| validated_by | User who reviewed the evidence |
| validated_at | When the evidence was reviewed |

## Project Access

| Field | Purpose |
|---|---|
| project_id | Project the access rule applies to |
| user_id | User who has access to the project |
| role | User's role within the project |
| access_level | Permission level, such as VIEWER, EDITOR, or OWNER |
| granted_at | When access was granted |

## Project Access

| Field | Purpose |
|---|---|
| project_id | Project the access rule applies to |
| user_id | User who has access to the project |
| role | User's role within the project |
| access_level | Permission level, such as VIEWER, EDITOR, or OWNER |
| granted_at | When access was granted |