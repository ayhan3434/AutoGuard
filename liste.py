import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.environ.get("NVIDIA_API_KEY", ""),
)

c = client.chat.completions.create(
    model="nvidia/nemotron-3.5-lightning-30b-a3b",
    messages=[
        {"role": "system", "content": "detailed thinking off"},
        {"role": "user", "content": "Merhaba de"},
    ],
    max_tokens=1000,
)

msg = c.choices[0].message
print("=== content ===")
print(repr(msg.content))
print("=== reasoning_content ===")
print(repr(getattr(msg, "reasoning_content", "YOK")))