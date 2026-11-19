import sys, json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import streamlit as st
from backend.db import Base, engine
from backend.models import Job, Application
from backend.services.profile import load_profile, save_profile
from backend.services.ingest import discover, save_jobs, list_jobs
from backend.services.matching import score_job
from backend.services.tracker import add_application, all_applications
from backend.services.resume import extract_resume
from backend.services.tailor import draft_tailoring
from job_sources.unsupported import source_status

st.set_page_config(page_title="CareerPilot AI",page_icon="🧭",layout="wide")
Base.metadata.create_all(bind=engine)
st.title("🧭 CareerPilot AI")
st.caption("Local-first job discovery · evidence-based matching · resume drafts · application tracking")
profile=load_profile()

tabs=st.tabs(["Dashboard","Find jobs","Master profile","Resume tailoring","Application tracker","Source setup"])

with tabs[0]:
    jobs=list_jobs(); apps=all_applications()
    c1,c2,c3=st.columns(3)
    c1.metric("Jobs saved",len(jobs)); c2.metric("Applications tracked",len(apps))
    c3.metric("Interviews",sum(1 for a in apps if a.status=="interview"))
    st.subheader("Profile")
    st.write(profile.get("headline",""),"—",profile.get("location",""))
    st.info("Job records default to **unverified**. Refresh source data and check the employer application page before applying.")

with tabs[1]:
    st.subheader("Discover jobs")
    q=st.text_input("Role or keyword", "Data Engineer")
    loc=st.text_input("Location", "United States")
    if st.button("Search configured sources",type="primary"):
        with st.spinner("Querying configured public job feeds..."):
            results=discover(q,loc)
            added=save_jobs(results,profile)
        st.success(f"Fetched {len(results)} postings; added {added} new records.")
    jobs=list_jobs()
    if jobs:
        for j in jobs:
            with st.container(border=True):
                st.markdown(f"**{j.title}** — {j.company}")
                st.caption(f"{j.location} · {j.source} · Match score {j.match_score:.1f}/100 · {j.status}")
                st.write((j.description or "")[:550])
                if j.application_url: st.link_button("Open original application page",j.application_url)
                if st.button("Add to tracker",key=f"track_{j.id}"):
                    from backend.schemas import ApplicationCreate
                    add_application(ApplicationCreate(job_id=j.id,company=j.company,title=j.title,application_url=j.application_url,status="saved"))
                    st.success("Saved to application tracker.")
    else: st.caption("No jobs yet. Configure source credentials and board slugs in Source setup / .env.")

with tabs[2]:
    st.subheader("Master profile")
    st.write("Imported from your uploaded Data Engineer resume. Edit only when the source resume supports the change.")
    st.text_area("Professional summary",profile.get("summary",""),height=150,disabled=True)
    for group,skills in profile.get("skills",{}).items():
        st.markdown(f"**{group}:** "+", ".join(skills))
    with st.expander("Experience and projects"):
        st.json({"experience":profile.get("experience",[]),"projects":profile.get("projects",[])})
    uploaded=st.file_uploader("Replace / update master resume (.docx or .pdf)",type=["docx","pdf"])
    if uploaded:
        Path("data/uploads").mkdir(parents=True,exist_ok=True)
        target=Path("data/uploads")/uploaded.name
        target.write_bytes(uploaded.getbuffer())
        extracted=extract_resume(str(target))
        st.text_area("Extracted text — review before updating the structured profile",extracted,height=250)

with tabs[3]:
    st.subheader("Job-specific resume tailoring")
    jobs=list_jobs()
    if jobs:
        choice=st.selectbox("Choose a saved job",jobs,format_func=lambda x:f"{x.title} — {x.company}")
        if st.button("Generate tailoring suggestions"):
            result=draft_tailoring(profile,{"title":choice.title,"company":choice.company,"description":choice.description})
            st.session_state["tailoring_result"]=result
        if "tailoring_result" in st.session_state:
            st.warning("Draft only. Review every statement against your real experience before using it.")
            st.json(st.session_state["tailoring_result"])
    else: st.info("Discover and save a job first.")
    st.caption("No automatic resume rewrite or application submission is performed.")

with tabs[4]:
    st.subheader("Application tracker")
    apps=all_applications()
    if apps:
        st.dataframe([{"Company":a.company,"Role":a.title,"Status":a.status,"Applied":a.applied_date,"URL":a.application_url} for a in apps],use_container_width=True)
    with st.form("manual_application"):
        company=st.text_input("Company")
        title=st.text_input("Role")
        url=st.text_input("Application URL")
        status=st.selectbox("Status",["saved","applied","interview","rejected","offer","withdrawn"])
        applied=st.text_input("Applied date (YYYY-MM-DD)")
        notes=st.text_area("Notes")
        submitted=st.form_submit_button("Add application")
        if submitted and company and title:
            from backend.schemas import ApplicationCreate
            add_application(ApplicationCreate(company=company,title=title,application_url=url,status=status,applied_date=applied,notes=notes))
            st.success("Application added. Refresh this tab to see it.")

with tabs[5]:
    st.subheader("Job-source configuration")
    st.write("Set credentials and comma-separated company board slugs in `.env`, then restart the app.")
    st.code("GREENHOUSE_BOARD_SLUGS=company1,company2\nLEVER_COMPANY_SLUGS=company1,company2\nASHBY_BOARD_SLUGS=company1,company2\nSMARTRECRUITERS_COMPANY_SLUGS=company1,company2\nADZUNA_APP_ID=...\nADZUNA_APP_KEY=...\nUSAJOBS_API_KEY=...\nUSAJOBS_USER_AGENT=...")
    for source,msg in source_status().items(): st.write(f"**{source}:** {msg}")
    st.warning("“All sources” means all supported/configurable adapters in this build. Unsupported sources are disclosed rather than scraped or represented as active.")
