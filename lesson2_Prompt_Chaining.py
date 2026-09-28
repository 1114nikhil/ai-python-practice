# Exercise 5 Prompt Chaining (Gemini version)

import os
import json
import sys
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
from google import genai

customer_email= (
    "Hi, my order #4471 never arrived, it's been 2 weeks, "
    "I'm really frustrated, please help or I want a refund."
)

load_dotenv()
client= genai.Client(api_key=os.environ['Gemini_API_Key'])
MODEL="gemini-3.6-flash"
pinned_facts = {"order_number": "4471"}
system_prompt = f"""You are a support assistant.
Known facts about this customer: {pinned_facts}"""

def ask(prompt:str,system=system_prompt)->str:
    """
        One LLM call: prompt in ,text out. All 3 chain steps reuse this
    """
    interaction= client.interactions.create(
        model=MODEL,
        system_instruction=system,
        input=prompt
    )
    return interaction.output_text




def parse_json(text:str)->dict:
    """
        Models sometime wraps JSON in ```json...``` fences even told not to.
        Strip them defensively before parsing. Never assume the output is clean.
    """
    cleaned=text.strip()
    if cleaned.startswith("```"):
        cleaned=cleaned.strip("`")
        if cleaned.lower().startswith("json"):
            cleaned=cleaned[4:]

    return json.loads(cleaned.strip())


extract_prompt=f"""
    Extract structured data from this customer email as json:
    {{"order_no":"...","sentiment":"positive|negative|mixed","wants_refund":true or false}}

    Email:"{customer_email}"

    Respond with Only the JSON object.
"""

raw_extraction=ask(extract_prompt)
print(f"raw_extraction: {raw_extraction}")

try:
    data=parse_json(raw_extraction)
except json.JSONDecodeError:
    print("Call 1 did not return valid JSON. Stopping the chain.")
    sys.exit(1)

print(f"Extracted: {data}")


escalation_prompt=f"""
    Given this customer data:{json.dumps(data)}
    Should this be escaleted to a human agent? Answer "yes" or "no".
"""

decision_raw=ask(escalation_prompt)
escalate=decision_raw.lower().startswith("yes")
print("Call 2 decision",decision_raw,"->",escalate,"\n")


reply_prompt=f"""
    write a short, professional reply to a customer.

    Facts (do not invent anything beyond these):
    - Order Number: {data["order_no"]}
    - Customer Sentiment: {data["sentiment"]}
    - Customer wants refund: {data["wants_refund"]}
    - Escalated to human: {escalate}

Acknowledge their frustraction. If escalated, confirm a specilist will contact them.
Do not promise  a specific  refund  amount or delivery date.
Respond with only the reply text
"""
reply=ask(reply_prompt)
print(f"Call 3 Reply:\n{reply}")