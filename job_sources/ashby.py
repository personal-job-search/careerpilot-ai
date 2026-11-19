import requests
from job_sources.common import normalize

def fetch(slugs, query=""):
    jobs=[]
    for slug in filter(None, [x.strip() for x in slugs.split(",")]):
        try:
            data=requests.get(f"https://api.ashbyhq.com/posting-api/job-board/{slug}", timeout=25).json()
            for item in data.get("jobs", []):
                title=item.get("title","")
                desc=item.get("descriptionPlain","") or item.get("descriptionHtml","")
                if query.lower() not in title.lower() + " " + desc.lower(): continue
                jobs.append(normalize("Ashby", item.get("id"), title, slug,
                    item.get("location",""), desc, item.get("jobUrl",""), item.get("publishedAt","")))
        except requests.RequestException:
            continue
    return jobs
