from django.views.generic import TemplateView

from jira_devops.jira.search.ReleaseDao import release_dao
from jira_devops.release_notes.ReleaseNotes import ReleaseNotes
from jira_devops.release_notes.dto.TicketReleaseNoteDTO import TicketReleaseNoteDTO


class HomeView(TemplateView):
    template_name = "layouts/base_frame.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        context["build_page_title"] = "Metrics"
        return context


class ReleaseView(TemplateView):
    template_name = "frames/release_notes.html"

    def get_context_data(self, **kwargs):
        context = super(ReleaseView, self).get_context_data(**kwargs)

        release_id = self.request.GET.get('version')
        release_notes = []
        if release_id:
            context["build_page_title"] = release_id + " Release Notes"
            release_notes.append(self.release_notes_with_clean_up(release_id))
        else:
            context["build_page_title"] = "Release Notes"

            unreleased_versions = release_dao.find_unreleased_versions()
            for release_version in reversed(unreleased_versions):
                release_notes.append(self.release_notes_with_clean_up(release_version))

        context["release_notes"] = release_notes

        return context

    def release_notes_with_clean_up(self, release_id):
        release_note = ReleaseNotes(release_id).generate()
        ticket_notes = release_note.ticket_notes
        cleaned_ticket_notes = [x for x in ticket_notes if not self.useless_note(x)]
        return ReleaseNotes(release_id, cleaned_ticket_notes)

    @staticmethod
    def useless_note(ticket_note: TicketReleaseNoteDTO):
        if ticket_note.special:
            return False
        elif ticket_note.update:
            return False
        elif ticket_note.impex:
            return False
        elif ticket_note.manual:
            return False

        return True
