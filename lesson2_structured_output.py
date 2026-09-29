#Gemini 


# from urllib import response
# import os
# import json
# import sys

# # pyrefly: ignore [missing-import]
# from dotenv import load_dotenv
# from google import genai
# from google.genai import types
# from typing import Literal
# from pydantic import BaseModel

# sys.stdout.reconfigure(encoding='utf-8')

# customer_email= (
#     "Hi, my order  never arrived, it's been 2 weeks, "
#     "I'm really frustrated, please help or I want a refund."
# )

# class Ticket (BaseModel):
#     order_number: str
#     sentiment: Literal['positive','negative',"mixed"]
#     wants_refund: bool

# load_dotenv()
# client=genai.Client(api_key=os.environ["Gemini_API_Key"])
# MODEL="gemini-3.6-flash"
# response=client.models.generate_content(
#     model=MODEL,
#     contents=f"Extract the ticket data from the customer email:\n\n{customer_email}",
#     config=types.GenerateContentConfig(
#         response_mime_type="application/json",
#         response_schema=Ticket,
#         system_instruction="You are a helpful assistant."
#     )
# )

# print("Raw Text:",response.text)

# ticket=response.parsed
# print("type of wants_refund :",type(ticket.wants_refund))

# print(ticket)

# if ticket.wants_refund:
#     print("-> route to refund flow")

# ======================================================================================

# OPEN AI


# from urllib import response
# import os
# import json
# import sys

# # pyrefly: ignore [missing-import]
# from dotenv import load_dotenv
# from openai import OpenAI
# from typing import Literal,Optional
# from pydantic import BaseModel

# sys.stdout.reconfigure(encoding='utf-8')

# customer_email= (
#     "Hi, my order  never arrived, it's been 2 weeks, "
#     "I'm really frustrated, please help or I want a refund."
# )

# class Ticket (BaseModel):
#     order_number: str
#     sentiment: Literal['positive','negative',"mixed"]
#     wants_refund: bool

# load_dotenv()
# client=OpenAI(api_key=os.environ["OPENAI_API_KEY"])
# MODEL="gpt-5"
# response=client.chat.completions.parse(
#     model=MODEL,
#     messages=[
#         {"role":"system","content":"You are a helpful assistant."},
#         {"role":"user","content":f"Extract the ticket data from the customer email:\n\n{customer_email}"}
#     ],
#     response_format=Ticket
# )

# print("Raw Text:",response.choises[0].messages.content)

# ticket=response.choises[0].messages.parsed
# print("type of wants_refund :",type(ticket.wants_refund))

# print(ticket)

# if ticket.wants_refund:
#     print("-> route to refund flow")

# ========================================================================================

# ANTHROPIC

import os
import sys
from typing import Literal,Optional
from pydantic import BaseModel
from anthropic import Anthropic
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')

customer_email=(
    "Hi, My order never arived, its been 2 week,"
    "I'm really frustrated,please help and I want refund"
)

class Ticket (BaseModel):
    order_number:Optional[str]
    sentiment:Literal["positive","negative","mixed"]
    wants_refund:bool

load_dotenv()
client=Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
MODEL="claude-haiku-4-5-20251001"

schema_hint=Ticket.model_json_schema()

response=client.messages.create(
    model=MODEL,
    max_tokens=300,
    system="You are a helpful assistant. Respond with ONLY valid JSON matching the given schema. No markdown fences, no explanation.",
    messages=[
        {
            "role":"user",
            "content":(
                f"Extract the ticket data from this customer_email:\n\n{customer_email}\n\n"
                f"JSON schema to match:\n\n{schema_hint}"
            )
        }
    ]
)

raw_text=response.content[0].text
print("Raw Text:",raw_text)


clean_text = raw_text.strip()
if clean_text.startswith("```"):
    clean_text = clean_text.split("```")[1]
    if clean_text.startswith("json"):
        clean_text = clean_text[4:]
    clean_text = clean_text.strip()


ticket=Ticket.model_validate_json(clean_text)

print("Type of wants_refund :",type(ticket.wants_refund))

print(ticket)

if ticket.wants_refund:
    print("-> route to refund flow")
 
print("\n---")
print(f"Input tokens:  {response.usage.input_tokens}")
print(f"Output tokens: {response.usage.output_tokens}")