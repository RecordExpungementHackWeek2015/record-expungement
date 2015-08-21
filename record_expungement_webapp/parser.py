# parser.py
#
# See if I can parse my test lines!
import ply.lex as lex
import ply.yacc as yacc


tokens = (
'DATE',
'NAME_LABEL',
'EVENT_START',
'COURT_HEADER',
'INDEX',
'CII_LABEL',
'TOC_LABEL',
'DOB_LABEL',
'DISPO_LABEL',
'ID_NUM',
'WORD',
'CNT_LABEL',
'CRIME_CATEGORY',
'CRIME_NUMBER',
'HEIGHT',
'WEIGHT',
'EYE_COLOR',
'AGENCY_ID',
'AMT_OF_MONTHS',
'AMT_OF_DAYS',
'MISTAKE', # so far anything with lower case letters
)

# Tokens

t_DATE = r'19\d{2}[0-1][0-9][0-3][0-9]|20\d{2}[0-1][0-9][0-3][0-9]'
t_NAME_LABEL = r'NAM[\/]+'
t_CII_LABEL = r'CII'
t_EVENT_START = r'^ARR[\/]DET[\/]C\w{3}[:]'
t_COURT_HEADER = r'^COURT[:]'
t_AMT_OF_MONTHS = r'\d{3}[ ]MONTHS'
t_AMT_OF_DAYS = r'\d{3}[ ]DAYS'
t_INDEX = r'0\d{2}' # 0 as the first digit, supposing a person doesn't commit over 99 crimes
t_TOC_LABEL = r'TOC[:][A-Z]'
t_DOB_LABEL = r'DOB[:\/]'
t_DISPO_LABEL = r'[\*]DISPO[:]'
t_ID_NUM = r'\#\w+'
t_CNT_LABEL = r'CNT'
t_HEIGHT = r'[ ]HGT[\/]\d+'
t_WEIGHT = r'[ ]WGT[\/]\d+'
t_EYE_COLOR = r'[ ]EYE[\/]\w+'
t_CRIME_CATEGORY = r'[A-Z][A-Z]-'
t_AGENCY_ID = r'CASO|CAPD|CASC|CACB|CAMC'
t_CRIME_NUMBER = r'\d+\(A*'
t_WORD = r'[A-Z_][A-Z]*' # text can't start with a number, must be all caps
t_MISTAKE = r'[a-z][A-Za-z0-9,_]*'

# defined literals
literals = "+-*/ :"

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
  print("Illegal character '%s'" % t.value[0])
  t.lexer.skip(1)

lexer = lex.lex()
#parser = yacc.yacc()

# Test data
data = '''
4CMTD693809.IH E, NW OP.E.cAo3494o0.11445154( PUSR. DATE:2015U303 EmE:( 07:22RESTRICTED—D0 NOT USE FOR EMPLOYMENT,LICENSING OR CERTIFICATION PURPOSESAIIE:APPUSR4* III CALIFORNIA ONLE SOURCE RECORDCII/DOB/ SEX/F RACXHISPARICHGT/504 WGT/120 EYE/BRO HA1/BRO POBXMXCTZ/MEXICONAM/001 S002 SIFBI_ .DOB/1 6DMV-Jr -J: 41- 4"ARR/DET/CITE: mmool DOB:l971-19960205 CASO REDEOOD CITYCNT:OU1 #1041065“CRT ORDER BOOK273D(AJ PC—INFLICT INJURY/ETC UPON CHILD TOC:F‘.4: :1: :4: -E:ARR/DET/CIIE: NAM:001 DOB:1967220021024 CASO REDWOOD CITYCNT:0Ul #477723—1041U65487(A) PC—GRARD THEFT:MONEY/LABOR/PROP TOC:FARR BY:CAPD GAR BRUEO -SCN:ll52297002lCOURT: RAM:00120021107 CASC SOUTH SAN FRANCISCOCRT:001 #NM324647487(A} PC—GRAND IREFI:MOREYXLABOR/PROP TOC:F*DISPO:CONVICTEDCONV sTAEUs:MIsDEMEAEORGEN: 018 MONTHS PROBATION, 005 DAYS JAILA S * END OF MESSAGE * 4 RPage 1 Of 1
'''

good_data = '''
.II_ _&UZ:RE¥ES¢J9SEwGONZA§§S_L

4cE&n204193.TH ~~ 9-

RE: QHY.CA0349400.U840376\h.PPUSR. DATE:20l50408 TIME(* :52:28
LRESTRICTED-DO NOT USE FOR EMPLOYMENT,LICENSING OR CERTIFICATION PURPOSES

ATTN:APPUSR

** PALM PRINT ON FILE AT DOJ FOR ADDITIONAL INFORMATION PLEASE E—MAIL

PALE.PRINT@OOJ.CA.GOv

** III CALIFORNIA ONLY SOURCE RECORD
CII/A08403?6?

DOB/19641023 SEX/M RAC/HISPANIC

HGT/50? NGT/135 EYE/BRO HAT/ERO POE/NM
CTZ/MEXICO _ -
NAM/001 RETES,JOSE G

003 GONZALEZ,JOSE REYES
U04 REYES,JOSE

U05 REYES—GONZALEZ,JOSE
U06 REYES,JOSE GONZALEZ

FBI/B943U7EA3

DOB/19661023 19661027

DMV/Ull905U5

SOC/562917818

SMT/CRIP L HND—UNKNOWN . ; SC L CHK—UNKNONN

SC L EYE—UNKNOWN ; SC L RNEE—UNKNONN
OCC/CASHIER; GENERAL HELPER;
HANDYMAN

:'r'.i:"iri.'

ARR/OET/CITE: NAM:001

19870130 CAPD SAN MATEO

CNT:00l #95024

594 PC—MALICIOUS MISCHIEF/VANDALISM

:k**J:'.-kit‘

ARR/BET/CITE: - NAM:0U2
19870322 CAPD SAN MATEO

CNT:0Ul #95631 _

594 PC—MALICIOUS MTSCHTEFXVANDALISM
COURT: NAM:002
19870629 CAMC SAN MATEO

'CNT:001 #E122974

594(A) PCyVANDALISM
*DISPO:CONVICTED
CONV STATUS:MISOEMEANOR
SEN: 002 YEARS PROBATION, 015 DAYS JAIL SS, RESTN

1|r'.ir'Jr:.l-

ARR/OET/CITE: NAM:0U3 DOB:l9641023
19980416 ' CASO REONOOU CITY-

CNT:001—002 #267789
166(A)(4) PC7CONTEMPT:DISOBEY COURT ORDER/ETC
ARR BY:CAPD SAN MATEO
NUMBER 8NM283362A
COURT: NAM:003
19980416 CAMC SOUTH SAN FRANCISCO

CNT:D0l #NM283362A

Page 1 Of 6

'''

lexer.input(good_data)

#DOESN'T WORK
def find_indexes(data):
    indexes = []
    types = []
    headerList = ['EVENT_START', 'COURT_HEADER', 'DISPO_LABEL', 'CNT_LABEL']
    while True:
        tok = lexer.token()
        if tok:
            types.append(str(tok.type))
            if types in headerList:
                indexes.append(tok.lexpos)
        else:
            break
    return indexes

def split_record(data, indexes):
    sections = []
    last_char_index = len(data) - 1
    for i, str_i in enumerate(indexes):
        if i != len(indexes) - 1:
            record = data[indexes[i]:indexes[i+1]-1]
            sections.append(record)
        else:
            break
    last_record = data[indexes[-1]:last_char_index]
    sections.append(last_record)
    return sections

#test indexes from data to pass into split_record
indexes = [317, 465, 627, 735]

#test indexes from good_data to pass into split_record
good_indexes = [338, 754, 870, 973, 1052, 1160, 1276, 1332]

# Tokenize the data
while True:
    tok = lexer.token()
    if tok:
        print(tok, tok.type)
    else:
        break
