from django.core.management.base import BaseCommand

from jira_devops.repo.RepoFilesService import RepoFilesService


class UpdateRepositoryCommand(BaseCommand):
    help = 'Fetch git from remote'

    def handle(self, *args, **options):
        RepoFilesService.fetch_latest_data_from_remote_repository()
