from typing import List

from django.conf import settings
from jira import Issue

from jira_devops.jira.JiraClient import JiraClient, jira_client


class ReleaseDao:

    def __init__(self, search_client: JiraClient) -> None:
        self.search_client = search_client.get_client()

    def find_unreleased_versions(self) -> List[str]:
        unreleased_releases = []

        for project_id in settings.JIRA_PROJECT_IDS:
            releases = self.search_client.project_versions(project_id)
            for release in releases:
                if not release.released and not release.archived:
                    unreleased_releases.append(release.name)

        return unreleased_releases

    def release_issues(self, release_name: str) -> List[Issue]:
        return self.search_client.search_issues("fixVersion='" + release_name + "'")


release_dao = ReleaseDao(jira_client)
