import re
from collections import defaultdict

from jira_devops.repo.RepoFilesService import RepoFilesService


class TicketReleaseNoteDTO:
    __slots__ = "id", "update", "impex", "impex_files_map", "manual", "special"

    def __init__(self, ticket_id: str, update, impex, manual, special: str) -> None:
        self.id = ticket_id
        self.special = special

        self.update = self.convert_to_valid_boolean(update)
        self.impex = self.convert_to_valid_boolean(impex)
        self.manual = self.convert_to_valid_boolean(manual)

        impex_files = RepoFilesService.get_file_names_from_repository(ticket_id)
        if impex_files:
            impex_release_map = defaultdict(list)
            for file_name in impex_files:
                version = re.search(r"v([\d.]+)", file_name).group(1)
                impex_release_map[version].append(file_name)

            self.impex_files_map = dict(impex_release_map)
        else:
            self.impex_files_map = {}

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

    @staticmethod
    def convert_to_valid_boolean(value):
        if value is None:
            return False
        elif isinstance(value, list):
            list_value = value[0]
            if hasattr(list_value, "value"):
                string_value = list_value.value
                if string_value == "Yes":
                    return True
        elif isinstance(value, bool):
            return value
        return False
