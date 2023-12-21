import pandas as pd 
import streamlit as st 

df = pd.read_csv('startup_funding.csv')
# Data cleaning
df['Investors Name'] = df['Investors Name'].fillna('Undisclosed')

st.sidebar.title('Starup Funding Analysis') 

option = st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investor'])

if option == 'Overall Analysis':
    st.title('Overall Analysis')
elif option == 'Startup':
    st.title('Startup')
    st.sidebar.selectbox('Select Startup',sorted(df['Startup Name'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup Details')
else:
    st.title('Investor')
    st.sidebar.selectbox('Select Investor',sorted(df['Investors Name'].unique().tolist()))
    btn1 = st.sidebar.button('Find Investor Details')

