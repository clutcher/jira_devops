from typing import List

from django.conf import settings
from jira import Issue

from jira_devops.jira.JiraClient import JiraClient, jira_client


class IssueDao:

    def __init__(self, search_client: JiraClient) -> None:
        self.search_client = search_client.get_client()

    def find_by_release(self, release_name: str) -> List[Issue]:
        return self.search_client.search_issues("fixVersion='" + release_name + "'")


issue_dao = IssueDao(jira_client)
