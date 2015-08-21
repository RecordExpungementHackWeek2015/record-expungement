import datetime
from special_case_offenses import WobblerOffensesModel, IneligibleOffensesModel
from county_court_info import SanMateoCountyCourt
from models import PersonalHistory, IneligibilityReason, DispositionDecision, CrimeCategory, NeedsDeclarationReason, \
    IncarcerationType, Count, CaseInfo
from cr180_model import CR180Model
from cr181_model import CR181Model
from fw001_model import FW001Model
from fw003_model import FW003Model
from pos040_model import POS040Model


class ExpungementLogicEngine:
    def __init__(self, personal_history):
        """
        :type personal_history: PersonalHistory
        """
        self.personal_history = personal_history

    @classmethod
    def _annotate_count_eligibility(cls, case_info, count):
        """
        :type case_info: CaseInfo
        :type count: Count
        """
        o = count.offense
        is_felony = count.disposition.crime_category == CrimeCategory.FELONY
        o.eligible_for_reduction = is_felony \
            and WobblerOffensesModel.offense_is_a_wobbler(o.code, o.offense_id, count.disposition.crime_category)
        o.eligible_for_dismissal = not IneligibleOffensesModel.offense_is_ineligible(o.code,
                                                                                     o.offense_id,
                                                                                     count.disposition.crime_category)

        if not o.eligible_for_dismissal:
            count.ineligible_for_expungement_reasons.append(IneligibilityReason.OFFENSE_INELIGIBLE_FOR_EXPUNGMENT)

        incarceration = case_info.sentence.incarceration
        if count.disposition.crime_category == CrimeCategory.FELONY \
                and incarceration \
                and incarceration.type == IncarcerationType.JAIL\
                and incarceration.duration >= datetime.timedelta(days=365):
            count.ineligible_for_expungement_reasons.append(
                IneligibilityReason.TOO_RECENT_FOR_FELONY_WITH_LOTS_OF_JAIL_TIME)

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

    def _filter_non_convictions(self):
        for event in self.personal_history.rap_sheet.events:
            for case_info in event.associated_cases:
                case_info.counts = [count for count in case_info.counts
                                    if count.disposition.disposition_decision == DispositionDecision.CONVICTED]

            # Filter out cases where all counts are dismissed
            event.associated_cases = [case for case in event.associated_cases if case.counts]

            # There should only be one court event with convictions
            assert len(event.associated_cases) <= 1

    def _annotate_ineligibility(self):
        for event in self.personal_history.rap_sheet.events:
            for case_info in event.associated_cases:
                for count in case_info.counts:
                    if count.disposition.disposition_decision == DispositionDecision.CONVICTED:
                        self._annotate_count_eligibility(case_info, count)

                event_ineligibility_reasons = []
                if not SanMateoCountyCourt.contains_city(event.arrest_info.city):
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
        self._filter_non_convictions()
        self._annotate_ineligibility()
        self._annotate_needs_declarations()

        # TODO: Create some sort of summary?
        return self.personal_history.rap_sheet

    def update_financial_information(self, financial_information):
        """
        :type financial_information: FinancialInfo
        """
        self.personal_history.financial_information = financial_information

    def generate_expungement_packets(self):
        for event in self.personal_history.rap_sheet.events:
            CR180Model.generate(self.personal_history, event)
            CR181Model.generate(self.personal_history, event)
            FW001Model.generate(self.personal_history, event)
            FW003Model.generate(self.personal_history, event)
            POS040Model.generate(self.personal_history, event)
