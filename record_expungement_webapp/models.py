# from django.db import models


class Name:
    def __init__(self, first, middle, last):
        self.first = first
        self.middle = middle  # optional
        self.last = last


# START RAP SHEET MODEL CLASSES

class ProbationModification:
    def __init__(self):
        self.type = None  # Either MODIFIED/EXTENDED or REINSTATED
        self.date = None  # datetime.date
        self.new_duration = None  # datetime.timedelta
        self.description = None  # String, i.e. "6 MS PROB TERMINATES ON RLSE, 6 MS JL CS"


class Charge:
    def __init__(self):
        self.offense_id = None  # i.e. "11352 HS"
        self.offense_description = None  # i.e. "TRANSPORT/SELL NARCOTIC/CNTL SUB"
        self.type_of_crime = None  # enum, either F (felony) or M (misdemeanor)


class Arrest:
    def __init__(self):
        self.arrest_id = None  # Next to CNT001
        self.name_as_charged_id = None  # Index in the names_as_charged list
        self.date = None  # datetime.date
        self.city = None  # String
        self.charges = []  # List of Charge, index denotes count number (CNT: 001, etc)


class Disposition:
    def __init__(self):
        self.crime = None  # Charge
        self.result = None  # String: CHARGED, DISMISSED, ETC


class CaseResult:
    def __init__(self):
        self.arrest = None  # Arrest
        self.case_id = None  # String, i.e. NM239120A
        self.county = None  # String
        self.dispositions = []  # list of Disposition


class Event:
    def __init__(self):
        self.arrest = None  # Arrest
        self.case_result = None  # CaseResult
        self.probation_modifications = []  # List ProbationModification
        self.county = None  # same information as in the CaseResult


class RAPSheet:
    def __init__(self):
        self.names_as_charged = []  # map of number (i.e. 001) to Name
        self.dob = None  # datetime.date
        self.sex = None  # M/F
        self.events = []  # list of Event


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
        # ... Fill out the rest #

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
    def generate(personal_history, offense_index):  # ==> saves PDF
        raise NotImplementedError


class CR181Factory:
    def __init__(self):
        raise ValueError("Don't construct me")

    @staticmethod
    def generate(personal_history, offense_index):
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
    def generate(personal_history, offense_index):
        raise NotImplementedError
