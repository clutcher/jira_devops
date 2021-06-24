import subprocess

from django.conf import settings


class RepoFilesService:

    @staticmethod
    def get_file_names_from_repository(grep_filter, branch_name=settings.GIT_CURRENT_BRANCH):

        command = ("git ls-tree -r origin/" + branch_name + " --name-only | grep %s") % grep_filter

        try:
            process = subprocess.run(command, shell=True, capture_output=True, cwd=settings.GIT_REPO_PATH)
        except:
            return []

        result = process.stdout

        file_names = []
        if result:
            file_names_in_bytes = result.splitlines()
            for file_name in file_names_in_bytes:
                file_names.append(str(file_name, "utf-8"))

        return file_names
