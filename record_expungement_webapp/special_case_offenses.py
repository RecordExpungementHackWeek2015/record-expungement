from models import CrimeCategory


class IneligibleOffensesModel:
    _INELIGIBLE_OFFENSES = {
        "VC": ["42002.1", "2815", "22526(A)", "22526(B)"],
        "PC": ["286(C)", "288", "288(C)", "288.5", "289(J)",
               "311.1", "311.2", "311.3", "311.11"]
    }

    _INELIGIBLE_WITH_FELONY = {
        "PC": ["261.5(D)"]
    }

    def __init__(self):
        pass

    @staticmethod
    def offense_is_ineligible(offense_code, offense_id, type_of_crime):
        """
        :rtype : bool
        :type offense_code: str
        :type offense_id: str
        :type type_of_crime: str
        """
        if type_of_crime == CrimeCategory.INFRACTION:
            return True
        if offense_code in IneligibleOffensesModel._INELIGIBLE_OFFENSES:
            if offense_id in IneligibleOffensesModel._INELIGIBLE_OFFENSES[offense_code]:
                return True
        if type_of_crime == CrimeCategory.FELONY \
                and offense_code in IneligibleOffensesModel._INELIGIBLE_WITH_FELONY:
            if offense_id in IneligibleOffensesModel._INELIGIBLE_WITH_FELONY[offense_code]:
                return True
        return False


class WobblerOffensesModel:
    _WOBBLERS = {
        "PC": ["69", "71", "72", "76", "118.1", "136.1", "136.5", "136.7", "139", "142", "146(A)", "148(D)",
               "148.1", "148.10", "149", "153", "168", "171(B)", "171(C)", "171(D)", "186.10", "192(C)(1)",
               "192.5(A)", "219.2", "241.1", "241.4", "241.7", "243(C)(1)", "243.3", "243.4", "243.6",
               "243.7", "243.9"],
        "HS": ["11377", "11379.2", "11390", "11391"],
        "VC": ["10851", "23152", "23153"]
    }

    def __init__(self):
        pass

    @staticmethod
    def offense_is_a_wobbler(offense_code, offense_id, type_of_crime):
        """
        :rtype : bool
        :type offense_code: str
        :type offense_id: str
        :type type_of_crime: str
        """
        assert type_of_crime == CrimeCategory.FELONY
        if offense_code in WobblerOffensesModel._WOBBLERS:
            return offense_id in WobblerOffensesModel._WOBBLERS[offense_code]
