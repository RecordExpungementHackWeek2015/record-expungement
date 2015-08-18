from django.db import models


class Name(models.Model):
    def __init__(self, first, middle, last):
        super(Name, self).__init__()
        self.first = first
        self.middle = middle  # optional
        self.last = last

# START RAP SHEET MODEL CLASSES


class IneligibilityReason:
    def __init__(self):
        raise NotImplementedError

    NOT_IN_SAN_MATEO_COUNTY = "not_in_san_mateo"
    PRISON_TIME_GRANTED = "prison_time_granted"
    INELIGIBLE_FOR_EXPUNGMENT = "ineligible"
    FELONY_CANNOT_BE_REDUCED = "felony_cannot_be_reduced"
    PROBATION_NOT_PART_OF_SENTENCE = "probation_not_part_of_sentence"


class NeedsDeclarationReason:
    def __init__(self):
        raise NotImplementedError

    FELONY_ELIGIBLE_FOR_REDUCTION = "felony_eligible_for_reduction"
    PROBATION_VIOLATED = "probation_violated"


# I.e. the court decision
class DispositionDecision:
    def __init__(self):
        raise NotImplementedError

    CONVICTED = "convicted"
    DISMISSED = "dismissed"


class TypeOfCrime:
    def __init__(self):
        raise NotImplementedError

    FELONY = "felony"
    MISDEMEANOR = "misdemeanor"
    INFRACTION = "infraction"  # These don't matter except for it means they violated probation


class IncarcerationType:
    def __init__(self):
        raise NotImplementedError

    PRISON = "prison"
    JAIL = "jail"


class Incarceration(models.Model):
    def __init__(self):
        super(Incarceration, self).__init__()
        self.type = None  # IncarcerationType
        self.duration = None  # datetime.timedelta


# Not all of these should be
class Sentence(models.Model):
    def __init__(self):
        super(Sentence, self).__init__()
        self.probation_duration = None  # optionally, datetime.timedelta
        self.incarceration = None  # optionally, Incarceration
        self.fine = None  # bool - If a fine exists, can't determine if a declaration is needed (need to know if


# I.e. the court decision
class Disposition(models.Model):
    def __init__(self):
        super(Disposition, self).__init__()
        self.disposition_decision = None  # DispositionDecision
        self.conviction_status = None  # TypeOfCrime


class ProbationModification(models.Model):
    def __init__(self):
        super(ProbationModification, self).__init__()
        self.type = None  # Either MODIFIED/EXTENDED or REINSTATED
        self.date = None  # datetime.date
        self.new_duration = None  # datetime.timedelta
        self.description = None  # String, i.e. "6 MS PROB TERMINATES ON RLSE, 6 MS JL CS"


class Offense(models.Model):
    def __init__(self):
        super(Offense, self).__init__()
        self.offesnse_code = None  # String - HS or VC
        self.offense_id = None  # i.e. "11352" or "11377(A)"
        self.offense_description = None  # i.e. "TRANSPORT/SELL NARCOTIC/CNTL SUB"
        self.eligible_for_reduction = None  # bool TODO - FIX THIS TO REFLECT THAT FELONIES CAN SOMETIMES BE DISMISSED


class Count(models.Model):
    def __init__(self):
        super(Count, self).__init__()
        self.offense = None  # Offense
        self.disposition = None  # Disposition
        self.needs_declaration_reasons = []  # List of NeedDeclarationReason
        self.ineligible_for_expungement_reasons = []  # list of IneligibilityReason


class ArrestInfo(models.Model):
    def __init__(self):
        super(ArrestInfo, self).__init__()
        self.arrest_id = None  # Next to CNT001
        self.name_as_charged_id = None  # Index in the names_as_charged list
        self.date = None  # datetime.date
        self.city = None  # String


class CaseInfo(models.Model):
    def __init__(self):
        super(CaseInfo, self).__init__()        
        self.case_id = None  # String, i.e. NM239120A
        self.county = None  # String
        self.counts = []  # List of Count
        self.sentence = None  # optionally, Sentence - if any of the counts were CONVICTED


class Event(models.Model):
    def __init__(self):
        super(Event, self).__init__()
        self.arrest_info = None  # ArrestInfo
        self.case_info = None  # CaseInfo
        self.probation_modifications = []  # List ProbationModification
        self.listed_dob = None  # datetime.date


class RAPSheet(models.Model):
    def __init__(self):
        super(RAPSheet, self).__init__()
        self.names_as_charged = []  # map of number (i.e. 001) to Name
        self.dob = None  # datetime.date - NOTE: The DOB on a criminal event TRUMPS this DOB if they are different
        self.sex = None  # M/F
        self.events = []  # list of Event
        self.needs_declaration = None


# OTHER PERSONAL INFORMATION
class StateBenefit:
    FOOD_STAMPS = "Food Stamps"
    # TODO ... Fill out the rest

    def __init__(self, benefit):
        self.benefit = benefit


class FinancialInfo:
    def __init__(self):
        # info as necessary
        self.employer = None  # Employer
        self.benefits_received_from_state = []  # List of StateBenefit
        # TODO ... Fill out the rest


class PersonalHistory:
    def __init__(self, rap_sheet):
        self.name = None  # Name
        self.address = None  # Address
        self.email = None
        self.phone_number = None
        self.financial_information = None
        self.rap_sheet = rap_sheet
        # TODO ... Fill out the rest

# CLASSES FOR PDF GENERATION


# Used to navigate to the offense inside of a PersonalHistory
class OffenseIndex:
    def __init__(self, event_index, charge_index):
        self.event_index = event_index
        self.charge_index = charge_index


class CR180Factory:
    def __init__(self):
        raise ValueError("Don't construct me")

    @staticmethod
    def generate(personal_history, event_index):  # ==> saves PDF
        raise NotImplementedError


class CR181Factory:
    def __init__(self):
        raise ValueError("Don't construct me")

    @staticmethod
    def generate(personal_history, event_index):
        raise NotImplementedError


class FW001Factory:
    def __init__(self):
        raise ValueError("Don't construct me")

    @staticmethod
    def generate(personal_history):
        raise NotImplementedError


class FW003Factory:
    def __init__(self):
        raise ValueError("Don't construct me")

    @staticmethod
    def generate(personal_history):
        raise NotImplementedError


# Need to fill out the top box plus 2, 4, 5a&b, 6a for the San Mateo County POSes
class POS040Factory:
    def __init__(self):
        raise ValueError("Don't construct me")

    @staticmethod
    def generate(personal_history, event_index):
        raise NotImplementedError


class ExpungementLogicEngine:
    def __init__(self, personal_history):
        self.personal_history = personal_history

    def __requires_declaration(self, index, event):
        raise NotImplementedError

    # Annotates the rap sheet model with which charges need declarations and which ones we
    # can't generate forms for
    def annotate_rap_sheet(self):
        self.personal_history.rap_sheet.needs_declaration = False
        for index, event in enumerate(self.personal_history.rap_sheet.events):
            assert isinstance(event, Event)
            if self.__requires_declaration(index, event):
                event.needs_declaration = True
                self.personal_history.rap_sheet.needs_declaration = True

    def update_personal_information(self):
        assert isinstance(self.personal_history, PersonalHistory)
        # self.personal_history.financial_information = ???

    def generate_expungement_packets(self):
        for event_index, event in enumerate(self.personal_history.rap_sheet.events):
            CR180Factory.generate(self.personal_history, event_index)
            CR181Factory.generate(self.personal_history, event_index)
            FW001Factory.generate(self.personal_history)
            FW003Factory.generate(self.personal_history)
            POS040Factory.generate(self.personal_history, event_index)
