from fastapi import FastAPI
from pydantic import BaseModel
from backend.retrieval import retrieve_evidence

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

    if not relevant_chunks:
        return {
            "status": "insufficient_evidence",
            "question": request.question,
            "answer": "I couldn't find enough information in the available discovery material to answer this question.",
            "sources": []
        }

    return {
        "status": "answered",
        "question": request.question,
        "sources": relevant_chunks
    }