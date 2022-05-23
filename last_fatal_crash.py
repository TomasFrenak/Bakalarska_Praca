import requests
import pandas as pd
import streamlit as st

def get_last_fatal(col1,col2):

    r = requests.get("https://data.cincinnati-oh.gov/resource/rvmt-pkmq.json")

    df = pd.DataFrame(r.json())

    df['Date'] = pd.to_datetime(df['crashdate'])
    df['Date'] = df['Date'].dt.date

    df_fatal = df[df['crashseverityid'] == '201901']

    date = df_fatal['Date'].max()
    death_count = df_fatal['instanceid'][df_fatal['Date'] == date].count()

    if death_count > 0:
        col1.text(f'Posledná smrteľná nehoda: {date} -->')
        col2.text(f'Počet úmrtí: {death_count} ')
        
    else:
        col1.text(f"Od {df['Date'].min()} sme nezaznemenali žiadnu nehodu")
        col2.text(f"")