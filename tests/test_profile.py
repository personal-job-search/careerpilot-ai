from backend.services.profile import load_profile

def test_seed_profile_has_resume_data():
    p=load_profile()
    assert p["headline"]=="Data Engineer"
    assert any(x["company"]=="Aetna" for x in p["experience"])
