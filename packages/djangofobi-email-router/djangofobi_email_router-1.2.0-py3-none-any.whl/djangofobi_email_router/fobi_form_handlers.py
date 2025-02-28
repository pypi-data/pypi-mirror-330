# Django
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

# Third party
from fobi.base import (
    FormHandlerPlugin,
    form_handler_plugin_registry,
    get_processed_form_data,
)
from fobi.contrib.plugins.form_handlers.mail.helpers import send_mail
from fobi.contrib.plugins.form_handlers.mail.mixins import MailHandlerMixin
from fobi.helpers import safe_text

# Local application / specific library imports
from .forms import MailForm

# Project
from djangofobi_email_router.constants import SPAMMER_TEXT


class RecipientChoiceHandlerPlugin(FormHandlerPlugin, MailHandlerMixin):
    """Handler plugin that allow users to select recipient of the form."""

    uid = "email_router"
    name = _("E-mail router")
    allow_multiple = False
    form = MailForm

    def send_email(self, rendered_data, files):
        str_rendered_data = "".join(rendered_data)

        for spammer_text in SPAMMER_TEXT:
            if spammer_text in str_rendered_data:
                print(f"Spammer text found, not sending email: {spammer_text}")
                return

        to_emails = self.data.to_emails.split("\n")

        def parse_line(line):
            bits = list(map(str.strip, line.split(",")))
            return bits[0], bits[1:]

        to_emails_dict = dict(map(parse_line, to_emails))

        choice_field = self.data.to_email_choice_field
        choices = self.form_data.getlist(choice_field)

        assert choices != [""] and choices != []

        to_emails = []
        for choice in choices:
            to_emails.extend(to_emails_dict[choice])

        # Remove duplicates
        to_emails = list(set(to_emails))

        send_mail(
            safe_text(self.data.subject),
            "{}\n\n{}".format(safe_text(self.data.body), "".join(rendered_data)),
            self.data.from_email,
            to_emails,
            fail_silently=False,
            attachments=files.values(),
        )

    def run(self, form_entry, request, form, form_element_entries=None):
        """Run.
        :param fobi.models.FormEntry form_entry: Instance of
            ``fobi.models.FormEntry``.
        :param django.http.HttpRequest request:
        :param django.forms.Form form:
        :param iterable form_element_entries: Iterable of
            ``fobi.models.FormElementEntry`` objects.
        """
        base_url = self.get_base_url(request)

        self.form_data = form.data

        # Clean up the values, leave our content fields and empty values.
        field_name_to_label_map, self.cleaned_data = get_processed_form_data(
            form, form_element_entries
        )

        rendered_data = self.get_rendered_data(
            self.cleaned_data, field_name_to_label_map, base_url
        )

        files = self._prepare_files(request, form)

        self.send_email(rendered_data, files)

    def plugin_data_repr(self):
        """Human readable representation of plugin data.
        :return string:
        """
        to_emails = self.data.to_emails

        context = {
            "to_emails": to_emails,
            "subject": safe_text(self.data.subject),
        }
        return render_to_string("email_router/plugin_data_repr.html", context)


form_handler_plugin_registry.register(RecipientChoiceHandlerPlugin)
