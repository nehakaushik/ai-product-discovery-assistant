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

    return {
        "status": "answered",
        "question": request.question,
        "sources": relevant_chunks
    }