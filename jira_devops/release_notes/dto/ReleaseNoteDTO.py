from typing import List

from jira_devops.release_notes.dto.TicketReleaseNoteDTO import TicketReleaseNoteDTO


class ReleaseNoteDTO:
    __slots__ = "id", "ticket_notes"

    def __init__(self, release_id: str, ticket_notes: List[TicketReleaseNoteDTO]) -> None:
        self.id = release_id
        self.ticket_notes = ticket_notes
