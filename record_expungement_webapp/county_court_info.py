# from types import FunctionType
from models import Address

# class CountyCourtInfo:
#     def __init__(self):
#         methods = [name for name, value in self.__dict__.items() if type(value) == FunctionType]
#         expected_methods = ["san_mateo_county_court_mailing_address"]
#         assert all(method in expected_methods for method in methods)


class SanMateoCountyCourt:
    _COUNTY_NAME = "SAN MATEO"
    _ADDRESS = Address("400 COUNTY CENTER", "REDWOOD CITY", "CA", "94063")

    def __init__(self):
        pass

    @staticmethod
    def county_name():
        return SanMateoCountyCourt._COUNTY_NAME

    @staticmethod
    def chief_probation_officer_name_and_title_str():
        return "CHIEF JOHN KEENE, PROBATION DEPARTMENT"

    @staticmethod
    def mailing_address_multiline_str():
        """
        :rtype : str
        """
        return SanMateoCountyCourt._COUNTY_NAME + "\n" + SanMateoCountyCourt._ADDRESS.to_str_multiline()

    @staticmethod
    def mailing_address_oneline_str():
        """
        :rtype : str
        """
        return SanMateoCountyCourt._ADDRESS.to_str_one_line()

    @staticmethod
    def mailing_address():
        """
        :rtype : Address
        """
        return SanMateoCountyCourt._ADDRESS

    @staticmethod
    def contains_city(city):
        """
        :type city: str
        """
        return city in ["REDWOOD CITY"]
