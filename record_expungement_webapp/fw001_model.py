from models import PersonalHistory, StateBenefit, FinancialInfo
from county_court_info import SanMateoCountyCourt
from form_util import FormUtil, FormModel


class FW001Model(FormModel):
    def __init__(self):
        FormModel.__init__(self)
        raise ValueError("Don't construct me")

    @staticmethod
    def _benefit_to_checkbox_name(benefit):
        key = {
            StateBenefit.FOOD_STAMPS: "5a1",
            StateBenefit.SUPP_SEC_INC: "5a2",
            StateBenefit.SSP: "5a3",
            StateBenefit.MEDI_CAL: "5a4",
            StateBenefit.COUNTY_RELIEF_OR_GEN_ASSIST: "5a5",
            StateBenefit.IHSS: "5a6",
            StateBenefit.CALWORKS_OR_TRIBAL_TANF: "5a7",
            StateBenefit.CAPI: "5a8",
        }

        return key[benefit]

    @staticmethod
    def _waiver_needed_reasons(fi):
        """
        :type fi: FinancialInfo
        """
        checks = [(FW001Model._benefit_to_checkbox_name(benefit), True)
                  for benefit in fi.benefits_received_from_state]
        if checks:
            checks.append(("5a", True))  # Check the first box

        family_size_to_threshold = [0,
                                    1226.05,
                                    1659.38,
                                    2092.71,
                                    2526.05,
                                    2959.38,
                                    3392.71]

        family_size = int(fi.family_size)
        family_income = float(fi.total_family_income)
        last_threshold = family_size_to_threshold[-1]
        last_size = len(family_size_to_threshold) - 1
        threshold = family_size_to_threshold[family_size] if last_size >= family_size \
            else last_threshold + 433.34 * (family_size - last_size)

        if family_income < threshold:
            checks.append(("5b", True))

        if not checks:
            checks.append(("5c", True))  # Check the first box
            checks.append(("5c1", True))  # Check the first box

        return checks

    @staticmethod
    def _monthly_and_household_income(fi):
        """
        :type fi: FinancialInfo
        """
        monthly_personal_income_total = sum([int(source.monthly_income) for source in fi.monthly_income_sources if source.monthly_income])
        household_income_total = sum([int(source.gross_monthly_income) for source in fi.other_household_wage_earners if source.gross_monthly_income])
        total = monthly_personal_income_total + household_income_total

        income_fields = []
        for i, source in enumerate(fi.monthly_income_sources):
            income_fields.extend([("8a%(i)sa" % {'i': i+1}, source.job_title),
                                  ("8a%(i)sb" % {'i': i+1}, source.monthly_income)])

        for i, source in enumerate(fi.other_household_wage_earners):
            income_fields.extend([("9a%(i)sa" % {'i': i+1}, source.name),
                                  ("9a%(i)sb" % {'i': i+1}, source.age),
                                  ("9a%(i)sc" % {'i': i+1}, source.relationship),
                                  ("9a%(i)sd" % {'i': i+1}, source.gross_monthly_income)])

        income_fields.append(("8b", monthly_personal_income_total))
        income_fields.append(("9b", household_income_total))
        income_fields.append(("8b_9b", total))
        return income_fields

    @staticmethod
    def _money_and_property(fi):
        """
        :type fi: FinancialInfo
        """
        mp = fi.money_and_property
        fields = [("10a", mp.total_cash)]

        for i, acct in enumerate(mp.bank_accounts):
            fields.extend([("10b%(i)sa" % {'i': i+1}, acct.bank_name),
                           ("10b%(i)sb" % {'i': i+1}, acct.amount)])

        for i, vehicle in enumerate(mp.vehicles):
            fields.extend([("10c%(i)sa" % {'i': i+1}, vehicle.make_and_year),
                           ("10c%(i)sb" % {'i': i+1}, vehicle.asset_value.fair_market_value),
                           ("10c%(i)sc" % {'i': i+1}, vehicle.asset_value.amount_still_owed)])

        for i, asset in enumerate(mp.real_estate):
            fields.extend([("10d%(i)sa" % {'i': i+1}, asset.address),
                           ("10d%(i)sb" % {'i': i+1}, asset.asset_value.fair_market_value),
                           ("10d%(i)sc" % {'i': i+1}, asset.asset_value.amount_still_owed)])

        for i, asset in enumerate(mp.other_property):
            fields.extend([("10e%(i)sa" % {'i': i+1}, asset.description),
                           ("10e%(i)sb" % {'i': i+1}, asset.asset_value.fair_market_value),
                           ("10e%(i)sc" % {'i': i+1}, asset.asset_value.amount_still_owed)])
        return fields

    @staticmethod
    def _monthly_deductions_and_expenses(fi):
        dollar_amounts = []
        descriptions = []

        md = fi.monthly_deductions_and_expenses
        for i, deduction in enumerate(md.payroll_deduction):
            descriptions.append(("11a%(i)sa" % {'i': i+1}, deduction.recipient))
            dollar_amounts.append(("11a%(i)sb" % {'i': i+1}, deduction.amount))

        dollar_amounts.extend([
            ("11b", md.rent_or_house_payment),
            ("11c", md.food_and_household_supplies),
            ("11d", md.utilities_and_telephone),
            ("11e", md.clothing),
            ("11f", md.laundry_and_cleaning),
            ("11g", md.medical_and_dental),
            ("11h", md.insurance),
            ("11i", md.school_and_child_care),
            ("11j", md.child_or_spousal_support),
            ("11k", md.car_and_transporation),
            ("11m", md.wages_witheld_by_court_order),
        ])

        for i, payment in enumerate(md.installment_payments):
            descriptions.append(("11l%(i)sa" % {'i': i+1}, payment.recipient))
            dollar_amounts.append(("11l%(i)sb" % {'i': i+1}, payment.amount))

        for i, expense in enumerate(md.other_monthly_expenses):
            descriptions.append(("11n%(i)sa" % {'i': i+1}, expense.recipient))
            dollar_amounts.append(("11n%(i)sb" % {'i': i+1}, expense.amount))
        other_expenses_total = sum([int(expense.amount) for expense in md.other_monthly_expenses])
        # dollar_amounts.append(("11n", other_expenses_total))

        total = sum(int(amount) for (label, amount) in dollar_amounts if amount)
        return descriptions + dollar_amounts + [("11_total", total)]

    @staticmethod
    def get_name():
        return "fw001"

    @staticmethod
    def get_output_file_name():
        return "fw001.pdf"

    @staticmethod
    def get_fields(ph, event):
        """
        :type ph: PersonalHistory
        :type event: Event
        """
        fi = ph.financial_information
        fields = [
            ("1a", str(ph.name)),
            ("1b", ph.address.address),
            ("1c", ph.address.city),
            ("1d", ph.address.state),
            ("1e", ph.address.zip_code),
            ("1f", ph.phone_number),
            ("2a", fi.job.job_title),
            ("2b", fi.job.employer_name),
            ("2c", fi.job.employer_address.to_str_one_line()),
            ("3a", "N/A"),  # Lawyer, if person has one
            ("4a", True),  # Check 4a but not 4b
        ]
        fields.extend(FW001Model._waiver_needed_reasons(fi))
        fields.extend(
            [("6a", True)]
            if fi.event_index_to_whether_fees_have_been_waived_recently[ph.rap_sheet.events.index(event)] else []
        )
        fields.extend(
            [("7", True)] if fi.income_changes_significantly_month_to_month else []
        )
        fields.extend(FW001Model._monthly_and_household_income(fi))
        fields.extend(FW001Model._money_and_property(fi))
        fields.extend(FW001Model._monthly_deductions_and_expenses(fi))
        fields.extend([
            ("12", SanMateoCountyCourt.mailing_address_multiline_str()),
            ("13", event.associated_cases[0].case_id),
            ("14", FormUtil.short_case_name(ph, event)),
        ])
        return fields
