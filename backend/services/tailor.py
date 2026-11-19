import os
import requests
from backend.config import settings

def draft_tailoring(profile: dict, job: dict) -> dict:
    # Optional OpenAI-compatible endpoint (e.g. a self-hosted Hugging Face TGI/vLLM endpoint).
    # LLM output is always marked as a draft and must be reviewed by the user.
    if settings.llm_base_url and settings.llm_model:
        prompt = f'''You are a resume editor. Use ONLY evidence in the supplied profile.
Do not invent skills, employers, dates, tools, metrics, achievements, or responsibilities.
Return JSON with keys "suggested_summary", "relevant_bullets", "gaps_to_review".
Job: {job.get("title")} at {job.get("company")}
Job description: {job.get("description","")[:10000]}
Verified profile: {profile}'''
        try:
            response = requests.post(
                settings.llm_base_url.rstrip("/") + "/v1/chat/completions",
                headers={"Authorization": f"Bearer {settings.llm_api_key}"} if settings.llm_api_key else {},
                json={"model": settings.llm_model, "messages":[{"role":"user","content":prompt}], "temperature":0.1},
                timeout=90,
            )
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
            return {"draft": content, "mode":"llm", "approval_required":True}
        except Exception as exc:
            return {"draft": "", "mode":"llm_error", "error":str(exc), "approval_required":True}
    return {
      "draft": "LLM not configured. Use the matched evidence below to manually tailor the resume. No resume content has been changed.",
      "mode":"manual",
      "matched_profile_sections": ["summary", "skills", "experience"],
      "approval_required": True
    }
