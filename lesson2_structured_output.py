from urllib import response
import os
import json
import sys

# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
from google import genai
from google.genai import types
from typing import Literal
from pydantic import BaseModel

sys.stdout.reconfigure(encoding='utf-8')

customer_email= (
    "Hi, my order #4471 never arrived, it's been 2 weeks, "
    "I'm really frustrated, please help or I want a refund."
)

class Ticket (BaseModel):
    order_number: str
    sentiment: Literal['positive','negative',"mixed"]
    wants_refund: bool

load_dotenv()
client=genai.Client(api_key=os.environ["Gemini_API_Key"])
MODEL="gemini-3.6-flash"
response=client.models.generate_content(
    model=MODEL,
    contents=f"Extract the ticket data from the customer email:\n\n{customer_email}",
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=Ticket,
        system_instruction="You are a helpful assistant."
    )
)

print("Raw Text:",response.text)

ticket=response.parsed
print("type of wants_refund :",type(ticket.wants_refund))

print(ticket)

if ticket.wants_refund:
    print("-> route to refund flow")