# Exercise 1
#  import os
# # pyrefly: ignore [missing-import]
# from dotenv import load_dotenv
# from google import genai



# load_dotenv()

# client=genai.Client(api_key=os.environ["Gemini_API_Key"])

# interaction = client.interactions.create(
#     model="gemini-3.6-flash",
#     system_instruction="You are a helpful coding assistant.",
#     input=("write a function to validate email"),
# # generation_config={"max_output_tokens":500}

# )

# answer=interaction.output_text

# print(answer)
# print("\n---")
# print(f"Interaction id: {interaction.id}")

# =================================================================================
# Exercise 2

# import os
# # pyrefly: ignore [missing-import]
# from dotenv import load_dotenv
# from google import genai



# load_dotenv()

# client=genai.Client(api_key=os.environ["Gemini_API_Key"])

# interaction = client.interactions.create(
#     model="gemini-3.6-flash",
#     system_instruction="You are a helpful coding assistant.",
#     input="""
# Write a Python function `is_valid_email(email: str) -> bool`.

# Requirements:
# - Use the `re` module (no external dependencies)
# - Must reject strings with no '@' or no domain part
# - Do not attempt full RFC 5322 compliance — basic format checking is enough
# - Return False for None or empty string, do not raise an exception
# """,
# # generation_config={"max_output_tokens":500}

# )

# answer=interaction.output_text

# print(answer)
# print("\n---")
# print(f"Interaction id: {interaction.id}")

# ====================================================================================

# Exercise 3
# import os

# # pyrefly: ignore [missing-import]
# from dotenv import load_dotenv
# from google import genai

# load_dotenv()

# client = genai.Client(api_key=os.environ['Gemini_API_Key'])

# interaction=client.interactions.create(
#     model="gemini-3.6-flash",
#     system_instruction="You are a Helpfull HR assistence !",
#     input="""
#         Help me craft a resume!
        
#         Requirements
#         - Use a clean, modern template
# - Include sections: Contact, Summary, Experience, Education, Skills
# - Keep it under 500 words
# - Output only the Markdown text (no explanations, no chat)
#     """
# )
# answer=interaction.output_text
# print(answer)

# =======================================================================================
# Exercise 4

# import os
# # pyrefly: ignore [missing-import]
# from dotenv import load_dotenv
# from google import genai

# load_dotenv()
# client = genai.Client(api_key=os.environ['Gemini_API_Key'])

# interaction = client.interactions.create(
#     model="gemini-3.6-flash",
#     system_instruction="You are a helpful assistant.",
#     input="""
# Classify the sentiment of this review as exactly one word: positive, negative, or mixed.
# Review: "The food was absolutely amazing and the service was quick."

# Respond with ONLY the single word. No punctuation, no explanation.
# """
# )
# print(interaction.output_text)

# ======================================================================================
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


def ask(prompt:str,system="You are a Helpfull assistant")->str:
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
    {{"order_no":"...","sentiment":"positive|negative|mixed","wants_refund":"true|false"}}

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

    