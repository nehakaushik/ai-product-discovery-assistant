from backend.validator import validate_answer
from fastapi import FastAPI
from pydantic import BaseModel
from backend.retrieval import retrieve_evidence
from backend.generator import generate_answer


app = FastAPI()


class QuestionRequest(BaseModel):
    project_id: str
    question: str


@app.post("/questions")
def ask_question(request: QuestionRequest):

    relevant_chunks = retrieve_evidence(
        request.question,
        top_k=2
    )

    # Guardrail 1:
    # Retrieval could not find sufficiently relevant evidence.
    if not relevant_chunks:
        return {
            "status": "insufficient_evidence",
            "question": request.question,
            "answer": "I couldn't find enough information in the available discovery material to answer this question.",
            "sources": []
        }

    answer = generate_answer(
        request.question,
        relevant_chunks
    )

    # Guardrail 2:
    # Evidence was retrieved, but the generator could not
    # produce an answer supported by that evidence.
    if not validate_answer(request.question, answer):
        return {
            "status": "answer_validation_failed",
            "question": request.question,
            "answer": None,
            "message": "I found potentially relevant research, but couldn't generate an answer that passed validation.",
            "sources": relevant_chunks
        }

    return {
        "status": "answered",
        "question": request.question,
        "answer": answer,
        "sources": relevant_chunks
    }