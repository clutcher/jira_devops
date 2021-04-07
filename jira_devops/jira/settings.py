import os

from django.apps import AppConfig
from django.core.exceptions import ImproperlyConfigured


class JiraAppConfig(AppConfig):
    name = 'jira_devops.jira'
    verbose_name = 'Jira Connections'

    def ready(self):
        from django.conf import settings
        settings = settings._wrapped.__dict__
        settings.setdefault('JIRA_SERVER', self.get_env_variable_with_exception("JIRA_SERVER"))

        settings.setdefault('JIRA_USERNAME', self.get_env_variable_with_exception("JIRA_USERNAME"))
        settings.setdefault('JIRA_PASSWORD', self.get_env_variable_with_exception("JIRA_PASSWORD"))

        settings.setdefault('JIRA_PROJECT_IDS', ['TBC'])

    @staticmethod
    def get_env_variable_with_exception(variable):
        value = os.getenv(variable)
        if not value:
            raise ImproperlyConfigured(
                "Env variable is not setup for %s" % variable
            )
        return value
