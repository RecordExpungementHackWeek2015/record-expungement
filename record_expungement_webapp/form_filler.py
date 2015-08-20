import json
import os
import subprocess


class FormFiller:
    def __init__(self, form_name, form_location):
        self.form_name = form_name
        self.form_location = form_location

    def get_fields(self):
        json_file_path = os.path.join(self.form_location, self.form_name)
        json_file_path += "_fields.json"
        with open(json_file_path) as json_file:
            return json.load(json_file)

    def fill(self, fields_json, output_pdf_path, form_filler_bin=None):
        if form_filler_bin is None:
            from django.conf import settings
            assert hasattr(settings, 'FORM_FILLER_BIN'), "PDF generation requires form_filler. Edit your FORM_FILLER_BIN settings accordingly."
            form_filler_bin = settings.FORM_FILLER_BIN

        input_pdf_path = os.path.join(self.form_location, self.form_name)
        input_pdf_path += ".pdf"
        cmd = [
            form_filler_bin,
            'fill',
            input_pdf_path,
            output_pdf_path,
        ]
        cmd = ' '.join(cmd)
        try:
            process = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE, shell=True)
            return process.communicate(input=json.dumps(fields_json))
        except OSError:
            return None
