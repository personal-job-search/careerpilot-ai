from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "sqlite:///./data/careerpilot.db"
    adzuna_app_id: str = ""
    adzuna_app_key: str = ""
    usajobs_api_key: str = ""
    usajobs_user_agent: str = ""
    greenhouse_board_slugs: str = ""
    lever_company_slugs: str = ""
    ashby_board_slugs: str = ""
    smartrecruiters_company_slugs: str = ""
    hiringcafe_enabled: bool = False
    welcome_to_jungle_enabled: bool = False
    llm_base_url: str = ""
    llm_api_key: str = ""
    llm_model: str = ""
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
