from pydantic import BaseModel, HttpUrl
from typing import Optional

class JobOut(BaseModel):
    id: int
    title: str
    company: str
    location: str
    source: str
    application_url: str
    posted_date: str
    status: str
    match_score: float
    model_config = {"from_attributes": True}

class ApplicationCreate(BaseModel):
    job_id: Optional[int] = None
    company: str
    title: str
    application_url: str = ""
    status: str = "saved"
    applied_date: str = ""
    notes: str = ""
