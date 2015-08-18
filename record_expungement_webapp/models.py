# from django.db import models


class Name:
    def __init__(self, first=None, middle=None, last=None):
        self.first = first
        self.middle = middle  # optional
        self.last = last


class Address:
    def __init__(self, address=None, city=None, state=None, zip_code=None):
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code


class Job:
    def __init__(self, job_title=None, employer_name=None, employer_address=None):
        self.job_title = job_title
        self.employer_name = employer_name
        self.employer_address = employer_address

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


class Incarceration:
    def __init__(self):
        self.type = None  # IncarcerationType
        self.duration = None  # datetime.timedelta


# Not all of these should be
class Sentence:
    def __init__(self):
        self.probation_duration = None  # optionally, datetime.timedelta
        self.incarceration = None  # optionally, Incarceration
        self.fine = None  # bool - If a fine exists, can't determine if a declaration is needed (need to know if


# I.e. the court decision
class Disposition:
    def __init__(self):
        self.disposition_decision = None  # DispositionDecision
        self.conviction_status = None  # TypeOfCrime


class ProbationModification:
    def __init__(self):
        self.type = None  # Either MODIFIED/EXTENDED or REINSTATED
        self.date = None  # datetime.date
        self.new_duration = None  # datetime.timedelta
        self.description = None  # String, i.e. "6 MS PROB TERMINATES ON RLSE, 6 MS JL CS"


class Offense:
    def __init__(self):
        self.offesnse_code = None  # String - HS or VC
        self.offense_id = None  # i.e. "11352" or "11377(A)"
        self.offense_description = None  # i.e. "TRANSPORT/SELL NARCOTIC/CNTL SUB"
        self.eligible_for_reduction = None  # bool
        self.eligible_for_dismissal = None  # bool - is this crime on the list of crimes that can't be dismissed?


class Count:
    def __init__(self):
        self.offense = None  # Offense
        self.disposition = None  # Disposition
        self.needs_declaration_reasons = []  # List of NeedDeclarationReason
        self.ineligible_for_expungement_reasons = []  # list of IneligibilityReason


class ArrestInfo:
    def __init__(self):
        self.arrest_id = None  # Next to CNT001
        self.name_as_charged_id = None  # Index in the names_as_charged list
        self.date = None  # datetime.date
        self.city = None  # String


class CaseInfo:
    def __init__(self):
        self.case_id = None  # String, i.e. NM239120A
        self.county = None  # String
        self.counts = []  # List of Count
        self.sentence = None  # optionally, Sentence - if any of the counts were CONVICTED


class Event:
    def __init__(self):
        super(Event, self).__init__()
        self.arrest_info = None  # ArrestInfo
        self.case_info = None  # CaseInfo
        self.probation_modifications = []  # List ProbationModification
        self.listed_dob = None  # datetime.date


class RAPSheet:
    def __init__(self):
        super(RAPSheet, self).__init__()
        self.names_as_charged = []  # map of number (i.e. 001) to Name
        self.dob = None  # datetime.date - NOTE: The DOB on a criminal event TRUMPS this DOB if they are different
        self.sex = None  # M/F
        self.events = []  # list of Event
        self.needs_declaration = None


# OTHER PERSONAL INFORMATION
class StateBenefit:
    FOOD_STAMPS = 0
    SUPP_SEC_INC = 1
    SSP = 2
    MEDI_CAL = 3
    COUNTY_RELIEF_OR_GEN_ASSIST = 4
    IHSS = 5
    CALWORKS_OR_TRIBAL_TANF = 6
    CAPI = 7

    def __init__(self, benefit):
        self.benefit = benefit


class MonthlyIncomeSource:
    def __init__(self):
        self.job_title = None
        self.monthly_income = None


class WageEarner:
    def __init__(self):
        self.name = None  # Name
        self.age = None  # int in years
        self.relationship = None  # String (mother, father, etc...)
        self.gross_monthly_income = None  # int in dollars


class Expense:
    def __init__(self):
        self.recipient = None  # String
        self.amount = None  # int (dollars)


class AssetValue:
    def __init__(self):
        self.fair_market_value = None  # int (dollars)
        self.amount_still_owed = None  # int (dollars)


class BankAccount:
    def __init__(self):
        self.recipient = None  # String
        self.amount = None  # int (dollars)


class Vehicle:
    def __init__(self):
        self.make_and_year = None  # String
        self.asset_value = None  # AssetValue


class RealEstate:
    def __init__(self):
        self.address = None  # String
        self.asset_value = None  # AssetValue


class PersonalProperty:
    def __init__(self):
        self.description = None  # String
        self.asset_value = None  # AssetValue


class MoneyAndProperty:
    def __init__(self):
        self.total_cash = None  # int (dollars)
        self.bank_accounts = []  # BankAccount
        self.vehicles = []  # List VehicleInfo
        self.real_estate = []  # List RealEstate
        self.other_property = []  # List Property


class MonthlyDeductionsAndExpenses:
    def __init__(self):
        self.payroll_deduction = []  # List Expense
        self.rent_or_house_payment = None  # int (dollars)
        self.food_and_household_supplies = None  # int (dollars)
        self.utilities_and_telephone = None  # int (dollars)
        self.clothing = None  # int (dollars)
        self.laundry_and_cleaning = None  # int (dollars)
        self.medical_and_dental = None  # int (dollars)
        self.insurance = None  # int (dollars)
        self.school_and_child_care = None  # int (dollars)
        self.child_or_spousal_support = None  # int (dollars)
        self.car_and_transporation = None  # int (dollars)
        self.installment_payments = []  # list Expense
        self.wages_witheld_by_court_order = None  # int (dollars)
        self.other_monthly_expenses = []  # List Expense


class FinancialInfo:
    def __init__(self):
        # FW001 Section 2
        self.job = None  # Job

        # FW001 Section 5a
        self.benefits_received_from_state = []  # List of StateBenefit (i.e. int)

        # FW001 Section 5b
        self.family_size = None  # int
        self.total_family_income = None  # int - in dollars

        # FW001 Section 6
        self.fees_have_been_waived_for_this_case_recently = None  # bool, annotated after the fact

        # The info below is only filled out if

        # FW001 Section 7
        self.income_changes_significantly_month_to_month = None  # bool

        # FW001 Section 8
        self.monthly_income_sources = []  # List MonthlyIncomeSource

        # FW003 Section 9
        self.other_household_wage_earner = []  # List WageEarner

        # FW003 Section 10
        self.money_and_property = None  # MoneyAndProperty

        # FW003 Section 11
        self.monthly_deductions_and_expenses = None  # MonthlyDeductionsAndExpenses


class PersonalHistory:
    def __init__(self, rap_sheet):
        self.name = None  # Name
        self.address = None  # Address
        self.email = None  # String
        self.phone_number = None  # String
        self.financial_information = None  # FinancialInfo
        self.rap_sheet = rap_sheet  # RAPSheet

# CLASSES FOR PDF GENERATION


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
