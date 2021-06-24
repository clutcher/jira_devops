import os

from django.apps import AppConfig


class ReleaseNotesAppConfig(AppConfig):
    name = 'jira_devops.release_notes'
    verbose_name = 'Release Notes'

    DEFAULT_JIRA_RELEASE_FIELD_MAP = {
        "hac_update": "customfield_13359",
        "need_impex": "customfield_13360",
        "need_manual": "customfield_13361",
        "special_notes": "customfield_13362",
        "responsible_person": "customfield_12200",
    }

    def ready(self):
        from django.conf import settings
        settings = settings._wrapped.__dict__
        settings.setdefault('JIRA_RELEASE_FIELD_MAP', self.DEFAULT_JIRA_RELEASE_FIELD_MAP)

        settings.setdefault('FILE_CLEAN_UP_PREFIX', self.get_env_variable("FILE_CLEAN_UP_PREFIX", "hybris/bin/custom"))

    @staticmethod
    def get_env_variable(variable, default=""):
        value = os.getenv(variable)
        if not value:
            return default
        return value
