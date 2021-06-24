import re
from collections import defaultdict

from django.conf import settings


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


def create_file_version_map(files, prefix=None):
    version_map = defaultdict(list)

    if files:
        for file_name in files:
            version = get_version_from_file_name(file_name)
            if prefix:
                version_file_name = prefix + ":" + file_name.removeprefix(settings.FILE_CLEAN_UP_PREFIX)
            else:
                version_file_name = file_name.removeprefix(settings.FILE_CLEAN_UP_PREFIX)
            version_map[version].append(version_file_name)

    return version_map


def get_version_from_file_name(file_name):
    search = re.search(r"v([\d.]+)", file_name)
    if search is not None:
        return search.group(1)
    else:
        return "undefined"


def merge_version_maps(current, future):
    def already_added(file, current_results):
        for current_file in current_results:
            if current_file in file:
                return True
        return False

    result = defaultdict(list)
    for key, value in current.items():
        result[key].extend(value)
    for key, value in future.items():
        current_results = result[key]
        if not current_results:
            current_results.extend(value)
        else:
            for file in value:
                if not already_added(file, current_results):
                    current_results.append(file)

    return dict(result)
