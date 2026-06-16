import torch

from transformers import AutoTokenizer
from transformers import AutoModelForCausalLM

MODEL_NAME = "Qwen/Qwen3-8B"

print("Loading tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)

print("Loading Qwen on AMD MI300X...")

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.bfloat16,
    device_map="auto"
)

print("Qwen model loaded successfully")

def ask_llm(prompt):

    inputs = tokenizer(
        prompt,
        return_tensors="pt"
    ).to(model.device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=250,
        temperature=0.3,
        do_sample=True
    )

    response = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    return response
