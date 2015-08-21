import os
from cr180_factory import CR180Model
from cr181_factory import CR181Model
from pos040_factory import POS040Model
from fw001_factory import FW001Model
from fw003_factory import FW003Model

from form_util import FormUtil, FormModel
from form_filler import FormFiller
import shutil


class PacketFactory:
    def __init__(self):
        raise ValueError("Don't construct me")

    @staticmethod
    def generate(ph,  event, packet_output_folder, resources_directory):  # ==> saves PDF
        """
        :type ph: PersonalHistory
        :type event: Event
        """

        if os.path.exists(packet_output_folder):
            shutil.rmtree(packet_output_folder)
        os.makedirs(packet_output_folder)

        PacketFactory.generate_form(CR180Model, ph, event, packet_output_folder, resources_directory)
        PacketFactory.generate_form(CR181Model, ph, event, packet_output_folder, resources_directory)
        PacketFactory.generate_form(POS040Model, ph, event, packet_output_folder, resources_directory)
        PacketFactory.generate_form(FW001Model, ph, event, packet_output_folder, resources_directory)
        PacketFactory.generate_form(FW003Model, ph, event, packet_output_folder, resources_directory)

    @staticmethod
    def generate_form(form_model, ph, event, packet_output_folder, resources_directory):  # ==> saves PDF
        """
        :type form_model: FormModel
        """
        print "***** GENERATING FORMS FOR " + form_model.get_name()
        fields_list = form_model.get_fields(ph, event)
        form_filler = FormFiller(form_model.get_name(), resources_directory)
        json_list = form_filler.get_fields()
        json_list = FormUtil.fill_field_json_with_field_list(json_list, fields_list)
        output_path = os.path.join(packet_output_folder, form_model.get_output_file_name())
        form_filler.fill(json_list, output_path)
