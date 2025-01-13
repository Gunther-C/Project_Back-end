import logging
import sentry_sdk


def conf_sentry():
    sentry_logging = sentry_sdk.integrations.logging.LoggingIntegration(
        level=logging.INFO,
        event_level=logging.ERROR
    )

    sentry_sdk.init(
        dsn="YOUR_SENTRY_DSN",
        integrations=[sentry_logging]
    )

    logging.basicConfig(level=logging.INFO)
