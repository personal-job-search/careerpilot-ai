import re

def tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-zA-Z][a-zA-Z0-9+#.]{1,}", (text or "").lower()))

def score_job(job: dict, profile: dict) -> dict:
    profile_terms = set()
    for values in profile.get("skills", {}).values():
        profile_terms.update(tokens(" ".join(values)))
    profile_terms.update(tokens(profile.get("summary", "")))
    jd_terms = tokens(" ".join([job.get("title",""), job.get("description","")]))
    overlap = profile_terms & jd_terms
    ratio = len(overlap) / max(1, min(len(profile_terms), 40))
    title_terms = tokens(job.get("title", ""))
    role_bonus = 15 if title_terms & {"data", "engineer", "etl", "analytics", "quality"} else 0
    score = min(100.0, round(ratio * 100 + role_bonus, 1))
    return {"score": score, "matched_terms": sorted(overlap)[:30],
            "note": "Deterministic keyword overlap; not an ATS prediction. Review required and preferred qualifications manually."}
