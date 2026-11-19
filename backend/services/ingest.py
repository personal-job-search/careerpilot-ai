from datetime import datetime, timezone
from sqlalchemy import select
from backend.db import SessionLocal
from backend.models import Job
from backend.config import settings
from backend.services.matching import score_job
from job_sources import greenhouse, lever, ashby, adzuna, usajobs, smartrecruiters

def discover(query="data engineer", location="United States"):
    found=[]
    found += greenhouse.fetch(settings.greenhouse_board_slugs, query)
    found += lever.fetch(settings.lever_company_slugs, query)
    found += ashby.fetch(settings.ashby_board_slugs, query)
    found += smartrecruiters.fetch(settings.smartrecruiters_company_slugs, query)
    found += adzuna.fetch(query, location)
    found += usajobs.fetch(query, location)
    return found

def save_jobs(jobs, profile):
    db=SessionLocal()
    added=0
    try:
        for item in jobs:
            item["match_score"]=score_job(item,profile)["score"]
            existing=db.scalar(select(Job).where(Job.external_id==item["external_id"]))
            if existing:
                existing.title=item["title"]; existing.description=item["description"]
                existing.application_url=item["application_url"]; existing.status="unverified"
                existing.match_score=item["match_score"]
            else:
                db.add(Job(**item)); added+=1
        db.commit()
        return added
    finally:
        db.close()

def list_jobs():
    db=SessionLocal()
    try: return db.scalars(select(Job).order_by(Job.match_score.desc())).all()
    finally: db.close()

def mark_verified(job_id, is_open):
    db=SessionLocal()
    try:
        job=db.get(Job,job_id)
        if job:
            job.last_verified=datetime.now(timezone.utc)
            job.status="open" if is_open else "expired"
            db.commit()
    finally: db.close()
