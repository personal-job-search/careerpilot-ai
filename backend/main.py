from fastapi import FastAPI
from backend.db import Base, engine
from backend.models import Job, Application
from backend.services.profile import load_profile
from backend.services.ingest import discover, save_jobs, list_jobs
from backend.schemas import ApplicationCreate
from backend.services.tracker import add_application, all_applications

Base.metadata.create_all(bind=engine)
app=FastAPI(title="CareerPilot AI API", version="0.1.0")

@app.get("/health")
def health(): return {"status":"ok"}

@app.get("/profile")
def profile(): return load_profile()

@app.post("/jobs/discover")
def discover_jobs(query: str="data engineer", location: str="United States"):
    jobs=discover(query,location)
    added=save_jobs(jobs,load_profile())
    return {"fetched":len(jobs),"new_records":added}

@app.get("/jobs")
def jobs(): return list_jobs()

@app.post("/applications")
def create_application(data: ApplicationCreate): return add_application(data)

@app.get("/applications")
def applications(): return all_applications()
