from django.conf import settings

from jira_devops.release_notes.utils import ConverterUtils
from jira_devops.repo.RepoFilesService import RepoFilesService


class TicketReleaseNoteDTO:
    __slots__ = "id", "responsible_person", "update", "impex", "impex_files_map", "manual_files_map", "manual", "special"

    def __init__(self, ticket_id: str, responsible_person, update, impex, manual, special: str) -> None:
        self.id = ticket_id
        self.special = special
        self.responsible_person = responsible_person

        self.update = ConverterUtils.convert_to_valid_boolean(update)
        self.impex = ConverterUtils.convert_to_valid_boolean(impex)
        self.manual = ConverterUtils.convert_to_valid_boolean(manual)

        current_file_list = RepoFilesService.get_file_names_from_repository(ticket_id)
        future_file_list = RepoFilesService.get_file_names_from_repository(ticket_id, settings.GIT_FUTURE_BRANCH)

        self.impex_files_map = ConverterUtils.create_version_map(ConverterUtils.filter_impex_files(current_file_list),
                                                                 ConverterUtils.filter_impex_files(future_file_list))

        self.manual_files_map = ConverterUtils.create_version_map(
            ConverterUtils.filter_non_impex_files(current_file_list),
            ConverterUtils.filter_non_impex_files(future_file_list))

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
