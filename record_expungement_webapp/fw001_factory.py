from models import PersonalHistory, StateBenefit, FinancialInfo
from county_court_info import SanMateoCountyCourt
from form_util import FormUtil


class FW001Factory:
    def __init__(self):
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
    def _benefits_checks(fi):
        """
        :type fi: FinancialInfo
        """
        checks = [(FW001Factory._benefit_to_checkbox_name(benefit), True)
                  for benefit in fi.benefits_received_from_state]
        if checks:
            checks.append(("5a", True))  # Check the first box
        return checks

    @staticmethod
    def _monthly_and_household_income(fi):
        """
        :type fi: FinancialInfo
        """
        monthly_personal_income_total = sum([source.monthly_income for source in fi.monthly_income_sources])
        household_income_total = sum([source.gross_monthly_income for source in fi.other_household_wage_earners])
        total = monthly_personal_income_total + household_income_total

        income_fields = []
        for i, source in enumerate(fi.monthly_income_sources):
            income_fields.extend([("8a%(i)s1" % {'i': i}, source.job_title),
                                  ("8a%(i)s2" % {'i': i}, source.monthly_income)])

        for i, source in enumerate(fi.other_household_wage_earners):
            income_fields.extend([("8a%(i)s1" % {'i': i}, source.name),
                                  ("8a%(i)s2" % {'i': i}, source.age),
                                  ("8a%(i)s3" % {'i': i}, source.relationship),
                                  ("8a%(i)s4" % {'i': i}, source.gross_monthly_income)])

        income_fields.append(("8_total", monthly_personal_income_total))
        income_fields.append(("9_total", household_income_total))
        income_fields.append(("8_and_9_total", total))

    @staticmethod
    def _money_and_property(fi):
        """
        :type fi: FinancialInfo
        """
        mp = fi.money_and_property
        fields = [("10a", mp.total_cash)]

        for i, acct in enumerate(mp.bank_accounts):
            fields.extend([("10b%(i)s1" % {'i': i}, acct.bank_name), ("10b%(i)s2" % {'i': i}, acct.amount)])

        for i, vehicle in enumerate(mp.vehicles):
            fields.extend([("10c%(i)s1" % {'i': i}, vehicle.make_and_year),
                           ("10c%(i)s2" % {'i': i}, vehicle.asset_value.fair_market_value),
                           ("10c%(i)s3" % {'i': i}, vehicle.asset_value.amount_still_owed)])

        for i, asset in enumerate(mp.real_estate):
            fields.extend([("10d%(i)s1" % {'i': i}, asset.address.to_str_one_line()),
                           ("10d%(i)s2" % {'i': i}, asset.asset_value.fair_market_value),
                           ("10d%(i)s3" % {'i': i}, asset.asset_value.amount_still_owed)])

        for i, asset in enumerate(mp.other_property):
            fields.extend([("10e%(i)s1" % {'i': i}, asset.description),
                           ("10e%(i)s2" % {'i': i}, asset.asset_value.fair_market_value),
                           ("10f%(i)s3" % {'i': i}, asset.asset_value.amount_still_owed)])

    @staticmethod
    def _monthly_deductions_and_expenses(fi):
        dollar_amounts = []
        descriptions = []

        md = fi.monthly_deductions_and_expenses
        for i, deduction in enumerate(md.payroll_deduction):
            descriptions.append(("11a%(i)s1" % {'i': i}, deduction.recipient))
            dollar_amounts.append(("11a%(i)s2" % {'i': i}, deduction.amount))

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
            descriptions.append(("11l%(i)s1" % {'i': i}, payment.recipient))
            dollar_amounts.append(("11l%(i)s2" % {'i': i}, payment.amount))

        for i, expense in enumerate(md.other_monthly_expenses):
            descriptions.append(("11n%(i)s1" % {'i': i}, expense.recipient))
            dollar_amounts.append(("11n%(i)s2" % {'i': i}, expense.amount))

        total = sum(amount for (label, amount) in dollar_amounts)
        return descriptions + dollar_amounts + [("11_total", total)]

    @staticmethod
    def generate(ph, event):
        """
        :type ph: PersonalHistory
        :type event: Event
        """
        fi = ph.financial_information
        return [
            ("1a", ph.name),
            ("1b", ph.address.address),
            ("1c", ph.address.city),
            ("1d", ph.address.state),
            ("1e", ph.address.zip_code),
            ("1f", ph.phone_number),
            ("2a", fi.job.job_title),
            ("2b", fi.job.employer_name),
            ("2c", fi.job.employer_address.to_str_one_line()),
            ("3", "N/A"),  # Lawyer, if person has one
            ("4a", True),  # Check 4a but not 4b
        ].extend(
            FW001Factory._benefits_checks(fi)
        ).extend(
            [("6a", True)]
            if fi.event_index_to_whether_fees_have_been_waived_recently(ph.rap_sheet.events.index(event)) else []
        ).extend(
            [("7", True)] if fi.income_changes_significantly_month_to_month else []
        ).extend(
            FW001Factory._monthly_and_household_income(fi)
        ).extend(
            FW001Factory._money_and_property(fi)
        ).extend(
            FW001Factory._monthly_deductions_and_expenses(fi)
        ).extend([
            ("12", SanMateoCountyCourt.mailing_address_multiline_str()),
            ("13", event.associated_cases[0].case_id),
            ("14", FormUtil.short_case_name(ph, event)),
        ])
