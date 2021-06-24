from django.conf import settings

from jira_devops.release_notes.utils import ConverterUtils
from jira_devops.repo.RepoFilesService import RepoFilesService


class TicketReleaseNoteDTO:
    __slots__ = "id", "responsible_person", "update", "impex", "impex_files_map", "manual", "special"

    def __init__(self, ticket_id: str, responsible_person, update, impex, manual, special: str) -> None:
        self.id = ticket_id
        self.special = special
        self.responsible_person = responsible_person

        self.update = ConverterUtils.convert_to_valid_boolean(update)
        self.impex = ConverterUtils.convert_to_valid_boolean(impex)
        self.manual = ConverterUtils.convert_to_valid_boolean(manual)

        impex_files = RepoFilesService.get_file_names_from_repository(ticket_id)
        future_impex_files = RepoFilesService.get_file_names_from_repository(ticket_id, settings.GIT_FUTURE_BRANCH)

        version_map = ConverterUtils.create_file_version_map(impex_files)
        future_version_map = ConverterUtils.create_file_version_map(future_impex_files, settings.GIT_FUTURE_BRANCH)
        self.impex_files_map = ConverterUtils.merge_version_maps(version_map, future_version_map)

    def useless_note(self):
        if self.special:
            return False
        elif self.update:
            return False
        elif self.impex:
            return False
        elif self.manual:
            return False
        elif self.impex_files_map:
            return False

        return True
