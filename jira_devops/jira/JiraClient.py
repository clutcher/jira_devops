from django.conf import settings
from jira import JIRA


class JiraClient:

    def __init__(self, server, username, password) -> None:
        self.client = JIRA(server=server, basic_auth=(username, password))

    def get_client(self):
        return self.client


jira_client = JiraClient(server=settings.JIRA_SERVER,
                         username=settings.JIRA_USERNAME,
                         password=settings.JIRA_PASSWORD)
