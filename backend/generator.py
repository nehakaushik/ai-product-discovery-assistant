import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


model_name = "Qwen/Qwen2.5-0.5B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)


def generate_answer(question, evidence):

    if not evidence:
        return None

    evidence_text = "\n".join(
        item["text"]
        for item in evidence
    )

    system_message = """
You answer questions about customer research using only the evidence provided.

Rules:
- Answer the question directly and briefly.
- Use only information contained in the evidence.
- Do not invent or assume facts.
- For yes/no questions, begin with Yes or No.
- If the evidence does not contain enough information to answer the question, say exactly: Not enough information.
"""

    user_message = f"""
Question:
{question}

Evidence:
{evidence_text}
"""

    messages = [
        {
            "role": "system",
            "content": system_message
        },
        {
            "role": "user",
            "content": user_message
        }
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(
        text,
        return_tensors="pt"
    )

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=100,
            do_sample=False
        )

    generated_tokens = outputs[
        0,
        inputs["input_ids"].shape[1]:
    ]

    answer = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True
    )

    return answer.strip()