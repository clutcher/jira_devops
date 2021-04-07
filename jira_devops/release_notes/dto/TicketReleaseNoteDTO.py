class TicketReleaseNoteDTO:
    __slots__ = "id", "update", "impex", "manual", "special"

    def __init__(self, ticket_id: str, update, impex, manual, special: str) -> None:
        self.id = ticket_id

        self.update = self.convert_to_valid_boolean(update)

        self.impex = self.convert_to_valid_boolean(impex)

        self.manual = self.convert_to_valid_boolean(manual)

        self.special = special

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
