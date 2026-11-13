from typing import Literal
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from engines.traditional import analyze_traditional
from engines.generative import analyze_generative

app = FastAPI(
    title="AI Support Engine",
    description="API de clasificacion hibrida de tickets de soporte",
    version="1.0.0"
)

class AnalyzeRequest(BaseModel):
    message: str = Field(..., min_length=3, max_length=2000)
    mode: Literal["traditional", "generative"]

    @field_validator("message")
    @classmethod
    def message_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("El mensaje no puede contener solo espacios en blanco.")
        return v.strip()

class AnalyzeResponse(BaseModel):
    category: Literal["ACCESS", "BUG", "FEATURE", "SECURITY"]
    priority: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    response: str
    requiresHumanReview: bool
    mode: Literal["traditional", "generative"]

@app.post("/api/analyze", response_model=AnalyzeResponse)
def analyze_ticket(payload: AnalyzeRequest):
    try:
        if payload.mode == "traditional":
            result = analyze_traditional(payload.message)
        else:
            result = analyze_generative(payload.message)
        return AnalyzeResponse(**result)
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno inesperado en el servidor.")
