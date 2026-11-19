from datetime import datetime, timezone
from sqlalchemy import String, Text, DateTime, Integer, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from backend.db import Base

def utcnow():
    return datetime.now(timezone.utc)

class Job(Base):
    __tablename__ = "jobs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    external_id: Mapped[str] = mapped_column(String(500), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(500))
    company: Mapped[str] = mapped_column(String(300), default="")
    location: Mapped[str] = mapped_column(String(500), default="")
    description: Mapped[str] = mapped_column(Text, default="")
    source: Mapped[str] = mapped_column(String(100))
    application_url: Mapped[str] = mapped_column(Text, default="")
    posted_date: Mapped[str] = mapped_column(String(100), default="")
    first_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    last_verified: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="unverified")
    match_score: Mapped[float] = mapped_column(Float, default=0.0)

class Application(Base):
    __tablename__ = "applications"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    job_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    company: Mapped[str] = mapped_column(String(300))
    title: Mapped[str] = mapped_column(String(500))
    application_url: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(40), default="saved")
    applied_date: Mapped[str] = mapped_column(String(30), default="")
    notes: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
