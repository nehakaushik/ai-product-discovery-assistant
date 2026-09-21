from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


model_name = "google/flan-t5-base"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


def generate_answer(question, evidence):

    if not evidence:
        return None

    evidence_text = "\n".join(
        item["text"]
        for item in evidence
    )

    prompt = f"""
You answer questions using only the customer research evidence provided.

Instructions:
1. Read the question and evidence carefully.
2. If the evidence contains information that answers the question, give a short direct answer using only that information.
3. For yes/no questions, begin with Yes or No and briefly explain.
4. For questions asking what happened, what problem occurred, or what frustrated the customer, describe the relevant evidence directly.
5. Do not invent or assume information.
6. Only say "Not enough information" when the evidence truly does not contain information that answers the question.

Examples:

Question: What problem did the user have?
Evidence: The user could not reset their password.
Answer: The user could not reset their password.

Question: What pricing concerns did the user have?
Evidence: The user liked the dashboard layout.
Answer: Not enough information.

Now answer this question.

Question:
{question}

Evidence:
{evidence_text}

Answer:
"""

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True
    )

    outputs = model.generate(
        **inputs,
        max_new_tokens=100
    )

    answer = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    return answer