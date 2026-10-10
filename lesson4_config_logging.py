import logging
import time
from typing import Literal,Optional
from anthropic import AsyncAnthropic
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pydantic_settings import BaseSettings,SettingsConfigDict

# Configuration
class Setting(BaseSettings):
    anthropic_api_key:str
    model:str
    max_tokens:int
    temperature:float
    log_level:str

    model_config = SettingsConfigDict(env_file=".env",extra="ignore")

setting=Setting()

# Logging
logging.basicConfig(
    level=setting.log_level.upper(),
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    force=True
)

logger =logging.getLogger("ticket_service")

# App
app=FastAPI(title="Ticket Extraction Service")
client=AsyncAnthropic(api_key=setting.anthropic_api_key)

SYSTEM=(
    "You are a ticket-data extractor. Respond with ONLY valid JSON "
    "matching the given schema. No markdown fences, no explanation."
)

class EmailRequest(BaseModel):
    email_text:str

class Ticket(BaseModel):
    order_number:Optional[str]
    sentiment:Literal["positive","negative","mixed"]
    wants_refund:bool

@app.post("/extract-ticket",response_model=Ticket)
async def extract_ticket(request:EmailRequest)->Ticket:
    schema_hint= Ticket.model_json_schema()
    start=time.perf_counter()

    try:
        response=await client.messages.create(
            model=setting.model,
            max_tokens=setting.max_tokens,
            extra_body={"temperature":setting.temperature},
            system=SYSTEM,
            messages=[
                {
                    "role":"user",
                    "content":(
                        f"Extract the ticket data from this email:\n\n{request.email_text}\n\n"
                        f"JSON Schema to match:\n\n{schema_hint}"
                    ),
                }
            ]
        )
    except Exception as e:
        logger.exception("LLM call failed",)
        raise HTTPException(status_code=503,detail=f"AI service unavailable: {e}")

    latency_ms=(time.perf_counter()-start)*1000
    logger.info(
        "llm_call model-%s \n latency_ms=%.0f \n input_tokens=%d \n output_tokens=%d \n email_chars=%d \n stop_reason=%s",
        setting.model,
        latency_ms,
        response.usage.input_tokens,
        response.usage.output_tokens,
        len(request.email_text),
        response.stop_reason,
    ) 

    raw_text=response.content[0].text
    clean_text= raw_text.strip()
    if clean_text.startswith("```"):
        clean_text=clean_text.split("```")[1]
        if clean_text.startswith("json"):
            clean_text = clean_text[4:]
        clean_text=clean_text.strip()
    
    try:
        return Ticket.model_validate_json(clean_text)
    except Exception as e:
        logger.warning("invalid_model_output stop_reason=%s error=%s", response.stop_reason, e)
        raise HTTPException(status_code=502, detail=f"Model returned invalid ticket data: {e}")


@app.get("/health")
def health():
    return {"status": "ok"}
