import requests
from job_sources.common import normalize

def fetch(slugs, query=""):
    jobs=[]
    for slug in filter(None,[x.strip() for x in slugs.split(",")]):
        try:
            data=requests.get(f"https://api.smartrecruiters.com/v1/companies/{slug}/postings",params={"limit":100},timeout=25).json()
            for item in data.get("content",[]):
                title=item.get("name","")
                if query.lower() not in title.lower(): continue
                loc=item.get("location",{})
                jobs.append(normalize("SmartRecruiters",item.get("id"),title,slug,
                    ", ".join(filter(None,[loc.get("city"),loc.get("region"),loc.get("country")])),
                    item.get("ref",""),item.get("ref",""),item.get("releasedDate","")))
        except requests.RequestException:
            continue
    return jobs
