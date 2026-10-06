from anthropic.types import citation_content_block_location_param
import os
from typing import Literal,Optional

from anthropic import Anthropic
from dotenv import load_dotenv
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel


load_dotenv()

app=FastAPI(title="Ticket Extraction Service")

client=Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
MODEL="claude-haiku-4-5-20251001"
SYSTEM=(
            "You are a ticket-data extractor. Respond with ONLY valid JSON "
            "matching the given schema. No markdown fences, no explanation."
        )
# PROMPT=
class EmailRequest(BaseModel):
    email_text:str

class Ticket(BaseModel):
    order_number:Optional[str]
    sentiment:Literal["positive","negative","mixed"]
    wants_refund:bool

@app.post("/extract-ticket",response_model=Ticket)
def extract_ticket(request:EmailRequest)->Ticket:
    schema_hint=Ticket.model_json_schema()

    response=client.messages.create(
        model=MODEL,
        max_tokens=300,
        extra_body={"temperature":0.0},
        system=SYSTEM,
        messages=[
            {
                "role":"user",
                "content":(
                    f"Extract the ticket data from this email:\n\n{request.email_text}\n\n"
                    f"JSON schema to match:\n\n{schema_hint}"
                ),
            }
        ]
    )

    raw_text=response.content[0].text
    clean_text=raw_text.strip()
    if clean_text.startswith("```"):
        clean_text=clean_text.split("```")[1]
        if clean_text.startswith("json"):
            clean_text=clean_text[4:]
        clean_text=clean_text.strip()

    try:
        ticket=Ticket.model_validate_json(clean_text)
        return ticket
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Model returned invalid ticket data: {e}")



@app.get("/health")
def health():
    return {"status":"ok"}


