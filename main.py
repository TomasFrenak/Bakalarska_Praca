import matplotlib.pyplot as plt
from nbformat import write
import streamlit as st
import pandas as pd
import seaborn as sns
from PIL import Image

from data_cleaning import *
from last_fatal_crash import get_last_fatal

def streamlit_config(): 
    st.set_page_config(
        page_title="Bakalárska práca",
        initial_sidebar_state="expanded"
    )
    st.title('Dátová analýza v jazyku Python')
    col1,col2 = st.columns(2)
    return col1,col2


@st.cache    
def load_df():
    df1 = pd.read_csv('data/Traffic_Crash_Reports__CPD_1.csv', dtype = {8 : str,27: str})
    df2 = pd.read_csv('data/Traffic_Crash_Reports__CPD_2.csv', dtype = {8 : str,27: str})
      
    df = pd.concat([df1,df2])
    
    return df

def driver_age_plot(df,col1):
    sr_driver_age = df['AGE'][df['TYPEOFPERSON'] == 'D - DRIVER']
    sr_driver_age.dropna(inplace=True)
    sr_driver_age= sr_driver_age.astype(int)
    
    fig = sns.displot(sr_driver_age, bins = 17)
    col1.write("Počet nehôd vzhľadom na vek vodiča:")
    col1.pyplot(fig)
    
def driver_gender_plot(df,col2):
    sr_driver_gender = df['GENDER'][(df['TYPEOFPERSON'] == 'D - DRIVER') & (df['GENDER'] != 'UNKNOWN')]
    fig = sns.displot(sr_driver_gender)
    col2.write("Počet nehôd vzhľadom na pohlavie vodiča:")
    col2.pyplot(fig)
    
def time_graph():
    image = Image.open('data/lux_graph.png')
    st.write("Grafy vytvorené knižnicou LUX zobrazujúce vývoj počtu dopravných nehôd v čase")
    st.image(image)
    
def fatal_crashes_map(df):
    df_map = df[['LATITUDE_X', 'LONGITUDE_X']] [df['CRASHSEVERITY'] == '1 - FATAL INJURY']
    df_map.columns = ['latitude', 'longitude']
    df_map['latitude'] = pd.to_numeric(df_map['latitude'])
    df_map['longitude'] = pd.to_numeric(df_map['longitude'])
    df_map.dropna(how = 'any', inplace = True)
    df_map.drop(df_map['longitude'].idxmax(),inplace=True)
    st.write('Mapa smrteľných dopravných nehôd:')
    st.map(df_map, zoom = 10)
    
def filter_df(df,filter1,filter2):
    if filter1 == 'Muž':
        df = df[(df['TYPEOFPERSON'] == 'D - DRIVER') & (df['GENDER'] == 'MALE')]
    elif filter1 == 'Žena':
        df = df[(df['TYPEOFPERSON'] == 'D - DRIVER') & (df['GENDER'] == 'FEMALE')]
    else:
        pass
    
    df = df[df['AGE'] <= filter2]
    
    return df
    
def vehicle_type_graph(df,filter1,filter2):
    df = filter_df(df,filter1,filter2)
    df_unit = df['UNITTYPE'].value_counts()[:10]
    fig,ax = plt.subplots()
    ax =  df_unit.plot(kind = 'bar')
    st.pyplot(fig)

def crash_manner_graph(df,filter1,filter2):
    df = filter_df(df,filter1,filter2)
    df_manner = df['MANNEROFCRASH'].value_counts()[:10]
    fig,ax = plt.subplots()
    ax =  df_manner.plot(kind = 'bar')
    st.pyplot(fig)



def main():
    col1,col2 = streamlit_config()
    
    df = clean_data(load_df())
    
    with st.sidebar:
        st.header("Tomáš Frenák")
        
        option = st.sidebar.selectbox('Vyberte si možnosť:', ('Vizualizácie z bakalárskej práce','Vytvoriť vizualizáciu'))
               
        link_dataset = '[Stiahnuť dataset](https://data.cincinnati-oh.gov/api/views/rvmt-pkmq/rows.csv?accessType=DOWNLOAD)'
        st.markdown(link_dataset, unsafe_allow_html=True)
        
        link_code = '[Zrojový kód webstránky](https://github.com/TomasFrenak/Bakalarska_Praca)'
        st.markdown(link_code, unsafe_allow_html=True)
            
        link_bakalarka = '[Stiahnuť bakalársku prácu](https://opac.crzp.sk/?fn=detailBiblioForm&sid=D9F0BB0A8DA992698EA790D31B33&seo=CRZP-detail-kniha)'
        st.markdown(link_bakalarka, unsafe_allow_html=True)

    if option == 'Vizualizácie z bakalárskej práce':
        with st.spinner('Načítavam...'):
            get_last_fatal(col1,col2)
            driver_age_plot(df,col1)
            driver_gender_plot(df,col2)
            time_graph()
            fatal_crashes_map(df)

    elif option == "Vytvoriť vizualizáciu":
        choice = col1.radio("Vyberte si sledované kritérium:", ("Druh kolízie","Typ dopravného prostriedku"))
        filter = col2.radio("Pohlavie vodiča", ("Všetko", "Muž", "Žena"))
        filter2 = st.slider("Vek vodiča", min_value=15, max_value=100, value=100, step=1)
        
        with st.spinner('Načítavam...'):
            if choice == "Druh kolízie":
                crash_manner_graph(df,filter,filter2)
                
            elif choice == "Typ dopravného prostriedku":
                vehicle_type_graph(df,filter, filter2)
        
            
    
if __name__ == '__main__':
    main()