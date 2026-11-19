from backend.services.matching import score_job

def test_matching_detects_bigquery_and_python():
    profile={"summary":"Python SQL data engineer","skills":{"Cloud":["BigQuery","Airflow"]}}
    job={"title":"Data Engineer","description":"Build BigQuery pipelines using Python and Airflow"}
    result=score_job(job,profile)
    assert result["score"] > 0
    assert {"python","bigquery"} <= set(result["matched_terms"])
