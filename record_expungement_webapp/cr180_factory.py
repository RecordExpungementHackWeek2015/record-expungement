from models import PersonalHistory, Event, CrimeCategory, IncarcerationType
from form_util import FormUtil, FormModel
import datetime


class CR180Model(FormModel):
    def __init__(self):
        super(CR180Model, self).__init__()
        raise ValueError("Don't construct me")

    @staticmethod
    def _offenses_table(event):
        """
        :type event: Event
        """

        # TOD0: Actually flesh this out
        table_fields = []

        for i, count in enumerate(event.associated_cases[0].counts):
            table_fields.extend([("4b%(i)sa" % {'i': i}, count.offense.description),
                                 ("4b%(i)sb" % {'i': i}, count.offense.code),
                                 ("4b%(i)sc" % {'i': i}, count.offense.offense_id),
                                 ("4b%(i)sd" % {'i': i}, count.disposition.crime_category),
                                 ("4b%(i)se" % {'i': i}, count.offense.eligible_for_reduction)])

        return table_fields

    @staticmethod
    def _petition_categorization(ph, event):
        """
        :type ph: PersonalHistory
        :type event: Event
        """

        # If there is a felony with < 1 year OR a misdemeanor (both with probation), check 2.
        #   2a = completed probation
        #   TODO - ENCODE THESE DISPOSITIONS IN THE MODEL!
        #   2b = probation terminated early (says this on the RAP sheet as a disposition)
        #   2c = didn't complete probation
        #
        # If there are no misdemeanors or felonies (i.e. just infractions), check 3.
        #   3a = this is the last conviction EVER
        #   3b = there are more convictions after this one
        #
        # If there is a felony AND there is greater than one year jail time, check 4.
        #   4a = released from jail more than a year ago if there was some probation
        #   4b = released from jail more than two years ago if there was no probation
        #
        # You can check 2 and 4 at the same time

        category_checks = []

        felonies = event.get_eligible_convictions_of_type(CrimeCategory.FELONY)
        misdemeanors = event.get_eligible_convictions_of_type(CrimeCategory.MISDEMEANOR)
        infractions = event.get_eligible_convictions_of_type(CrimeCategory.INFRACTION)

        # Section 2
        if felonies or misdemeanors:
            category_checks.append(("5", True))
            if event.completed_probation():
                category_checks.append(("5a", True))  # 2a
            elif event.probation_terminated_early():
                category_checks.append(("5b", True))  # 2b
            else:  # Didn't complete probation
                category_checks.append(("5c", True))  # 2c

            category_checks.append(("10a", True))
        # Section 3
        else:
            assert infractions
            category_checks.append(("6", True))
            if ph.rap_sheet.is_last_arrest(event):
                category_checks.append(("6a", True))  # 3a
            else:
                category_checks.append(("6b", True))  # 3b

            category_checks.append(("10b", True))  # 3c

        # Section 4
        if felonies:
            incarceration = event.associated_cases[0].sentence.incarceration
            probation = event.associated_cases[0].sentence.probation_duration
            has_jail = incarceration.type == IncarcerationType.JAIL if incarceration else False
            is_one_year = incarceration.duration >= datetime.timedelta(days=365) if incarceration else False
            is_two_years = incarceration.duration >= datetime.timedelta(days=2*365) if incarceration else False

            checks = []
            if felonies and probation and has_jail and is_one_year:
                checks.append(("9a", True))  # 4a
            elif felonies and not probation and has_jail and is_two_years:
                checks.append(("9b", True))  # 4b

            if checks:
                category_checks.extend(checks + [("9", True), ("10c", True)])
        return category_checks

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
        header = FormUtil.cr_180_header(ph, event)

        table = CR180Model._offenses_table(event)
        offense_date = [("4a", FormUtil.case_date(event))]
        categorization = CR180Model._petition_categorization(ph, event)
        header_2 = FormUtil.cr_180_header_2(ph, event)

        page_2_footer = [
            ("11", FormUtil.today_date_str()),
            ("12", ph.address.to_str_one_line()),
            ("13", ph.address.city),
            ("14", ph.address.state),
            ("15", ph.address.zip_code),
        ]

        return header + offense_date + table + categorization + header_2 + page_2_footer
