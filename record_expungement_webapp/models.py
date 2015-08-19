# from django.db import models
import datetime


class Name:
    def __init__(self, first=None, middle=None, last=None):
        """
        :type last: str
        :type middle: str
        :type first: str
        """
        self.first = first
        self.middle = middle  # optional
        self.last = last


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


class Job:
    def __init__(self, job_title=None, employer_name=None, employer_address=None):
        """
        :type employer_address: str
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

    NOT_IN_SAN_MATEO_COUNTY = "not_in_san_mateo"
    PRISON_TIME_GRANTED = "prison_time_granted"
    OFFENSE_INELIGIBLE_FOR_EXPUNGMENT = "ineligible"
    PROBATION_NOT_PART_OF_SENTENCE = "probation_not_part_of_sentence"


class NeedsDeclarationReason:
    def __init__(self):
        raise NotImplementedError

    OFFENSE_IS_A_FELONY = "offense_is_a_felony"
    PROBATION_VIOLATED = "probation_violated"


# I.e. the court decision
class DispositionDecision:
    def __init__(self):
        raise NotImplementedError

    CONVICTED = "convicted"
    DISMISSED = "dismissed"


class CrimeCategory:
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
        :type counts: list
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
        :type associated_cases: list
        :type probation_modifications: list
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

class RAPSheet:
    def __init__(self, names_as_charged, dob, sex, events):
        """
        :type names_as_charged: list
        :type dob: datetime.date
        :type sex: str
        :type events: list
        """
        self.names_as_charged = names_as_charged  # list of Name
        self.dob = dob  # NOTE: The DOB on a criminal event TRUMPS this DOB if they are different
        self.sex = sex  # M/F
        self.events = events  # list of Event

    # If True, display warning at top
    def needs_declaration(self):
        if self.events == None:
            return False
        return any(event.needs_declaration for event in self.events)


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
        self.recipient = None  # str
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
        self.event_index_to_whether_fees_have_been_waived_recently = {}  # int to bool

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
    def generate(personal_history, event_index):
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


class IneligibleOffensesModel:
    _INELIGIBLE_OFFENSES = {
        "VC": ["42002.1", "2815", "22526(A)", "22526(B)"],
        "PC": ["286(C)", "288", "288(C)", "288.5", "289(J)",
               "311.1", "311.2", "311.3", "311.11"]
    }

    _INELIGIBLE_WITH_FELONY = {
        "PC": ["261.5(D)"]
    }

    def __init__(self):
        pass

    @staticmethod
    def offense_is_ineligible(offense_code, offense_id, type_of_crime):
        """
        :rtype : bool
        :type offense_code: str
        :type offense_id: str
        :type type_of_crime: str
        """
        if type_of_crime == CrimeCategory.INFRACTION:
            return True
        if offense_code in IneligibleOffensesModel._INELIGIBLE_OFFENSES:
            if offense_id in IneligibleOffensesModel._INELIGIBLE_OFFENSES[offense_code]:
                return True
        if type_of_crime == CrimeCategory.FELONY \
                and offense_code in IneligibleOffensesModel._INELIGIBLE_WITH_FELONY:
            if offense_id in IneligibleOffensesModel._INELIGIBLE_WITH_FELONY[offense_code]:
                return True
        return False


class WobblerOffensesModel:
    _WOBBLERS = {
        "PC": ["69", "71", "72", "76", "118.1", "136.1", "136.5", "136.7", "139", "142", "146(A)", "148(D)",
               "148.1", "148.10", "149", "153", "168", "171(B)", "171(C)", "171(D)", "186.10", "192(C)(1)",
               "192.5(A)", "219.2", "241.1", "241.4", "241.7", "243(C)(1)", "243.3", "243.4", "243.6",
               "243.7", "243.9"],
        "HS": ["11377", "11379.2", "11390", "11391"],
        "VC": ["10851", "23152", "23153"]
    }

    def __init__(self):
        pass

    @staticmethod
    def offense_is_a_wobbler(offense_code, offense_id, type_of_crime):
        """
        :rtype : bool
        :type offense_code: str
        :type offense_id: str
        :type type_of_crime: str
        """
        assert type_of_crime == CrimeCategory.FELONY
        if offense_code in WobblerOffensesModel._WOBBLERS:
            return offense_id in WobblerOffensesModel._WOBBLERS[offense_code]


class ExpungementLogicEngine:
    def __init__(self, personal_history):
        """
        :type personal_history: PersonalHistory
        """
        self.personal_history = personal_history

    @classmethod
    def _annotate_count_eligibility(cls, count):
        o = count.offense
        o.eligible_for_reduction = WobblerOffensesModel.offense_is_a_wobbler(o.code,
                                                                             o.offense_id,
                                                                             count.disposition.crime_category)
        o.eligible_for_dismissal = not IneligibleOffensesModel.offense_is_ineligible(o.code,
                                                                                     o.offense_id,
                                                                                     count.disposition.crime_category)

        if not o.eligible_for_dismissal:
            count.ineligible_for_expungement_reasons.append(IneligibilityReason.OFFENSE_INELIGIBLE_FOR_EXPUNGMENT)

    @classmethod
    def _get_final_probation_period(cls, event, case_info):
        """
        :rtype : tuple
        :type event: Event
        :type case_info: CaseInfo
        """
        if not len(event.probation_modifications):
            return case_info.date + datetime.timedelta(days=1), case_info.sentence.probation_duration

        probation_modification = event.probation_modifications[-1]
        return probation_modification.date, probation_modification.new_duration

    def _violated_probation(self, event, case_info):
        """
        :rtype : bool
        :type event: Event
        :type case_info: CaseInfo
\        """
        (start_date, time_delta) = self._get_final_probation_period(event, case_info)

        for event in self.personal_history.rap_sheet.events:
            if start_date <= event.arrest_info.date < start_date + time_delta:
                return True

        return False

    def _annotate_ineligibility(self):
        for event in self.personal_history.rap_sheet.events:
            for case_info in event.associated_cases:
                for count in case_info.counts:
                    if count.disposition.disposition_decision == DispositionDecision.CONVICTED:
                        self._annotate_count_eligibility(count)

                event_ineligibility_reasons = []
                if case_info.county != "SAN MATEO":
                    event_ineligibility_reasons.append(IneligibilityReason.NOT_IN_SAN_MATEO_COUNTY)
                if not case_info.sentence.probation_duration:
                    event_ineligibility_reasons.append(IneligibilityReason.PROBATION_NOT_PART_OF_SENTENCE)
                incarceration = case_info.sentence.incarceration
                if incarceration and incarceration == IncarcerationType.PRISON:
                    event_ineligibility_reasons.append(IneligibilityReason.PRISON_TIME_GRANTED)

                for count in case_info.counts:
                    count.ineligible_for_expungement_reasons.extend(event_ineligibility_reasons)

    def _annotate_needs_declarations(self):
        for event_index, event in enumerate(self.personal_history.rap_sheet.events):
            violated_probation = False
            includes_felony = False
            for case_info in event.associated_cases:
                for count in case_info.counts:
                    if count.disposition.disposition_decision == DispositionDecision.CONVICTED:
                        if count.disposition.crime_category == CrimeCategory.FELONY:
                            includes_felony = True
                if case_info.sentence:
                    if self._violated_probation(event, case_info):
                        violated_probation = True

            if includes_felony:
                event.needs_declaration_reasons.append(NeedsDeclarationReason.OFFENSE_IS_A_FELONY)
            if violated_probation:
                event.needs_declaration_reasons.append(NeedsDeclarationReason.PROBATION_VIOLATED)

    # Annotates the rap sheet model with which charges need declarations and which ones we
    # can't generate forms for
    def annotate_rap_sheet(self):
        self._annotate_ineligibility()
        self._annotate_needs_declarations()

        # TODO: Create some sort of summary?

    def update_financial_information(self, financial_information):
        """
        :type financial_information: FinancialInfo
        """
        self.personal_history.financial_information = financial_information

    def generate_expungement_packets(self):
        for event_index, event in enumerate(self.personal_history.rap_sheet.events):
            CR180Factory.generate(self.personal_history, event_index)
            CR181Factory.generate(self.personal_history, event_index)
            FW001Factory.generate(self.personal_history, event_index)
            FW003Factory.generate(self.personal_history)
            POS040Factory.generate(self.personal_history, event_index)
