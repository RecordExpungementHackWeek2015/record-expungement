from models import PersonalHistory, Event, CrimeCategory, IncarcerationType, Count
from form_util import FormUtil


class CR180Factory:
    def __init__(self):
        raise ValueError("Don't construct me")

    @staticmethod
    def _offenses_table(event):
        """
        :type event: Event
        """

        # TOD0: Actually flesh this out
        table_fields = []

        for i, count in enumerate(event.associated_cases[0].counts):
            table_fields.extend([("4b%(i)s1" % {'i': i}, count.offense.description),
                                 ("4b%(i)s2" % {'i': i}, count.offense.code),
                                 ("4b%(i)s3" % {'i': i}, count.offense.offense_id),
                                 ("4b%(i)s4" % {'i': i}, count.disposition.crime_category),
                                 ("4b%(i)s5" % {'i': i}, count.offense.eligible_for_reduction)])

        return table_fields

    @staticmethod
    def _petition_categorization(ph, event):
        """
        :type ph: PersonalHistory
        :type event: Event
        """

        # Felony and misdemeanor together

        # If it is a felony with < 1 year OR a misdemeanor (both with probation), check 2.
        # If it is an infraction, check 3.
        # Check #4 if it is a felony AND there is greater than one year jail time.

        # 2a = completed probation

        # TODO - ENCODE THESE DISPOSITIONS IN THE MODEL!
        # 2b = probation terminated early (says this on the RAP sheet as a disposition)
        # 2c = didn't complete probation

        # 3a = this is the last conviction EVER
        # 3b = there are more convictions after this one

        # 4a = released from jail more than a year ago if there was some probation
        # 4b = released from jail more than two years ago if there was no probation

        # Felony with greater than one year jail time and a misdemeanor?

        # TODO: Figure out how to fill these out!
        # felonies =  event.get_eligible_convictions_of_type(CrimeCategory.FELONY)
        # misdemeanors = event.get_eligible_convictions_of_type(CrimeCategory.MISDEMEANOR)
        # infractions = event.get_eligible_convictions_of_type(CrimeCategory.INFRACTION)

        # if felonies:
        #     has_jail = event.associated_cases[0].sentence.incarceration == IncarcerationType.JAIL
        #
        #
        # if not felonies and not misdemeanors:
        #     assert infractions
        #      ("6",),
        #     if ph.rap_sheet.is_last_arrest(event):
        #         return [("6a", True)]
        #     else:
        #         return [("6a", True)]

        # if
        # return [
        #     ("5", ),
        #     ("5a",),
        #     ("5b",),
        #     ("5c",),
        #     ("6a",),
        #     ("6b",),
        #     ("9a",),
        #     ("9b",),
        #     ("10a",),
        #     ("10b",),
        #     ("10c",),
        # ]

        return []

    @staticmethod
    def generate(ph, event):  # ==> saves PDF
        """
        :type ph: PersonalHistory
        :type event: Event
        """
        header = FormUtil.cr_180_header(ph, event)

        table = CR180Factory._offenses_table(event)
        offense_date = [("4a", FormUtil.case_date(event))]
        categorization = CR180Factory._petition_categorization(ph, event)
        header_2 = FormUtil.cr_180_header_2(ph, event)

        page_2_footer = [
            ("11", FormUtil.today_date_str()),
            ("12", ph.address.to_str_one_line()),
            ("13", ph.address.city),
            ("14", ph.address.state),
            ("15", ph.address.zip_code),
        ]

        return header + offense_date + table + categorization + header_2 + page_2_footer
