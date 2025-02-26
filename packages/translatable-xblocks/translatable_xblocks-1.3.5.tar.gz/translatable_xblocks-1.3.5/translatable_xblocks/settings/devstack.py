""" Config specific to the developer environment """


def plugin_settings(settings):
    """
    App-specific settings
    """
    # AI Translations Service
    settings.AI_TRANSLATIONS_API_URL = "http://host.docker.internal:18760"
    settings.AI_TRANSLATIONS_OAUTH_APP_NAME = "ai_translations-backend-service"

    # Add filter config
    settings.OPEN_EDX_FILTERS_CONFIG = getattr(settings, "OPEN_EDX_FILTERS_CONFIG", {})

    settings.OPEN_EDX_FILTERS_CONFIG[
        "org.openedx.learning.xblock.render.started.v1"
    ] = {
        "fail_silently": False,
        "pipeline": ["translatable_xblocks.filters.UpdateRequestLanguageCode"],
    }
