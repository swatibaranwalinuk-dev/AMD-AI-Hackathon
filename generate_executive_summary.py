from models.qwen_loader import ask_llm

prompt = """
Summarize the cybersecurity posture
for executive leadership.

Focus on:

1. Assets patched
2. Risk reduction
3. Business impact
4. Recommendations

Keep under 150 words.
"""

print(
    ask_llm(prompt)
)
