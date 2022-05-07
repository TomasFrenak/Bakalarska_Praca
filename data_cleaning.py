import pandas as pd
import streamlit as st

@st.cache
def clean_data(df):
    df = df.drop(df[(df['AGE'] < 15) & (df['TYPEOFPERSON'] == 'D - DRIVER')].index)
    df = df.drop(df[df['AGE'] > 100].index)

    for i in range(1,6):
        df['CRASHSEVERITYID'].mask(df['CRASHSEVERITYID'] == 201900 + i, i, inplace=True)

    df.dropna(subset=['CRASHSEVERITYID'], inplace=True)
    df['CRASHSEVERITYID'] = df['CRASHSEVERITYID'].astype(int)

    df['GENDER'].mask(df['GENDER'] == 'F - FEMALE', 'FEMALE', inplace=True)
    df['GENDER'].mask(df['GENDER'] == 'M - MALE', 'MALE', inplace=True)
    df['GENDER'].mask(df['GENDER'] == 'U - UNKNOWN', 'UNKNOWN', inplace=True)
    df['GENDER'].mask(df['GENDER'].isna(), 'UNKNOWN', inplace=True)

    df['CRASHSEVERITY'].mask(df['CRASHSEVERITY'] == '3 - PROPERTY DAMAGE ONLY (PDO)', '5 - PROPERTY DAMAGE ONLY', inplace=True)
    df['CRASHSEVERITY'].mask(df['CRASHSEVERITY'] == '1 - FATAL', '1 - FATAL INJURY', inplace=True)
    df['CRASHSEVERITY'].mask(df['CRASHSEVERITY'] == '2 - SERIOUS INJURY SUSPECTED', '2 - INJURY', inplace = True)

    df['INJURIES'].mask(df['INJURIES'] == '5 - FATAL', '1 - FATAL INJURY', inplace=True)
    df['INJURIES'].mask(df['INJURIES'] == '1 - NO INJURY / NONE REPORTED', '5 - NO APPARENTY INJURY', inplace=True)
    df['INJURIES'].mask(df['INJURIES'] == '4 - INCAPACITATING', '2 - SERIOUS INJURY', inplace=True)
    df['INJURIES'].mask(df['INJURIES'] == '2 - POSSIBLE', '4 - POSSIBLE INJURY', inplace=True)
    df['INJURIES'].mask(df['INJURIES'] == '2 - SUSPECTED SERIOUS INJURY', '2 - SERIOUS INJURY', inplace=True)
    df['INJURIES'].mask(df['INJURIES'] == '3 - SUSPECTED MINOR INJURY', '3 - MINOR INJURY', inplace=True)
    df['INJURIES'].mask(df['INJURIES'] == '3 - NON-INCAPACITATING', '3 - MINOR INJURY', inplace=True)
    df['INJURIES'].mask(df['INJURIES'] == '1 - FATAL', '1 - FATAL INJURY', inplace=True)

    df['ROADCONDITIONSPRIMARY'].mask(df['ROADCONDITIONSPRIMARY'] == '09 - UNKNOWN', '09 - OTHER', inplace=True)
    df['ROADCONDITIONSPRIMARY'].mask(df['ROADCONDITIONSPRIMARY'] == '10 - OTHER', '09 - OTHER', inplace=True)
    df['ROADCONDITIONSPRIMARY'].mask(df['ROADCONDITIONSPRIMARY'] == '99 - UNKNOWN', '09 - OTHER', inplace=True)

    df['LIGHTCONDITIONSPRIMARY'].mask(df['LIGHTCONDITIONSPRIMARY'] == '2 - DUSK', '2 - DAWN', inplace=True)
    df['LIGHTCONDITIONSPRIMARY'].mask(df['LIGHTCONDITIONSPRIMARY'] == '3 - DUSK', '2 - DAWN', inplace=True)
    df['LIGHTCONDITIONSPRIMARY'].mask(df['LIGHTCONDITIONSPRIMARY'] == '4 - DARK – ROADWAY NOT LIGHTED', '5 - DARK – ROADWAY NOT LIGHTED', inplace=True)
    df['LIGHTCONDITIONSPRIMARY'].mask(df['LIGHTCONDITIONSPRIMARY'] == '5 - DARK – UNKNOWN ROADWAY LIGHTING', '9 - UNKNOWN', inplace=True)

    return df

