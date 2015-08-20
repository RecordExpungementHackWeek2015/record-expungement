from form_util import FormUtil


class CR181Factory:
    def __init__(self):
        raise ValueError("Don't construct me")

    @staticmethod
    def generate(ph, event):
        """
        :type ph: PersonalHistory
        :type event: Event
        """

        return FormUtil.cr_180_header(ph, event) + FormUtil.cr_180_header_2(ph, event)
