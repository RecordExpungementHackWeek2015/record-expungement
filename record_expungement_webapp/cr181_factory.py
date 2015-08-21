from form_util import FormUtil, FormModel


class CR181Model(FormModel):
    def __init__(self):
        raise ValueError("Don't construct me")

    @staticmethod
    def get_name():
        return "cr_180"

    @staticmethod
    def get_output_file_name():
        return "cr_180.pdf"

    @staticmethod
    def get_fields(ph, event):
        """
        :type ph: PersonalHistory
        :type event: Event
        """

        return FormUtil.cr_180_header(ph, event) + FormUtil.cr_180_header_2(ph, event)
