import cStringIO
import pickle

from django import forms
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.template import RequestContext

from record_expungement_webapp import models


_MOCK_CASE_INFO1 = models.CaseInfo()
_MOCK_CASE_INFO1.case_id = 'case 1'

_MOCK_CASE_INFO2 = models.CaseInfo()
_MOCK_CASE_INFO2.case_id = 'case 2'

_MOCK_EVENT1 = models.Event()
_MOCK_EVENT1.case_info = _MOCK_CASE_INFO1

_MOCK_EVENT2 = models.Event()
_MOCK_EVENT2.case_info = _MOCK_CASE_INFO2

_MOCK_RAP_SHEET = models.RAPSheet({1: "Foo Bar"})
_MOCK_RAP_SHEET.events = [_MOCK_EVENT1, _MOCK_EVENT2]


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
    rap_sheet = _MOCK_RAP_SHEET
    return rap_sheet


def _load_vars_from_session(request):
    rap_sheet = request.session.get('rap_sheet')
    rap_sheet = pickle.loads(rap_sheet)

    filename = request.session.get('filename')
    filesize = request.session.get('filesize')
    return (filename, filesize, rap_sheet)


# Render the parsed rap sheet and personal info form.
def complete_personal_info(request):
    filename, filesize, rap_sheet = _load_vars_from_session(request)

    template = loader.get_template('steps/complete_personal_info.html')
    context = RequestContext(request, {
        'filename': filename,
        'filesize': filesize,
        'rap_sheet': rap_sheet,
        'info_form': PersonalInfoForm(events=rap_sheet.events),
    })

    return HttpResponse(template.render(context))


# Personal and financial info form.
class PersonalInfoForm(forms.Form):
    email = forms.CharField(label='Email', max_length=100)

    def __init__(self, events=[]):
        super(PersonalInfoForm, self).__init__()
        self.events = events
        for i, e in enumerate(events):
            field_name = 'waiver_%d' % i
            self.fields[field_name] = forms.BooleanField(label=e)

    # Get zipped list of event to waiver field.
    def waiver_fields(self):
        result = []
        for name in self.fields:
            if name.startswith('waiver_'):
                result.append(self[name])
        return zip(self.events, result)


# Process personal info input.
def submit_personal_info(request):
    filename, filesize, rap_sheet = _load_vars_from_session(request)

    if request.method == 'POST':
        info_form = PersonalInfoForm(request.POST)
        if info_form.is_valid():
            # Maybe try generating form or other server-side validation here.
            return HttpResponseRedirect('/webapp/success')
        else:
            info_form = PersonalInfoForm()

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
    # provide button to download the pdf
    # del session vars somewhere
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
