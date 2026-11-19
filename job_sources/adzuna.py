import requests
from backend.config import settings
from job_sources.common import normalize

def fetch(query="data engineer", location="United States"):
    if not settings.adzuna_app_id or not settings.adzuna_app_key: return []
    params={"app_id":settings.adzuna_app_id,"app_key":settings.adzuna_app_key,"what":query,"where":location,"results_per_page":50}
    try:
        data=requests.get("https://api.adzuna.com/v1/api/jobs/us/search/1",params=params,timeout=30).json()
        return [normalize("Adzuna", x.get("id"), x.get("title"), x.get("company",{}).get("display_name"),
            x.get("location",{}).get("display_name"), x.get("description"), x.get("redirect_url"), x.get("created"))
            for x in data.get("results",[])]
    except requests.RequestException:
        return []
