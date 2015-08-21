from form_util import FormUtil, FormModel
from models import PersonalHistory, Event
from county_court_info import SanMateoCountyCourt


# Need to fill out the top box plus 2, 4, 5a&b, 6a for the San Mateo County POSes
class POS040Model(FormModel):
    def __init__(self):
        FormModel.__init__(self)
        raise ValueError("Don't construct me")

    @staticmethod
    def get_name():
        return "pos040"

    @staticmethod
    def get_output_file_name():
        return "pos040.pdf"

    @staticmethod
    def get_fields(ph, event):
        """
        :type ph: PersonalHistory
        :type event: Event
        """
        return [
            ("1a", FormUtil.attorney_or_party_without_attorney(ph, event)),
            ("1b", str(ph.address)),
            ("1c", ph.phone_number),
            ("1d", ph.email),
            ("1e", "Self-Represented"),
            ("2a", SanMateoCountyCourt.county_name()),
            ("2b", SanMateoCountyCourt.mailing_address().address),
            ("2d", SanMateoCountyCourt.mailing_address().city + " " + SanMateoCountyCourt.mailing_address().zip_code),
            ("3a", "THE PEOPLE OF THE STATE OF CALIFORNIA"),
            ("3b", str(FormUtil.event_to_name_as_charged(ph, event))),
            ("4a", True),
            ("5", event.associated_cases[0].case_id),
            ("6", ph.address.to_str_one_line()),
            ("7a", FormUtil.case_date(event)),
            ("7b", "CR180, CR181" + (", DECLARATION" if event.needs_declaration() else "")),
            ("8a", SanMateoCountyCourt.chief_probation_officer_name_and_title_str()),
            ("8b", True),
            ("8c", SanMateoCountyCourt.mailing_address_oneline_str()),
            ("9", True),
            ("10", FormUtil.short_case_name(ph, event)),
            ("11", event.associated_cases[0].case_id),
            ("12", FormUtil.today_date_str()),
            ("13", str(ph.name)),
        ]
