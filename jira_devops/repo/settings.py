import logging
import os
import subprocess
import tempfile

from django.apps import AppConfig


class RepoAppConfig(AppConfig):
    name = 'jira_devops.repo'
    verbose_name = 'Repository'

    def ready(self):
        temp_dir = tempfile.gettempdir()
        temp_repo_path = os.path.join(temp_dir, "jira_devops", "repo")

        from django.conf import settings
        settings = settings._wrapped.__dict__
        settings.setdefault('GIT_REPO_PATH', temp_repo_path)

        settings.setdefault('GIT_REPO_URL', self.get_env_variable("GIT_REPO_URL"))
        settings.setdefault('GIT_WORKING_BRANCH', "release")

        settings.setdefault('GIT_USERNAME', self.get_env_variable("GIT_USERNAME"))
        settings.setdefault('GIT_PASSWORD', self.get_env_variable("GIT_PASSWORD"))

        logger = logging.getLogger("repo.RepoAppConfig")
        try:
            RepoAppConfig.update_repository(settings, logger)
        except:
            logger.error("Cant create init git repository!")

    @staticmethod
    def update_repository(settings, logger):
        repo_path = settings.get("GIT_REPO_PATH")
        logger.info("Temp repository path: " + repo_path)
        if not os.path.exists(repo_path):
            logger.info("Temp repo path doesn't exists. Creating new one.")
            os.makedirs(repo_path)
        else:
            logger.info("Temp repo path exists. Clean up...")
            subprocess.run("rm -rf %s" % repo_path, shell=True)

        logger.info("Init repo.")
        subprocess.run("git init", shell=True, cwd=repo_path)

        logger.info("Attach remote repository.")
        url = RepoAppConfig.generate_not_secured_url(settings)
        subprocess.run("git remote add origin %s" % url, shell=True, cwd=repo_path)

        logger.info("Fetch latest data from git.")
        subprocess.run("git fetch --depth=1 origin %s" % settings.get("GIT_WORKING_BRANCH"), shell=True, cwd=repo_path)

    @staticmethod
    def generate_not_secured_url(settings):
        # ! Refactor on ssh key or tokens!
        credentials = settings.get("GIT_USERNAME") + ":" + settings.get("GIT_PASSWORD")

        repo = settings.get("GIT_REPO_URL")
        index = repo.find("://") + 3
        output_line = repo[:index] + credentials + "@" + repo[index:]
        return output_line

    @staticmethod
    def get_env_variable(variable):
        value = os.getenv(variable)
        if not value:
            return ""
        return value
