# CareerPilot AI

A local-first job discovery, resume matching, tailored-resume drafting, and application-tracking workspace.

## Current implementation

- Streamlit frontend and FastAPI backend
- SQLite database for local development
- Initial profile seeded from the supplied Data Engineer resume
- Job-source adapters:
  - Greenhouse, Lever, Ashby (public company-board endpoints; configure board slugs)
  - Adzuna (API credentials required)
  - USAJOBS (API credentials required)
  - SmartRecruiters (public postings endpoint; validate tenant availability)
  - HiringCafe and Welcome to the Jungle are explicitly marked **not enabled** until a supported, permitted API/feed is configured. No scraping is performed.
- Job deduplication, source timestamps, original application URLs, and re-verification metadata
- Explainable deterministic match score
- Application tracker
- Optional Hugging Face/OpenAI-compatible LLM endpoint for resume tailoring; deterministic fallback is provided
- Resume upload (.docx/.pdf) and extraction

## Important safeguards

- The app never auto-submits applications.
- Resume tailoring is a draft. Review and approve every change.
- Do not add skills, employers, tools, accomplishments, metrics, or experience that are not supported by the master profile.
- Job records are marked `unverified` until refreshed against the source. A saved job is not assumed to still be open.
- LinkedIn and Indeed scraping/automation are intentionally excluded.
- Keep `.env` private. Never commit API keys or personal resume files.

## Quick start (Mac)

```bash
cd careerpilot-ai
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
streamlit run frontend/streamlit_app.py
```

In another terminal, optionally start the API:

```bash
source .venv/bin/activate
uvicorn backend.main:app --reload --port 8000
```

The Streamlit app can use its local service layer directly; the API is available for future integrations.

## Configure sources

Edit `.env`:

- `ADZUNA_APP_ID`, `ADZUNA_APP_KEY`
- `USAJOBS_API_KEY`, `USAJOBS_USER_AGENT`
- `GREENHOUSE_BOARD_SLUGS`, `LEVER_COMPANY_SLUGS`, `ASHBY_BOARD_SLUGS`
- `SMARTRECRUITERS_COMPANY_SLUGS`

The ATS board adapters need company board slugs. There is no universal endpoint that searches every employer on those ATS platforms. The UI lets you enter slugs; the source adapters query only those configured boards.

`HIRINGCAFE_ENABLED` and `WELCOME_TO_JUNGLE_ENABLED` default to `false`. Enable only after you have a documented, authorized API/feed and implement its adapter accordingly.

## Data and privacy

SQLite database: `data/careerpilot.db` (created on first run). Uploaded resumes and generated drafts stay local by default. Back up or delete the `data/` directory as needed.

## Tests

```bash
pytest -q
```

## Roadmap

1. Validate job-source coverage and rate limits for configured boards.
2. Add scheduled refresh and alerts.
3. Add semantic embeddings and reranking after the deterministic baseline is validated.
4. Add user-controlled GitHub publishing and deployment only after credentials/connection are authorized.
