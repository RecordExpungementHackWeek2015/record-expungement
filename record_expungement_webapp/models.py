# from django.db import models
import datetime


class Name:
    def __init__(self, last=None, first=None, middle=None):
        """
        :type last: str
        :type middle: str
        :type first: str
        """
        self.first = first
        self.middle = middle  # optional
        self.last = last

    def __str__(self):
        return self.first + " " + (self.middle + " " if self.middle else "") + self.last


class Address:
    def __init__(self, address=None, city=None, state=None, zip_code=None):
        """
        :type zip_code: str
        :type state: str
        :type city: str
        :type address: str
        """
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code

    def to_str_multiline(self):
        return self._to_str("\n")

    def to_str_one_line(self):
        return self._to_str(" ")

    def _to_str(self, line_delimiter):
        """
        :type line_delimiter: str
        """
        return self.address + line_delimiter + self.city + ", " + self.state + " " + self.zip_code


class Job:
    def __init__(self, job_title=None, employer_name=None, employer_address=None):
        """
        :type employer_address: Address
        :type employer_name: str
        :type job_title: str
        """
        self.job_title = job_title
        self.employer_name = employer_name
        self.employer_address = employer_address

# START RAP SHEET MODEL CLASSES


class IneligibilityReason:
    def __init__(self):
        raise NotImplementedError

    NOT_IN_SAN_MATEO_COUNTY = "OFFENSE DIDN'T TAKE PLACE IN ELIGIBLE COUNTY"
    PRISON_TIME_GRANTED = "PRISON TIME GRANTED"
    OFFENSE_INELIGIBLE_FOR_EXPUNGMENT = "INELIGIBLE"
    PROBATION_NOT_PART_OF_SENTENCE = "PROBATION NOT PART OF SENTENCE"
    TOO_RECENT_FOR_FELONY_WITH_LOTS_OF_JAIL_TIME = "TOO RECENT FOR FELONY WITH LOTS OF JAIL TIME"


class NeedsDeclarationReason:
    def __init__(self):
        raise NotImplementedError

    OFFENSE_IS_A_FELONY = "OFFENSE IS A FELONY"
    PROBATION_VIOLATED = "PROBATION VIOLATED"


# I.e. the court decision
class DispositionDecision:
    def __init__(self):
        raise NotImplementedError

    CONVICTED = "convicted"
    DISMISSED = "dismissed"


class CrimeCategory:
    def __init__(self):
        raise NotImplementedError

    FELONY = "FELONY"
    MISDEMEANOR = "MISDEMEANOR"
    INFRACTION = "INFRACTION"  # These don't matter except for it means they violated probation


class IncarcerationType:
    def __init__(self):
        raise NotImplementedError

    PRISON = "PRISON"
    JAIL = "JAIL"


class Incarceration:
    def __init__(self, incarceration_type, duration):
        """
        :type duration: datetime.timedelta
        :type incarceration_type: IncarcerationType
        """
        self.type = incarceration_type
        self.duration = duration


# Not all of these should be
class Sentence:
    def __init__(self, probation_duration, incarceration, fine):
        """
        :type fine: bool
        :type incarceration: Incarceration
        :type probation_duration: datetime.timedelta
        """
        assert probation_duration or incarceration or fine
        self.probation_duration = probation_duration  # optional
        self.incarceration = incarceration  # optional
        self.fine = fine  # If a fine exists, can't determine if a declaration is needed


# I.e. the court decision
class Disposition:
    def __init__(self, disposition_decision, crime_category):
        """
        :type crime_category: CrimeCategory
        :type disposition_decision: DispositionDecision
        """
        self.disposition_decision = disposition_decision
        self.crime_category = crime_category  # called conviction status on the RAP sheet


class ProbationModification:
    def __init__(self, mod_type, date, new_duration, description):
        """
        :type mod_type: str
        :type date: datetime.date
        :type new_duration: datetime.timedelta
        :type description: str
        """
        self.type = mod_type  # Either MODIFIED/EXTENDED or REINSTATED
        self.date = date
        self.new_duration = new_duration
        self.description = description  # i.e. "6 MS PROB TERMINATES ON RLSE, 6 MS JL CS"


class Offense:
    def __init__(self, code, offense_id, description):
        """
        :type code: str
        :type offense_id: str
        :type description: str
        """
        self.code = code  # str - HS or VC
        self.offense_id = offense_id  # i.e. "11352" or "11377(A)"
        self.description = description  # i.e. "TRANSPORT/SELL NARCOTIC/CNTL SUB"

        # FILL_ME_IN_LATER
        self.eligible_for_reduction = None  # bool
        self.eligible_for_dismissal = None  # bool - is this on list of crimes that can't be dismissed?


class Count:
    def __init__(self, offense, disposition):
        """
        :type offense: Offense
        :type disposition: Disposition
        """
        self.offense = offense  # Offense
        self.disposition = disposition  # Disposition

        # FILL_ME_IN_LATER
        self.ineligible_for_expungement_reasons = []  # list of IneligibilityReason

    # List reasons
    def is_eligible_for_expungement(self):
        return not self.ineligible_for_expungement_reasons


class ArrestInfo:
    def __init__(self, arrest_id, name_as_charged_id, date, city):
        """
        :type arrest_id: str
        :type name_as_charged_id: int
        :type date: datetime.date
        :type city: str
        """
        self.arrest_id = arrest_id  # Next to CNT001
        self.name_as_charged_id = name_as_charged_id  # Index in the names_as_charged list
        self.date = date  # datetime.date
        self.city = city  # str


class CaseInfo:
    def __init__(self, case_id, date, county, counts, sentence=None):
        """
        :type case_id: str
        :type date: datetime.date
        :type county: str
        :type counts: list[Count]
        :type sentence: Sentence
        """
        self.case_id = case_id
        self.date = date
        self.county = county
        self.counts = counts  # list of Count
        self.sentence = sentence  # optional, present if any of the counts were CONVICTED


class Event:
    def __init__(self, arrest_info, listed_dob, associated_cases=None, probation_modifications=None):
        """
        :type arrest_info: ArrestInfo
        :type listed_dob: datetime.date
        :type associated_cases: list[CaseInfo]
        :type probation_modifications: list[ProbationModification]
        """
        self.arrest_info = arrest_info
        self.listed_dob = listed_dob
        self.associated_cases = associated_cases  # list of CaseInfo
        self.probation_modifications = probation_modifications  # list of ProbationModification

        # FILL_ME_IN_LATER
        self.needs_declaration_reasons = []  # List of NeedDeclarationReason

    # Display star next to event. List out reasons.
    def needs_declaration(self):
        return bool(self.needs_declaration_reasons)

    def completed_probation(self):
        return NeedsDeclarationReason.PROBATION_VIOLATED in self.needs_declaration_reasons

    # TODO: ACTUALLY IMPLEMENT THIS
    def probation_terminated_early(self):
        return False and self

    def get_convictions_of_type(self, crime_category):
        """
        :type crime_category: CrimeCategory
        :rtype : list[Count]
        """
        convictions = []
        for case_info in self.associated_cases:
            for count in case_info.counts:
                d = count.disposition
                if d.disposition_decision == DispositionDecision.CONVICTED and d.crime_category == crime_category:
                    convictions.append(count)
        return convictions

    def get_eligible_convictions_of_type(self, crime_category):
        return [count for count in self.get_convictions_of_type(crime_category)
                if not count.ineligible_for_expungement_reasons]

    def has_eligible_convictions(self):
        return self.associated_cases and [count for count in self.associated_cases[0].counts
                                          if not count.ineligible_for_expungement_reasons]


class RAPSheet:
    def __init__(self, names_as_charged, dob, sex, events):
        """
        :type names_as_charged: list[Name]
        :type dob: datetime.date
        :type sex: str
        :type events: list[Event]
        """
        self.names_as_charged = names_as_charged  # list of Name
        self.dob = dob  # NOTE: The DOB on a criminal event TRUMPS this DOB if they are different
        self.sex = sex  # M/F
        self.events = events  # list of Event

    # If True, display warning at top
    def needs_declaration(self):
        if not self.events:
            return False
        return any(event.needs_declaration for event in self.events)

    def is_last_arrest(self, event):
        i = self.events.index(event)
        return i - 1 == len(self.events)


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
    def __init__(self, job_title=None, monthly_income=None):
        """
        :type job_title: str
        :type monthly_income: int
        """
        self.job_title = None
        self.monthly_income = None


class WageEarner:
    def __init__(self):
        self.name = None  # Name
        self.age = None  # int in years
        self.relationship = None  # str (mother, father, etc...)
        self.gross_monthly_income = None  # int in dollars


class Expense:
    def __init__(self):
        self.recipient = None  # str
        self.amount = None  # int (dollars)


class AssetValue:
    def __init__(self):
        self.fair_market_value = None  # int (dollars)
        self.amount_still_owed = None  # int (dollars)


class BankAccount:
    def __init__(self):
        self.bank_name = None  # str
        self.amount = None  # int (dollars)


class Vehicle:
    def __init__(self):
        self.make_and_year = None  # str
        self.asset_value = None  # AssetValue


class RealEstate:
    def __init__(self):
        self.address = None  # str
        self.asset_value = None  # AssetValue


class PersonalProperty:
    def __init__(self):
        self.description = None  # str
        self.asset_value = None  # AssetValue


class MoneyAndProperty:
    def __init__(self, real_estate=None):
        """
        :type real_estate: list[RealEstate]
        """
        self.total_cash = None  # int (dollars)
        self.bank_accounts = []  # BankAccount
        self.vehicles = []  # List VehicleInfo
        self.real_estate = real_estate  # List RealEstate
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
    def __init__(self, job=None, monthly_income_sources=None, other_household_wage_earners=None,
                 money_and_property=None, monthly_deductions_and_expenses=None):
        """

        :type monthly_deductions_and_expenses: MonthlyDeductionsAndExpenses
        :type money_and_property: MoneyAndProperty
        :type other_household_wage_earners: list[WageEarner]
        :type monthly_income_sources: list[MonthlyIncomeSource]
        :type job: Job
        """

        if not monthly_income_sources:
            monthly_income_sources = []
        if not other_household_wage_earners:
            other_household_wage_earners = []
        if not money_and_property:
            money_and_property = []

        # FW001 Section 2
        self.job = job  # Job

        # FW001 Section 5a
        # if non-empty don't show page 2
        self.benefits_received_from_state = []  # List of StateBenefit (i.e. int)

        # FW001 Section 5b
        # if non-empty don't show 10, 11
        self.family_size = None  # int
        self.total_family_income = None  # int - in dollars

        # FW001 Section 6
        self.event_index_to_whether_fees_have_been_waived_recently = {}  # int to bool

        # The info below is only filled out if

        # FW001 Section 7
        self.income_changes_significantly_month_to_month = None  # bool

        # FW001 Section 8
        self.monthly_income_sources = monthly_income_sources  # List MonthlyIncomeSource

        # FW003 Section 9
        self.other_household_wage_earners = other_household_wage_earners  # List WageEarner

        # FW003 Section 10
        self.money_and_property = money_and_property  # MoneyAndProperty

        # FW003 Section 11
        self.monthly_deductions_and_expenses = monthly_deductions_and_expenses  # MonthlyDeductionsAndExpenses

    def is_monthly_income_below_threshold(self):
        return False and self  # something with family_size and total_family_income


class PersonalHistory:
    def __init__(self, rap_sheet, name=None, address=None, email=None, phone_number=None, financial_info=None):
        """
        :type rap_sheet: RAPSheet
        :type name: Name
        :type address: Address
        :type email: str
        :type phone_number: str
        :type financial_info: FinancialInfo
        """
        self.rap_sheet = rap_sheet  # RAPSheet

        self.name = name  # Name
        self.address = address  # Address
        self.email = email  # str
        self.phone_number = phone_number  # str
        self.financial_information = financial_info  # FinancialInfo
