
from datetime import datetime
from datetime import timedelta

from record_expungement_webapp import models


ARREST_INFO_0 = models.ArrestInfo(
    arrest_id='137680',
    name_as_charged_id=0,
    date=datetime(1979, 5, 17),
    city='REDWOOD CITY'
    )
EVENT_0 = models.Event(
    arrest_info=ARREST_INFO_0,
    listed_dob=datetime(1953, 4, 20),
    associated_cases=[],
    probation_modifications=[]
    )


COUNT_COURT_1_1 = models.Count(
    offense=models.Offense(
        code='BP',
        offense_id='4149',
        description='POSSESS HYPODERMIC NEEDLE/SYRINGE'
    ),
    disposition=models.Disposition(
        disposition_decision=models.DispositionDecision.DISMISSED,
        crime_category=None
        )
    )
COUNT_COURT_1_2 = models.Count(
    offense=models.Offense(
        code='HS',
        offense_id='11364',
        description='POSSESS CONTROL SUBSTANCE PARAPHERNA'
    ),
    disposition=models.Disposition(
        disposition_decision=models.DispositionDecision.DISMISSED,
        crime_category=None
        )
    )
COUNT_COURT_1_3 = models.Count(
    offense=models.Offense(
        code='HS',
        offense_id='11377',
        description='POSSESS CONTROLLED SUBSTANCE'
    ),
    disposition=models.Disposition(
        disposition_decision=models.DispositionDecision.CONVICTED,
        crime_category=models.CrimeCategory.MISDEMEANOR
        )
    )
CASE_INFO_1_1 = models.CaseInfo(
    case_id='NM239120A',
    date=datetime(1995, 5, 18),
    county='SOUTH SAN FRANCISCO',
    counts=[COUNT_COURT_1_1, COUNT_COURT_1_2, COUNT_COURT_1_3],
    sentence=models.Sentence(
        probation_duration=timedelta(weeks=78),
        incarceration=models.Incarceration(
            incarceration_type=models.IncarcerationType.JAIL,
            duration=timedelta(days=26)
            ),
        fine=False
        )
    )
ARREST_INFO_1 = models.ArrestInfo(
    arrest_id='0801030',
    name_as_charged_id=3,
    date=datetime(1993, 9, 7),
    city='REDWOOD CITY'
    )
EVENT_1 = models.Event(
    arrest_info=ARREST_INFO_1,
    listed_dob=datetime(1953, 4, 20),
    associated_cases=[CASE_INFO_1_1],
    probation_modifications=[]
    )

COUNT_COURT_2_1 = models.Count(
    offense=models.Offense(
        code='HS',
        offense_id='11550',
        description='USE/UNDER INFL CONTROLD SUBSTANCE'
    ),
    disposition=models.Disposition(
        disposition_decision=models.DispositionDecision.CONVICTED,
        crime_category=models.CrimeCategory.MISDEMEANOR
        )
    )
COUNT_COURT_2_2 = models.Count(
    offense=models.Offense(
        code='HS',
        offense_id='11377',
        description='POSSESS CONTROLLED SUBSTANCE'
    ),
    disposition=models.Disposition(
        disposition_decision=models.DispositionDecision.CONVICTED,
        crime_category=models.CrimeCategory.FELONY
        )
    )
CASE_INFO_2_1 = models.CaseInfo(
    case_id='176456',
    date=datetime(1994, 11, 4),
    county='SAN JOSE',
    counts=[COUNT_COURT_2_1, COUNT_COURT_2_2],
    sentence=models.Sentence(
        probation_duration=timedelta(weeks=52),
        incarceration=models.Incarceration(
            incarceration_type=models.IncarcerationType.JAIL,
            duration=timedelta(days=90)
            ),
        fine=False
        )
    )
ARREST_INFO_2 = models.ArrestInfo(
    arrest_id='9483488DIP657',
    name_as_charged_id=2,
    date=datetime(1994, 6, 10),
    city='SAN JOSE'
    )
EVENT_2 = models.Event(
    arrest_info=ARREST_INFO_2,
    listed_dob=datetime(1953, 4, 20),
    associated_cases=[CASE_INFO_2_1],
    probation_modifications=[]  # todo
    )

RAP_SHEET_1 = models.RAPSheet(
    names_as_charged=[
        'ALEXANDER, ROBIN RAE',
        'MOAN, ROBIN RAE',
        'LEDEL, ROBIN RAE',
        'LEDEL, ROBIN',
        'SUMMERS, KARLA',
        'LEDEL, RUBIN RAE',
        'SUMMERS, CARTA',
        'TYREE, ROBIN',
        'TYREE, ROBIN RAE',
        'ALEXANDER, ROBIN',
        'TYREE, ROBIN R'
    ],
    dob=datetime(1953, 4, 20, 0, 0),
    sex='F',
    events=[EVENT_0, EVENT_1, EVENT_2])

