import torch
from transformers import AutoTokenizer, AutoModel
from backend.sample_data import discovery_data


model_name = "sentence-transformers/all-MiniLM-L6-v2"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)


# Create embeddings for our discovery chunks once
chunk_texts = [chunk["text"] for chunk in discovery_data]

encoded_chunks = tokenizer(
    chunk_texts,
    padding=True,
    truncation=True,
    return_tensors="pt"
)

with torch.no_grad():
    chunk_output = model(**encoded_chunks)

chunk_embeddings = chunk_output.last_hidden_state.mean(dim=1)


def retrieve_evidence(question, top_k=3, relevance_threshold=0.25):

    encoded_question = tokenizer(
        question,
        return_tensors="pt"
    )

    with torch.no_grad():
        question_output = model(**encoded_question)

    question_embedding = question_output.last_hidden_state.mean(dim=1)

    similarities = torch.nn.functional.cosine_similarity(
        question_embedding,
        chunk_embeddings
    )

    top_results = torch.topk(similarities, k=top_k)

    relevant_chunks = []

    for index, score in zip(top_results.indices, top_results.values):

        if score.item() >= relevance_threshold:

            chunk = discovery_data[index.item()]

            relevant_chunks.append({
                "source": chunk["source"],
                "location": chunk["location"],
                "text": chunk["text"],
                "similarity_score": round(score.item(), 3)
            })

    return relevant_chunks