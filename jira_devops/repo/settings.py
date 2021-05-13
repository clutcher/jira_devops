import logging
import os
import tempfile

from django.apps import AppConfig

from jira_devops.repo.RepoService import RepoService


class RepoAppConfig(AppConfig):
    name = 'jira_devops.repo'
    verbose_name = 'Repository'

    def ready(self):
        temp_dir = tempfile.gettempdir()
        temp_repo_path = os.path.join(temp_dir, "jira_devops", "repo")

        from django.conf import settings
        dict_settings = settings._wrapped.__dict__
        dict_settings.setdefault('GIT_REPO_PATH', temp_repo_path)

        dict_settings.setdefault('GIT_REPO_URL', self.get_env_variable("GIT_REPO_URL"))
        dict_settings.setdefault('GIT_WORKING_BRANCH', "release")

        dict_settings.setdefault('GIT_USERNAME', self.get_env_variable("GIT_USERNAME"))
        dict_settings.setdefault('GIT_PASSWORD', self.get_env_variable("GIT_PASSWORD"))

        logger = logging.getLogger("repo.RepoAppConfig")
        try:
            pass
            RepoService.force_create_repository(logger)
        except:
            logger.error("Cant create init git repository!")

    @staticmethod
    def get_env_variable(variable):
        value = os.getenv(variable)
        if not value:
            return ""
        return value
