import requests
from backend.config import settings
from job_sources.common import normalize

def fetch(query="data engineer", location=""):
    if not settings.usajobs_api_key or not settings.usajobs_user_agent: return []
    headers={"Host":"data.usajobs.gov","User-Agent":settings.usajobs_user_agent,"Authorization-Key":settings.usajobs_api_key}
    params={"Keyword":query,"LocationName":location,"ResultsPerPage":50}
    try:
        data=requests.get("https://data.usajobs.gov/api/search",headers=headers,params=params,timeout=30).json()
        items=data.get("SearchResult",{}).get("SearchResultItems",[])
        out=[]
        for x in items:
            p=x.get("MatchedObjectDescriptor",{})
            out.append(normalize("USAJOBS",p.get("PositionID"),p.get("PositionTitle"),p.get("OrganizationName"),
                p.get("PositionLocationDisplay"),p.get("UserArea",{}).get("Details",{}).get("JobSummary",""),
                p.get("PositionURI"),p.get("PublicationStartDate","")))
        return out
    except requests.RequestException:
        return []
