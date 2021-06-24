import logging
import os
import subprocess

from django.conf import settings


class RepoService:

    @staticmethod
    def fetch_latest_data_from_remote_repository():
        logger = logging.getLogger("repo.RepoFilesService")
        logger.info("Start fetching latest data from git async.")
        repo_path = settings.GIT_REPO_PATH
        try:
            if os.path.exists(repo_path):
                command = "git fetch --depth=1 origin %s" % settings.GIT_CURRENT_BRANCH
                subprocess.run(command, shell=True, cwd=settings.GIT_REPO_PATH)

                command = "git fetch --depth=1 origin %s" % settings.GIT_FUTURE_BRANCH
                subprocess.run(command, shell=True, cwd=settings.GIT_REPO_PATH)
            else:
                RepoService.force_create_repository(logger)
        except:
            pass

    @staticmethod
    def force_create_repository(logger):
        def generate_not_secured_git_url():
            # ! Refactor on ssh key or tokens!
            credentials = settings.GIT_USERNAME + ":" + settings.GIT_PASSWORD

            repo = settings.GIT_REPO_URL
            index = repo.find("://") + 3
            output_line = repo[:index] + credentials + "@" + repo[index:]
            return output_line

        repo_path = settings.GIT_REPO_PATH
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
        url = generate_not_secured_git_url()
        subprocess.run("git remote add origin %s" % url, shell=True, cwd=repo_path)

        logger.info("Fetch latest data from git.")
        subprocess.run("git fetch --depth=1 origin %s" % settings.GIT_CURRENT_BRANCH, shell=True, cwd=repo_path)
        subprocess.run("git fetch --depth=1 origin %s" % settings.GIT_FUTURE_BRANCH, shell=True, cwd=repo_path)
