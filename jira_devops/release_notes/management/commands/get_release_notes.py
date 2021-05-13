import collections
import json

from django.core.management.base import BaseCommand

from jira_devops.jira.search.ReleaseDao import release_dao
from jira_devops.release_notes.ReleaseNotes import ReleaseNotes


def convert_to_dict(obj):
    if isinstance(obj, str):
        return obj
    elif isinstance(obj, dict):
        return dict((key, convert_to_dict(val)) for key, val in obj.items())
    elif isinstance(obj, collections.Iterable):
        return [convert_to_dict(val) for val in obj]
    elif hasattr(obj, '__dict__'):
        return convert_to_dict(vars(obj))
    elif hasattr(obj, '__slots__'):
        return convert_to_dict(dict((name, getattr(obj, name)) for name in getattr(obj, '__slots__')))
    return obj


class ReleaseNoteCommand(BaseCommand):
    help = 'Generate release notes'

    def handle(self, *args, **options):
        unreleased_versions = release_dao.find_unreleased_versions()
        notes_per_release = []
        for release_version in reversed(unreleased_versions):
            notes_per_release.append(ReleaseNotes(release_version).generate())
            self.stdout.write(self.style.SUCCESS('Prepared release notes for release %s' % release_version))
        print(json.dumps(convert_to_dict(notes_per_release), sort_keys=True, indent=4))
        self.stdout.write(self.style.SUCCESS('Done'))
