import requests
from job_sources.common import normalize

def fetch(slugs, query=""):
    jobs=[]
    for slug in filter(None, [x.strip() for x in slugs.split(",")]):
        url=f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true"
        try:
            data=requests.get(url, timeout=25).json()
            for item in data.get("jobs", []):
                title=item.get("title","")
                if query.lower() not in title.lower() + " " + item.get("content","").lower(): continue
                jobs.append(normalize("Greenhouse", item.get("id"), title, slug,
                    item.get("location",{}).get("name",""), item.get("content",""),
                    item.get("absolute_url",""), item.get("updated_at","")))
        except requests.RequestException:
            continue
    return jobs
