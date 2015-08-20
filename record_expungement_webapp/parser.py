# parser.py
#
# See if I can parse my test lines!
import ply.lex as lex
import ply.yacc as yacc


tokens = (
'DATE',
'NAME',
'EVENT_START',
'COURT_HEADER',
'INDEX',
'TOC_LABEL',
'DOB_LABEL',
'DISPO_LABEL',
'ID_NUM',
'WORD',
'CNT_LABEL',
'CRIME_CATEGORY'
)

# Tokens

t_DATE = r'19\d{2}[0-1][0-9][0-3][0-9]|20\d{2}[0-1][0-9][0-3][0-9]+/g' #(\d{4}\d{2}\d{2})
t_NAME = r'NAM[\/]+/g'
t_EVENT_START = r'ARR[\/]DET[\/]C'
t_COURT_HEADER = r'COURT[:]'
t_INDEX = r'[ :]0\d{2}'
t_TOC_LABEL = r'TOC[:][A-Z]'
t_DOB_LABEL = r'DOB[:\/]'
t_DISPO_LABEL = r'DISPO[:]'
t_ID_NUM = r'\#\w+'
t_CNT_LABEL = r'CNT'
t_CRIME_CATEGORY = r'[A-Z][A-Z][-]'
#t_WORD = r'[A-Z_][A-Z0-9_,]*' # text can't start with a number

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

lexer.input(data)

# Tokenize the data
while True:
    tok = lexer.token()
    if not tok:
        break # no more input
    print(tok)
