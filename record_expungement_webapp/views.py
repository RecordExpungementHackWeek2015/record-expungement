import pickle
import os
from django import forms
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.template import RequestContext
from django.core.servers.basehttp import FileWrapper

import shutil
import record_expungement_webapp
from record_expungement_webapp import mocks, models
from logic_engine import ExpungementLogicEngine
from packet_factory import PacketFactory
from form_util import FormUtil


# File upload form.
class DocumentForm(forms.Form):
    docfile = forms.FileField()


# Render the initial form to upload the rap sheet.
def start(request):
    context = RequestContext(request, {
        'doc_form': DocumentForm()
        })
    return render(request, 'steps/start.html', context)


def _clear_session(request):
    keys = ('rap_sheet', 'personal_history')
    for key in keys:
        try:
            del request.session[key]
        except KeyError:
            pass


# Upload and process the rap sheet.
def upload_rap_sheet(request):
    # Sleep so that we see the spinner for now.
    import time
    time.sleep(1)

    _clear_session(request)

    if request.method == 'POST':
        doc_form = DocumentForm(request.POST, request.FILES)
        if doc_form.is_valid():
            uploaded_file = request.FILES['docfile']

            rap_sheet = _process_rap_sheet(uploaded_file)

            request.session['rap_sheet'] = pickle.dumps(rap_sheet)

            return HttpResponseRedirect('/webapp/complete_personal_info')
    else:
        doc_form = DocumentForm()

    context = RequestContext(request, {
        'doc_form': doc_form
    })
    return render(request, 'steps/start.html', context)


def _process_rap_sheet(uploaded_file):
    for chunk in uploaded_file.chunks():
        pass
    rap_sheet = mocks.RAP_SHEET_1
    logic_engine = ExpungementLogicEngine(models.PersonalHistory(rap_sheet))
    return logic_engine.annotate_rap_sheet()


def _load_vars_from_session(request):
    rap_sheet = request.session.get('rap_sheet')
    rap_sheet = pickle.loads(rap_sheet)

    return rap_sheet


# Render the parsed rap sheet and personal info form.
def complete_personal_info(request):
    rap_sheet = _load_vars_from_session(request)

    template = loader.get_template('steps/complete_personal_info.html')
    info_form = PersonalInfoForm(events=rap_sheet.events)
    context = RequestContext(request, {
        'rap_sheet': rap_sheet,
        'info_form': info_form,
    })

    return HttpResponse(template.render(context))


def _long_text_input(num=None, placeholder=None):
    if num:
        return forms.TextInput(attrs={'placeholder': '(%d)' % num, 'size': '30'})
    elif placeholder:
        return forms.TextInput(attrs={'placeholder': placeholder, 'size': '30'})
    else:
        return forms.TextInput(attrs={'size': '30'})

def _short_text_input(placeholder=None):
    if placeholder:
        return forms.TextInput(attrs={'placeholder': placeholder, 'size': '10'})
    else:
        return forms.TextInput(attrs={'size': '10'})

def _amt_input():
    return forms.TextInput(attrs={'placeholder': '($)', 'size': '10'})

# Personal and financial info form.
class PersonalInfoForm(forms.Form):
    name_address_fields = ('fname', 'mname', 'lname', 'address', 'city', 'state', 'zip_code',
        'job_title', 'employer_name', 'employer_address', 'employer_city', 'employer_state', 'employer_zip_code')

    fname = forms.CharField(max_length=100, widget=_long_text_input(placeholder='First name'))
    mname = forms.CharField(max_length=100, required=False, widget=_long_text_input(placeholder='Middle name'))
    lname = forms.CharField(max_length=100, widget=_long_text_input(placeholder='Last name'))

    address = forms.CharField(max_length=100, widget=_long_text_input(placeholder='Street address'))
    city = forms.CharField(max_length=100, widget=_long_text_input(placeholder='City'))
    state = forms.CharField(max_length=10, widget=_short_text_input(placeholder='State'))
    zip_code = forms.CharField(max_length=10, widget=_short_text_input(placeholder='Zip code'))

    email = forms.CharField(label='Email', max_length=100, required=False, widget=_long_text_input(placeholder='Email address'))
    phone = forms.CharField(label='Phone', max_length=20, widget=_long_text_input(placeholder='Phone number'))

    job_title = forms.CharField(max_length=100, required=False, widget=_long_text_input(placeholder='Job title'))
    employer_name = forms.CharField(max_length=100, required=False, widget=_long_text_input(placeholder='Name of employer'))
    employer_address = forms.CharField(max_length=100, widget=_long_text_input(placeholder='Street address'))
    employer_city = forms.CharField(max_length=100, widget=_long_text_input(placeholder='City'))
    employer_state = forms.CharField(max_length=10, widget=_short_text_input(placeholder='State'))
    employer_zip_code = forms.CharField(max_length=10, widget=_short_text_input(placeholder='Zip code'))

    benefit_0 = forms.BooleanField(label='FOOD_STAMPS', required=False)
    benefit_1 = forms.BooleanField(label='SUPP_SEC_INC', required=False)
    benefit_2 = forms.BooleanField(label='SSP', required=False)
    benefit_3 = forms.BooleanField(label='MEDI_CAL', required=False)
    benefit_4 = forms.BooleanField(label='COUNTY_RELIEF_OR_GEN_ASSIST', required=False)
    benefit_5 = forms.BooleanField(label='IHSS', required=False)
    benefit_6 = forms.BooleanField(label='CALWORKS_OR_TRIBAL_TANF', required=False)
    benefit_7 = forms.BooleanField(label='CAPI', required=False)

    family_size = forms.CharField(label='Family size', max_length=2, widget=_short_text_input())
    family_income = forms.CharField(label='Family income', max_length=10, help_text='Gross monthly household income (before deductions for taxes)',
        widget=forms.TextInput(attrs={'placeholder': '', 'size': '10'}))

    income_changes = forms.BooleanField(label='Check here if your income changes a lot from month to month.', required=False)

    name_amount_1_monthly_1 = forms.CharField(label='Job title', max_length=100, required=False, widget=_long_text_input(1))
    name_amount_2_monthly_1 = forms.CharField(label='Amount', max_length=10, widget=_amt_input(), required=False)
    name_amount_1_monthly_2 = forms.CharField(label='Job title', max_length=100, required=False, widget=_long_text_input(2))
    name_amount_2_monthly_2 = forms.CharField(label='Amount', max_length=10, widget=_amt_input(), required=False)
    name_amount_1_monthly_3 = forms.CharField(label='Job title', max_length=100, required=False, widget=_long_text_input(3))
    name_amount_2_monthly_3 = forms.CharField(label='Amount', max_length=10, widget=_amt_input(), required=False)
    name_amount_1_monthly_4 = forms.CharField(label='Job title', max_length=100, required=False, widget=_long_text_input(4))
    name_amount_2_monthly_4 = forms.CharField(label='Amount', max_length=10, widget=_amt_input(), required=False)

    wage_earner_title_1 = forms.CharField(label='Job title', max_length=100, required=False, widget=_long_text_input(1))
    wage_earner_age_1 = forms.CharField(label='Age', max_length=3, widget=_short_text_input(), required=False)
    wage_earner_relationship_1 = forms.CharField(label='Relationship', max_length=50, required=False, widget=_long_text_input())
    wage_earner_amount_1 = forms.CharField(label='Amount', max_length=10, required=False, widget=_amt_input())
    wage_earner_title_2 = forms.CharField(label='Job title', max_length=100, required=False, widget=_long_text_input(2))
    wage_earner_age_2 = forms.CharField(label='Age', max_length=3, widget=_short_text_input(), required=False)
    wage_earner_relationship_2 = forms.CharField(label='Relationship', max_length=50, required=False, widget=_long_text_input())
    wage_earner_amount_2 = forms.CharField(label='Amount', max_length=10, required=False, widget=_amt_input())
    wage_earner_title_3 = forms.CharField(label='Job title', max_length=100, required=False, widget=_long_text_input(3))
    wage_earner_age_3 = forms.CharField(label='Age', max_length=3, widget=_short_text_input(), required=False)
    wage_earner_relationship_3 = forms.CharField(label='Relationship', max_length=50, required=False, widget=_long_text_input())
    wage_earner_amount_3 = forms.CharField(label='Amount', max_length=10, required=False, widget=_amt_input())
    wage_earner_title_4 = forms.CharField(label='Job title', max_length=100, required=False, widget=_long_text_input(4))
    wage_earner_age_4 = forms.CharField(label='Age', max_length=3, widget=_short_text_input(), required=False)
    wage_earner_relationship_4 = forms.CharField(label='Relationship', max_length=50, required=False, widget=_long_text_input())
    wage_earner_amount_4 = forms.CharField(label='Amount', max_length=10, required=False, widget=_amt_input())

    cash = forms.CharField(label='a. Cash', max_length=10, required=False, widget=_amt_input())

    name_amount_1_bank_1 = forms.CharField(max_length=100, required=False, widget=_long_text_input(1))
    name_amount_2_bank_1 = forms.CharField(max_length=10, required=False, widget=_amt_input())
    name_amount_1_bank_2 = forms.CharField(max_length=100, required=False, widget=_long_text_input(2))
    name_amount_2_bank_2 = forms.CharField(max_length=10, required=False, widget=_amt_input())
    name_amount_1_bank_3 = forms.CharField(max_length=100, required=False, widget=_long_text_input(3))
    name_amount_2_bank_3 = forms.CharField(max_length=10, required=False, widget=_amt_input())

    asset_1_vehicle_1 = forms.CharField(max_length=100, required=False, widget=_long_text_input(1))
    asset_2_vehicle_1 = forms.CharField(max_length=10, required=False, widget=_amt_input())
    asset_3_vehicle_1 = forms.CharField(max_length=10, required=False, widget=_amt_input())
    asset_1_vehicle_2 = forms.CharField(max_length=100, required=False, widget=_long_text_input(2))
    asset_2_vehicle_2 = forms.CharField(max_length=10, required=False, widget=_amt_input())
    asset_3_vehicle_2 = forms.CharField(max_length=10, required=False, widget=_amt_input())
    asset_1_vehicle_3 = forms.CharField(max_length=100, required=False, widget=_long_text_input(3))
    asset_2_vehicle_3 = forms.CharField(max_length=10, required=False, widget=_amt_input())
    asset_3_vehicle_3 = forms.CharField(max_length=10, required=False, widget=_amt_input())

    asset_1_real_estate_1 = forms.CharField(max_length=100, required=False, widget=_long_text_input(1))
    asset_2_real_estate_1 = forms.CharField(max_length=10, required=False, widget=_amt_input())
    asset_3_real_estate_1 = forms.CharField(max_length=10, required=False, widget=_amt_input())
    asset_1_real_estate_2 = forms.CharField(max_length=100, required=False, widget=_long_text_input(2))
    asset_2_real_estate_2 = forms.CharField(max_length=10, required=False, widget=_amt_input())
    asset_3_real_estate_2 = forms.CharField(max_length=10, required=False, widget=_amt_input())

    asset_1_other_1 = forms.CharField(max_length=100, required=False, widget=_long_text_input(1))
    asset_2_other_1 = forms.CharField(max_length=10, required=False, widget=_amt_input())
    asset_3_other_1 = forms.CharField(max_length=10, required=False, widget=_amt_input())
    asset_1_other_2 = forms.CharField(max_length=100, required=False, widget=_long_text_input(2))
    asset_2_other_2 = forms.CharField(max_length=10, required=False, widget=_amt_input())
    asset_3_other_2 = forms.CharField(max_length=10, required=False, widget=_amt_input())

    name_amount_1_payroll_1 = forms.CharField(max_length=100, required=False, widget=_long_text_input(1))
    name_amount_2_payroll_1 = forms.CharField(max_length=10, required=False, widget=_amt_input())
    name_amount_1_payroll_2 = forms.CharField(max_length=100, required=False, widget=_long_text_input(2))
    name_amount_2_payroll_2 = forms.CharField(max_length=10, required=False, widget=_amt_input())
    name_amount_1_payroll_3 = forms.CharField(max_length=100, required=False, widget=_long_text_input(3))
    name_amount_2_payroll_3 = forms.CharField(max_length=10, required=False, widget=_amt_input())
    name_amount_1_payroll_4 = forms.CharField(max_length=100, required=False, widget=_long_text_input(4))
    name_amount_2_payroll_4 = forms.CharField(max_length=10, required=False, widget=_amt_input())

    long_rent = forms.CharField(label='b. Rent or house payment & maintenance', max_length=10, required=False, widget=_amt_input())
    long_food_household = forms.CharField(label='c. Food and household supplies', max_length=10, required=False, widget=_amt_input())
    long_utilities = forms.CharField(label='d. Utilities and telephone', max_length=10, required=False, widget=_amt_input())
    long_clothing = forms.CharField(label='e. Clothing', max_length=10, required=False, widget=_amt_input())
    long_laundry = forms.CharField(label='f. Laundry and cleaning', max_length=10, required=False, widget=_amt_input())
    long_medical = forms.CharField(label='g. Medical and dental expenses', max_length=10, required=False, widget=_amt_input())
    long_insurance = forms.CharField(label='h. Insurance (life, health, accident, etc)', max_length=10, required=False, widget=_amt_input())
    long_school = forms.CharField(label='i. School, child care', max_length=10, required=False, widget=_amt_input())
    long_child = forms.CharField(label='j. Child, spousal support (another marriage)', max_length=10, required=False, widget=_amt_input())
    long_transportation = forms.CharField(label='k. Transportation, gas, auto repair and insurance', max_length=10,
        required=False, widget=_amt_input())

    name_amount_1_installment_1 = forms.CharField(max_length=100, required=False, widget=_long_text_input(1))
    name_amount_2_installment_1 = forms.CharField(max_length=10, required=False, widget=_amt_input())
    name_amount_1_installment_2 = forms.CharField(max_length=100, required=False, widget=_long_text_input(2))
    name_amount_2_installment_2 = forms.CharField(max_length=10, required=False, widget=_amt_input())
    name_amount_1_installment_3 = forms.CharField(max_length=100, required=False, widget=_long_text_input(3))
    name_amount_2_installment_3 = forms.CharField(max_length=10, required=False, widget=_amt_input())

    long_wages = forms.CharField(label='m. Wages/earnings withheld by court order', max_length=10,
        widget=_amt_input(), required=False)

    name_amount_1_other_1 = forms.CharField(max_length=100, required=False, widget=_long_text_input(1))
    name_amount_2_other_1 = forms.CharField(max_length=10, required=False, widget=_amt_input())
    name_amount_1_other_2 = forms.CharField(max_length=100, required=False, widget=_long_text_input(2))
    name_amount_2_other_2 = forms.CharField(max_length=10, required=False, widget=_amt_input())
    name_amount_1_other_3 = forms.CharField(max_length=100, required=False, widget=_long_text_input(3))
    name_amount_2_other_3 = forms.CharField(max_length=10, required=False, widget=_amt_input())

    _WAIVER_PREFIX = 'waiver_'
    _BENEFIT_PREFIX = 'benefit_'

    def __init__(self, *args, **kwargs):
        self.events = kwargs.pop('events')
        super(PersonalInfoForm, self).__init__(*args, **kwargs)

        for i, e in enumerate(self.events):
            field_name = '%s%d' % (self._WAIVER_PREFIX, i)
            self.fields[field_name] = forms.BooleanField(label=field_name, required=False)

    def _create_personal_history(self, rap_sheet):
        name = models.Name(first=self.cleaned_data['fname'], middle=self.cleaned_data['mname'], last=self.cleaned_data['lname'])
        address = models.Address(self.cleaned_data['address'], self.cleaned_data['city'], self.cleaned_data['state'],
            self.cleaned_data['zip_code'])
        email = self.cleaned_data['email']
        phone_number = self.cleaned_data['phone']

        financial_info = self._get_financial_info()
        personal_history = models.PersonalHistory(rap_sheet, name=name, address=address,
            email=email, phone_number=phone_number, financial_info=financial_info)
        return personal_history

    def _get_financial_info(self):
        job_title = self.cleaned_data['job_title']
        employer_name = self.cleaned_data['employer_name']
        address = models.Address(self.cleaned_data['employer_address'], self.cleaned_data['employer_city'],
            self.cleaned_data['employer_state'], self.cleaned_data['employer_zip_code'])
        job = models.Job(job_title, employer_name, address)

        monthly_income_sources = self._get_monthly_income_sources()
        other_household_wage_earners = self._get_other_household_wage_earners()
        money_and_property = self._get_money_and_property()
        monthly_deductions_and_expenses = self._get_monthly_deductions_and_expenses()

        financial_info = models.FinancialInfo(job=job, monthly_income_sources=monthly_income_sources,
            money_and_property=money_and_property, monthly_deductions_and_expenses=monthly_deductions_and_expenses)

        financial_info.benefits_received_from_state = self._get_benefits()
        financial_info.family_size = self.cleaned_data['family_size']
        financial_info.total_family_income = self.cleaned_data['family_income']
        financial_info.event_index_to_whether_fees_have_been_waived_recently = self._get_event_to_waiver_status()
        financial_info.income_changes_significantly_month_to_month = self.cleaned_data['income_changes']
        return financial_info

    def _get_monthly_deductions_and_expenses(self):
        mdae = models.MonthlyDeductionsAndExpenses()

        payroll_deduction = []
        for i in xrange(1, 5):
            expense = models.Expense()
            expense.recipient = self.cleaned_data['name_amount_1_payroll_%d' % i]
            expense.amount = self.cleaned_data['name_amount_2_payroll_%d' % i]
            payroll_deduction.append(expense)

        mdae.payroll_deduction = payroll_deduction

        mdae.rent_or_house_payment = self.cleaned_data['long_rent']
        mdae.food_and_household_supplies = self.cleaned_data['long_food_household']
        mdae.utilities_and_telephone = self.cleaned_data['long_utilities']
        mdae.clothing = self.cleaned_data['long_clothing']
        mdae.laundry_and_cleaning = self.cleaned_data['long_laundry']
        mdae.medical_and_dental = self.cleaned_data['long_medical']
        mdae.insurance = self.cleaned_data['long_insurance']
        mdae.school_and_child_care = self.cleaned_data['long_school']
        mdae.child_or_spousal_support = self.cleaned_data['long_child']
        mdae.car_and_transporation = self.cleaned_data['long_transportation']

        installment_payments = []
        for i in xrange(1, 4):
            expense = models.Expense()
            expense.recipient = self.cleaned_data['name_amount_1_installment_%d' % i]
            expense.amount = self.cleaned_data['name_amount_2_installment_%d' % i]
            installment_payments.append(expense)
        mdae.installment_payments = installment_payments

        mdae.wages_witheld_by_court_order = self.cleaned_data['long_wages']

        other_monthly_expenses = []
        for i in xrange(1, 4):
            expense = models.Expense()
            expense.recipient = self.cleaned_data['name_amount_1_other_%d' % i]
            expense.amount = self.cleaned_data['name_amount_2_other_%d' % i]
            other_monthly_expenses.append(expense)
        mdae.other_monthly_expenses = other_monthly_expenses

        return mdae

    def _get_money_and_property(self):
        total_cash = self.cleaned_data['cash']

        bank_accounts = []
        for i in xrange(1, 4):
            bank_account = models.BankAccount()
            bank_account.bank_name = self.cleaned_data['name_amount_1_bank_%d' % i]
            bank_account.amount = self.cleaned_data['name_amount_2_bank_%d' % i]
            bank_accounts.append(bank_account)

        vehicles = []
        for i in xrange(1, 4):
            vehicle = models.Vehicle()
            vehicle.make_and_year = self.cleaned_data['asset_1_vehicle_%d' % i]
            vehicle.asset_value = models.AssetValue()
            vehicle.asset_value.fair_market_value = self.cleaned_data['asset_2_vehicle_%d' % i]
            vehicle.asset_value.amount_still_owed = self.cleaned_data['asset_3_vehicle_%d' % i]
            vehicles.append(vehicle)

        real_estates = []
        for i in xrange(1, 3):
            real_estate = models.RealEstate()
            real_estate.address = self.cleaned_data['asset_1_real_estate_%d' % i]
            real_estate.asset_value = models.AssetValue()
            real_estate.asset_value.fair_market_value = self.cleaned_data['asset_2_real_estate_%d' % i]
            real_estate.asset_value.amount_still_owed = self.cleaned_data['asset_3_real_estate_%d' % i]
            real_estates.append(real_estate)

        other_property = []
        for i in xrange(1, 3):
            personal_property = models.PersonalProperty()
            personal_property.description = self.cleaned_data['asset_1_other_%d' % i]
            personal_property.asset_value = models.AssetValue()
            personal_property.asset_value.fair_market_value = self.cleaned_data['asset_2_other_%d' % i]
            personal_property.asset_value.amount_still_owed = self.cleaned_data['asset_3_other_%d' % i]
            other_property.append(personal_property)

        money_and_property = models.MoneyAndProperty()
        money_and_property.total_cash = total_cash
        money_and_property.bank_accounts = bank_accounts
        money_and_property.vehicles = vehicles
        money_and_property.real_estate = real_estates
        money_and_property.other_property = other_property
        return money_and_property

    def _get_monthly_income_sources(self):
        monthly_income_sources = []
        for i in xrange(1, 5):
            monthly_income_source = models.MonthlyIncomeSource()
            monthly_income_source.job_title = self.cleaned_data['name_amount_1_monthly_%d' % i]
            monthly_income_source.monthly_income = self.cleaned_data['name_amount_2_monthly_%d' % i]
            monthly_income_sources.append(monthly_income_source)
        return monthly_income_sources

    def _get_other_household_wage_earners(self):
        other_household_wage_earners = []
        for i in xrange(1, 5):
            wage_earner = models.WageEarner()
            wage_earner.name = self.cleaned_data['wage_earner_title_%d' % i]
            wage_earner.age = self.cleaned_data['wage_earner_age_%d' % i]
            wage_earner.relationship = self.cleaned_data['wage_earner_relationship_%d' % i]
            wage_earner.gross_monthly_income = self.cleaned_data['wage_earner_amount_%d' % i]
            other_household_wage_earners.append(wage_earner)
        return other_household_wage_earners

    # Get zipped list of event to waiver field.
    def waiver_fields(self):
        result = []
        for name in self.fields:
            if name.startswith(self._WAIVER_PREFIX):
                result.append(self[name])
        return zip(self.events, result)

    # Get map of event index to if fees were waived before
    # i.e. {0: False, 1: False, 2: False}
    def _get_event_to_waiver_status(self):
        idx_to_status = {}
        for name, value in self.cleaned_data.items():
            if name.startswith(self._WAIVER_PREFIX):
                idx = int(name[len(self._WAIVER_PREFIX):])
                idx_to_status[idx] = value
        return idx_to_status

    # Get benefits received as int values
    # i.e. [2, 4, 6]
    def _get_benefits(self):
        benefits = []
        for name, value in self.cleaned_data.items():
            if name.startswith(self._BENEFIT_PREFIX):
                if value:
                    idx = int(name[len(self._BENEFIT_PREFIX):])
                    benefits.append(idx)
        return benefits


# Process personal info input.
def submit_personal_info(request):
    rap_sheet = _load_vars_from_session(request)

    if request.method == 'POST':
        info_form = PersonalInfoForm(request.POST, events=rap_sheet.events)

        info_form.require_all_fields = False
        for field in info_form:
            field.required = False

        if info_form.is_valid():
            request.session['personal_history'] = pickle.dumps(info_form._create_personal_history(rap_sheet))
            return HttpResponseRedirect('/webapp/success')
    else:
        info_form = PersonalInfoForm(events=rap_sheet.events)

    template = loader.get_template('steps/complete_personal_info.html')
    context = RequestContext(request, {
        'rap_sheet': rap_sheet,
        'info_form': info_form
    })
    return HttpResponse(template.render(context))


# Render the success page with a button to download.
def success(request):
    context = RequestContext(request, {})
    return render(request, 'steps/success.html', context)


def _generate_forms(request):
    personal_history = pickle.loads(request.session['personal_history'])

    DIR_FOR_ALL_SESSIONS = "outputs"
    SUBFOLDER_FOR_THIS_SESSION = "session_" + request.session.session_key
    FORMS_FOLDER = "static/forms"
    WEBAPP_PATH = os.path.abspath(record_expungement_webapp.__path__[0])
    PACKET_BASE_FOLDER = os.path.join(WEBAPP_PATH, DIR_FOR_ALL_SESSIONS, SUBFOLDER_FOR_THIS_SESSION)

    if os.path.exists(SUBFOLDER_FOR_THIS_SESSION):
        shutil.rmtree(SUBFOLDER_FOR_THIS_SESSION)

    for i, event in enumerate(personal_history.rap_sheet.events):
        EVENT_SUBFOLDER = FormUtil.date_to_str(event.arrest_info.date) + "_arrest"
        if event.has_eligible_convictions():
            packet_output_folder = os.path.join(WEBAPP_PATH, DIR_FOR_ALL_SESSIONS, SUBFOLDER_FOR_THIS_SESSION,
                                                str(EVENT_SUBFOLDER))
            resources_directory = os.path.join(WEBAPP_PATH, FORMS_FOLDER)
            PacketFactory.generate(personal_history, event, packet_output_folder, resources_directory)

    file_name = "expungement_forms_packet"
    zip_path = "/tmp/" + file_name
    path_to_zip = shutil.make_archive(zip_path, "zip", PACKET_BASE_FOLDER)
    response = HttpResponse(FileWrapper(file(path_to_zip, 'rb')), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=' + file_name.replace(" ", "_") + '.zip'
    return response


def download_forms(request):
    return _generate_forms(request)

