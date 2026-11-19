from sqlalchemy import select
from backend.db import SessionLocal
from backend.models import Application

STATUSES={"saved","applied","interview","rejected","offer","withdrawn"}

def add_application(data):
    if data.status not in STATUSES: raise ValueError("Invalid application status")
    db=SessionLocal()
    try:
        row=Application(**data.model_dump())
        db.add(row); db.commit(); db.refresh(row)
        return row
    finally: db.close()

def all_applications():
    db=SessionLocal()
    try: return db.scalars(select(Application).order_by(Application.created_at.desc())).all()
    finally: db.close()
