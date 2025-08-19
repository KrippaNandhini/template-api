from logging.config import dictConfig


def setup_logging() -> None:
    """
    Configure root logger for JSON logs on stdout.
    Falls back to plain text if python-json-logger isn't available.
    """
    fmt = "%(asctime)s %(levelname)s %(name)s %(message)s %(pathname)s:%(lineno)d"

    try:
        dictConfig(
            {
                "version": 1,
                "disable_existing_loggers": False,
                "formatters": {
                    "json": {
                        # NOTE: correct module path (no underscore)
                        "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                        "fmt": fmt,
                    }
                },
                "handlers": {
                    "console": {"class": "logging.StreamHandler", "formatter": "json"}
                },
                "root": {"handlers": ["console"], "level": "INFO"},
            }
        )
    except Exception:
        # Safe fallback if the JSON formatter isn't present for any reason
        dictConfig(
            {
                "version": 1,
                "disable_existing_loggers": False,
                "formatters": {"plain": {"format": fmt}},
                "handlers": {
                    "console": {"class": "logging.StreamHandler", "formatter": "plain"}
                },
                "root": {"handlers": ["console"], "level": "INFO"},
            }
        )
