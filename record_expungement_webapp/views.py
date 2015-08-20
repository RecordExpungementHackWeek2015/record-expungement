import cStringIO
import pickle
from django import forms
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.template import RequestContext

from record_expungement_webapp import mocks
from logic_engine import ExpungementLogicEngine
from models import PersonalHistory


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
    keys = ('filename', 'filesize', 'rap_sheet')
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
            request.session['filename'] = uploaded_file.name
            request.session['filesize'] = uploaded_file.size

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
    logic_engine = ExpungementLogicEngine(PersonalHistory(rap_sheet))
    return logic_engine.annotate_rap_sheet()


def _load_vars_from_session(request):
    rap_sheet = request.session.get('rap_sheet')
    rap_sheet = pickle.loads(rap_sheet)

    filename = request.session.get('filename')
    filesize = request.session.get('filesize')
    return filename, filesize, rap_sheet


# Render the parsed rap sheet and personal info form.
def complete_personal_info(request):
    filename, filesize, rap_sheet = _load_vars_from_session(request)

    template = loader.get_template('steps/complete_personal_info.html')
    info_form = PersonalInfoForm(events=rap_sheet.events)
    context = RequestContext(request, {
        'filename': filename,
        'filesize': filesize,
        'rap_sheet': rap_sheet,
        'info_form': info_form,
    })

    return HttpResponse(template.render(context))


# Personal and financial info form.
class PersonalInfoForm(forms.Form):
    fname = forms.CharField(label='First name', max_length=100)
    mname = forms.CharField(label='Middle name', max_length=100, required=False)
    lname = forms.CharField(label='Last name', max_length=100)

    address = forms.CharField(label='Address', max_length=100)
    city = forms.CharField(label='City', max_length=100)
    state = forms.CharField(label='State', max_length=10)
    zip_code = forms.CharField(label='Zip code', max_length=10)

    email = forms.CharField(label='Email', max_length=100, required=False)
    phone = forms.CharField(label='Phone', max_length=20)

    job_title = forms.CharField(label='Job title', max_length=100, required=False)
    employer_name = forms.CharField(label='Employer name', max_length=100, required=False)
    employer_address = forms.CharField(label='Employer address', max_length=100, required=False)
    employer_city = forms.CharField(label='City', max_length=100, required=False)
    employer_state = forms.CharField(label='State', max_length=10, required=False)
    employer_zip_code = forms.CharField(label='Zip code', max_length=10, required=False)

    benefit_0 = forms.BooleanField(label='FOOD_STAMPS', required=False)
    benefit_1 = forms.BooleanField(label='SUPP_SEC_INC', required=False)
    benefit_2 = forms.BooleanField(label='SSP', required=False)
    benefit_3 = forms.BooleanField(label='MEDI_CAL', required=False)
    benefit_4 = forms.BooleanField(label='COUNTY_RELIEF_OR_GEN_ASSIST', required=False)
    benefit_5 = forms.BooleanField(label='IHSS', required=False)
    benefit_6 = forms.BooleanField(label='CALWORKS_OR_TRIBAL_TANF', required=False)
    benefit_7 = forms.BooleanField(label='CAPI', required=False)

    family_size = forms.CharField(label='Family size', max_length=10)
    family_income = forms.CharField(label='Monthly family income', max_length=10)

    income_changes = forms.BooleanField(label='Does your income change a lot from month to month?', required=False)

    name_amount_1_monthly_1 = forms.CharField(label='Job title', max_length=100, required=False)
    name_amount_2_monthly_1 = forms.CharField(label='Amount', max_length=10, widget=forms.TextInput(attrs={'size': '10'}), required=False)
    name_amount_1_monthly_2 = forms.CharField(label='Job title', max_length=100, required=False)
    name_amount_2_monthly_2 = forms.CharField(label='Amount', max_length=10, widget=forms.TextInput(attrs={'size': '10'}), required=False)
    name_amount_1_monthly_3 = forms.CharField(label='Job title', max_length=100, required=False)
    name_amount_2_monthly_3 = forms.CharField(label='Amount', max_length=10, widget=forms.TextInput(attrs={'size': '10'}), required=False)
    name_amount_1_monthly_4 = forms.CharField(label='Job title', max_length=100, required=False)
    name_amount_2_monthly_4 = forms.CharField(label='Amount', max_length=10, widget=forms.TextInput(attrs={'size': '10'}), required=False)

    wage_earner_title_1 = forms.CharField(label='Job title', max_length=100, required=False)
    wage_earner_age_1 = forms.CharField(label='Age', max_length=3, widget=forms.TextInput(attrs={'size': '3'}), required=False)
    wage_earner_relationship_1 = forms.CharField(label='Relationship', max_length=50, required=False)
    wage_earner_amount_1 = forms.CharField(label='Amount', max_length=10, required=False)
    wage_earner_title_2 = forms.CharField(label='Job title', max_length=100, required=False)
    wage_earner_age_2 = forms.CharField(label='Age', max_length=3, widget=forms.TextInput(attrs={'size': '3'}), required=False)
    wage_earner_relationship_2 = forms.CharField(label='Relationship', max_length=50, required=False)
    wage_earner_amount_2 = forms.CharField(label='Amount', max_length=10, required=False)
    wage_earner_title_3 = forms.CharField(label='Job title', max_length=100, required=False)
    wage_earner_age_3 = forms.CharField(label='Age', max_length=3, widget=forms.TextInput(attrs={'size': '3'}), required=False)
    wage_earner_relationship_3 = forms.CharField(label='Relationship', max_length=50, required=False)
    wage_earner_amount_3 = forms.CharField(label='Amount', max_length=10, required=False)
    wage_earner_title_4 = forms.CharField(label='Job title', max_length=100, required=False)
    wage_earner_age_4 = forms.CharField(label='Age', max_length=3, widget=forms.TextInput(attrs={'size': '3'}), required=False)
    wage_earner_relationship_4 = forms.CharField(label='Relationship', max_length=50, required=False)
    wage_earner_amount_4 = forms.CharField(label='Amount', max_length=10, required=False)

    name_amount_1_bank_1 = forms.CharField(label='', max_length=100, required=False)
    name_amount_2_bank_1 = forms.CharField(label='', max_length=10, required=False)
    name_amount_1_bank_2 = forms.CharField(label='', max_length=100, required=False)
    name_amount_2_bank_2 = forms.CharField(label='', max_length=10, required=False)

    asset_1_vehicle_1 = forms.CharField(label='', max_length=100, required=False)
    asset_2_vehicle_1 = forms.CharField(label='', max_length=10, required=False)
    asset_3_vehicle_1 = forms.CharField(label='', max_length=10, required=False)
    asset_1_vehicle_2 = forms.CharField(label='', max_length=100, required=False)
    asset_2_vehicle_2 = forms.CharField(label='', max_length=10, required=False)
    asset_3_vehicle_2 = forms.CharField(label='', max_length=10, required=False)

    asset_1_real_estate_1 = forms.CharField(label='', max_length=100, required=False)
    asset_2_real_estate_1 = forms.CharField(label='', max_length=10, required=False)
    asset_3_real_estate_1 = forms.CharField(label='', max_length=10, required=False)
    asset_1_real_estate_2 = forms.CharField(label='', max_length=100, required=False)
    asset_2_real_estate_2 = forms.CharField(label='', max_length=10, required=False)
    asset_3_real_estate_2 = forms.CharField(label='', max_length=10, required=False)

    asset_1_other_1 = forms.CharField(label='', max_length=100, required=False)
    asset_2_other_1 = forms.CharField(label='', max_length=10, required=False)
    asset_3_other_1 = forms.CharField(label='', max_length=10, required=False)
    asset_1_other_2 = forms.CharField(label='', max_length=100, required=False)
    asset_2_other_2 = forms.CharField(label='', max_length=10, required=False)
    asset_3_other_2 = forms.CharField(label='', max_length=10, required=False)

    name_amount_1_payroll_1 = forms.CharField(label='', max_length=100, required=False)
    name_amount_2_payroll_1 = forms.CharField(label='', max_length=10, required=False)
    name_amount_1_payroll_2 = forms.CharField(label='', max_length=100, required=False)
    name_amount_2_payroll_2 = forms.CharField(label='', max_length=10, required=False)

    long_rent = forms.CharField(label='Rent or house payment', max_length=10, widget=forms.TextInput(attrs={'size': '10'}), required=False)
    long_food_household = forms.CharField(label='Food or household supplies', max_length=10, widget=forms.TextInput(attrs={'size': '10'}), required=False)
    long_utilities = forms.CharField(label='Utilities and telephone', max_length=10, widget=forms.TextInput(attrs={'size': '10'}), required=False)
    long_clothing = forms.CharField(label='Clothing', max_length=10, widget=forms.TextInput(attrs={'size': '10'}), required=False)
    long_laundry = forms.CharField(label='Laundry and cleaning', max_length=10, widget=forms.TextInput(attrs={'size': '10'}), required=False)
    long_medical = forms.CharField(label='Medical and dental', max_length=10, widget=forms.TextInput(attrs={'size': '10'}), required=False)
    long_insurance = forms.CharField(label='Insurance', max_length=10, widget=forms.TextInput(attrs={'size': '10'}), required=False)
    long_school = forms.CharField(label='School, child care', max_length=10, widget=forms.TextInput(attrs={'size': '10'}), required=False)
    long_child = forms.CharField(label='Child, spousal support', max_length=10, widget=forms.TextInput(attrs={'size': '10'}), required=False)
    long_transportation = forms.CharField(label='Transportation, gas', max_length=10, widget=forms.TextInput(attrs={'size': '10'}), required=False)

    name_amount_1_installment_1 = forms.CharField(label='', max_length=100, required=False)
    name_amount_2_installment_1 = forms.CharField(label='', max_length=10, required=False)
    name_amount_1_installment_2 = forms.CharField(label='', max_length=100, required=False)
    name_amount_2_installment_2 = forms.CharField(label='', max_length=10, required=False)

    long_wages = forms.CharField(label='Wages withheld by court order', max_length=10, widget=forms.TextInput(attrs={'size': '10'}), required=False)

    name_amount_1_other_1 = forms.CharField(label='', max_length=100, required=False)
    name_amount_2_other_1 = forms.CharField(label='', max_length=10, required=False)
    name_amount_1_other_2 = forms.CharField(label='', max_length=100, required=False)
    name_amount_2_other_2 = forms.CharField(label='', max_length=10, required=False)

    _WAIVER_PREFIX = 'waiver_'
    _BENEFIT_PREFIX = 'benefit_'

    def __init__(self, *args, **kwargs):
        self.events = kwargs.pop('events')
        super(PersonalInfoForm, self).__init__(*args, **kwargs)

        for i, e in enumerate(self.events):
            field_name = '%s%d' % (self._WAIVER_PREFIX, i)
            self.fields[field_name] = forms.BooleanField(label=field_name, required=False)

    # Get zipped list of event to waiver field.
    def waiver_fields(self):
        result = []
        for name in self.fields:
            if name.startswith(self._WAIVER_PREFIX):
                result.append(self[name])
        return zip(self.events, result)

    # Get map of event index to if fees were waived before
    # i.e. {0: False, 1: False, 2: False}
    def get_event_to_waiver_status(self):
        idx_to_status = {}
        for name, value in self.cleaned_data.items():
            if name.startswith(self._WAIVER_PREFIX):
                idx = int(name[len(self._WAIVER_PREFIX):])
                idx_to_status[idx] = value
        return idx_to_status

    # Get benefits received as int values
    # i.e. [2, 4, 6]
    def get_benefits(self):
        benefits = []
        for name, value in self.cleaned_data.items():
            if name.startswith(self._BENEFIT_PREFIX):
                if value:
                    idx = int(name[len(self._BENEFIT_PREFIX):])
                    benefits.append(idx)
        return benefits

# Process personal info input.
def submit_personal_info(request):
    filename, filesize, rap_sheet = _load_vars_from_session(request)

    if request.method == 'POST':
        info_form = PersonalInfoForm(request.POST, events=rap_sheet.events)

        info_form.require_all_fields = False
        for field in info_form:
            field.required = False

        if info_form.is_valid():
            # for item in info_form.cleaned_data.items():
            #     print item
            print info_form.get_event_to_waiver_status()
            print info_form.get_benefits()

            return HttpResponseRedirect('/webapp/success')
    else:
        info_form = PersonalInfoForm(events=rap_sheet.events)

    template = loader.get_template('steps/complete_personal_info.html')
    context = RequestContext(request, {
        'filename': filename,
        'filesize': filesize,
        'rap_sheet': rap_sheet,
        'info_form': info_form
    })
    return HttpResponse(template.render(context))


# Render the success page with a button to download.
def success(request):
    context = RequestContext(request, {})
    return render(request, 'steps/success.html', context)


def _generate_forms(request):
    buf = cStringIO.StringIO()
    buf.write("foo")
    return buf.getvalue()


def download_forms(request):
    data = _generate_forms(request)
    response = HttpResponse(data)

    filename = 'record_expungment_forms.txt'
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    # set other headers
    return response
