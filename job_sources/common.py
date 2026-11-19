import hashlib
from datetime import datetime, timezone

def normalize(source, external_id, title, company="", location="", description="", url="", posted=""):
    raw = f"{source}:{external_id or url or title}:{company}"
    return {
      "external_id": hashlib.sha256(raw.encode()).hexdigest(),
      "title": title or "Untitled role",
      "company": company or "",
      "location": location or "",
      "description": description or "",
      "source": source,
      "application_url": url or "",
      "posted_date": str(posted or ""),
      "status": "unverified",
      "last_verified": None
    }
