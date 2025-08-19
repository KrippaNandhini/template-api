from app.settings import Settings


def test_settings_loads_from_env_defaults() -> None:
    s = Settings()
    assert s.APP_NAME != ""
