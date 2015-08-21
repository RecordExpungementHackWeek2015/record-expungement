from form_util import FormUtil, FormModel
from county_court_info import SanMateoCountyCourt
from models import PersonalHistory, Event


class FW003Model(FormModel):
    def __init__(self):
        raise ValueError("Don't construct me")

    @staticmethod
    def get_name():
        return "cr_180"

    @staticmethod
    def get_output_file_name():
        return "cr_180.pdf"

    @staticmethod
    def get_fields(ph, event):
        """
        :type ph: PersonalHistory
        :type event: Event
        """
        return [
            ("1a", ph.name,),
            ("1b", ph.address.address),
            ("1c", ph.address.city),
            ("1d", ph.address.state),
            ("1e", ph.address.zip_code),
            ("2", "N/A"),  # Lawyer, if person has one
            ("3", SanMateoCountyCourt.mailing_address_multiline_str()),
            ("4", event.associated_cases[0].case_id),
            ("5", FormUtil.short_case_name(ph, event)),
        ]
