from django.conf import settings

from jira_devops.jira.search.IssueDao import issue_dao
from jira_devops.release_notes.dto.ReleaseNoteDTO import ReleaseNoteDTO
from jira_devops.release_notes.dto.TicketReleaseNoteDTO import TicketReleaseNoteDTO


class ReleaseNotes:

    def __init__(self, release, ticket_notes=None) -> None:
        self.release = release

        if ticket_notes is None:
            ticket_notes = []
        self.ticket_notes = ticket_notes

    def generate(self) -> ReleaseNoteDTO:
        issues = issue_dao.find_by_release(self.release)
        for issue in issues:
            requires_hac_update = getattr(issue.fields, settings.JIRA_RELEASE_FIELD_MAP["hac_update"])
            requires_impex = getattr(issue.fields, settings.JIRA_RELEASE_FIELD_MAP["need_impex"])
            requires_manual = getattr(issue.fields, settings.JIRA_RELEASE_FIELD_MAP["need_manual"])
            special_notes = getattr(issue.fields, settings.JIRA_RELEASE_FIELD_MAP["special_notes"])
            responsible_person = getattr(issue.fields, settings.JIRA_RELEASE_FIELD_MAP["responsible_person"])

            ticket_release_note = TicketReleaseNoteDTO(issue.key,
                                                       responsible_person,
                                                       requires_hac_update,
                                                       requires_impex,
                                                       requires_manual,
                                                       special_notes)
            self.ticket_notes.append(ticket_release_note)

        return ReleaseNoteDTO(self.release, self.ticket_notes)
