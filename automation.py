import os
import sys
import pandas as pd
import numpy as np
import pyodbc
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s -  %(levelname)s  -  %(message)s')

os.chdir(r'C:\Users\quantec\Desktop\work at office\QRAPS-automation')

logging.debug('Connecting to the database using pyodbc')

# pyodbc를 이용해 database에 connect
conn = pyodbc.connect(
    r'DRIVER={ODBC Driver 13 for SQL Server};'
    r'DATABASE=Quantec_Financial_Database;'
    r'SERVER=192.168.103,49990;'
    r'UID=QTCLIENTUSER;'
    r'PWD=qt0330'
)

TopN = [10, 20, 30, 40]
STTV = [0.5, 5, 10]

def df_gen(TopN, STTV):
    for topn in TopN:
        for sttv in STTV:
            with open('test.sql') as t:
                yield pd.read_sql_query(t.read().replace('set @진입종목수 = 10', f'set @진입종목수 = {topn}').replace('0.5----', f'{sttv}----'), conn)

IndexLenWarningList = []
for filename in os.listdir(os.getcwd()):
    if filename.endswith('sql'):
        with open(filename) as t:
            SqlText = t.read()

        logging.debug(f'Currently working on {filename}')

        assert 'set @진입종목수 = 10' in SqlText, "'set @진입종목수 = 10' should be inside the sql file."
        assert '0.5----' in SqlText, "'0.5----' should be inside the sql file."

        for topn in TopN:
            for sttv in STTV:
                logging.debug(f'TopN={topn}, STTV={sttv}')

                # NewSQLName = os.path.splitext(filename)[0] + f' Top{topn}' + f' STTV{sttv}' + '.sql'
                directory = os.path.join(os.getcwd(), os.path.splitext(filename)[0] + f'_Top{topn}' + f'_STTV{sttv}')
                directory = directory.replace(" ", "").replace('workatoffice', 'work at office')
                if not os.path.exists(directory):
                    os.makedirs(directory)

                logging.debug('Querying...')

                Data = pd.read_sql_query(
                    SqlText.replace('set @진입종목수 = 10', f'set @진입종목수 = {topn}').replace('0.5----', f'{sttv}----'),
                    conn)

                logging.debug('Saving excel files...')

                for date in Data['날짜'].drop_duplicates():
                    Data1 = Data[Data['날짜']==date].iloc[:, 0:4]
                    Data1.iloc[:, 1] = Data1.iloc[:, 1].str.strip()

                    if len(Data1.index) != topn:
                        logging.debug(f'Warning: {len(Data1.index)} does not equal {topn}')
                        IndexLenWarningList.append((filename, len(Data1.index), topn, sttv))

                    Data1.to_csv(os.path.join(directory, f'{date[:6]}_tot.csv'), encoding='euc_kr', index=False, header=False)

with open ('Index Length Warning.txt', 'w') as t:
    for item in IndexLenWarningList:
        t.write(str(item)+'\n')