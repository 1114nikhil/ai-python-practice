import os
import sys
from anthropic import Anthropic
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()
client=Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
MODEL="claude-haiku-4-5-20251001"

prompt = "Give me one creative name for a coffee shop. Reply with just the name, nothing else."

def ask(temperature:float)->str:
    response = client.messages.create(
    model=MODEL,
    max_tokens=20,
    extra_body={"temperature": temperature},
    messages=[{"role": "user", "content": prompt}],
)
    return response.content[0].text.strip()

for temp in [0.0,0.0,1.0,1.0]:
    print(f"temperature={temp}: {ask(temp)}")