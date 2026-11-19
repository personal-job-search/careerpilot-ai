import requests
from job_sources.common import normalize

def fetch(slugs, query=""):
    jobs=[]
    for slug in filter(None, [x.strip() for x in slugs.split(",")]):
        try:
            data=requests.get(f"https://api.lever.co/v0/postings/{slug}?mode=json", timeout=25).json()
            for item in data:
                title=item.get("text","")
                desc=item.get("descriptionPlain","")
                if query.lower() not in title.lower() + " " + desc.lower(): continue
                categories=item.get("categories",{})
                loc=categories.get("location","")
                jobs.append(normalize("Lever", item.get("id"), title, slug, loc, desc,
                    item.get("hostedUrl",""), item.get("createdAt","")))
        except requests.RequestException:
            continue
    return jobs
