import pandas as pd 
import streamlit as st 



st.set_page_config(layout='wide',page_title='Startup Analysis')

df = pd.read_csv('startup_cleaned.csv')
df['date'] = pd.to_datetime(df['date'], errors = 'coerce')
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['vertical'] = df['vertical'].str.replace('eCommerce','E-Commerce')
df['vertical'] = df['vertical'].str.replace('ECommerce','E-Commerce')
df['vertical'] = df['vertical'].str.replace('ECommerce Marketplace','E-Commerce')
df['city'] = df['city'].str.replace('Bengaluru','Bangalore')

def load_overall_analysis():
    st.title('Overall Analysis')

    #total invested amount          
    total = round(df['amount'].sum())
    #max amount infused in startup
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    #avg ticket size
    avg_funding = df.groupby('startup')['amount'].sum().mean()
    #total funded startup
    num_startups = df['startup'].nunique()

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.metric('Total Funding',str(total) + 'Cr')
    with col2:
        st.metric('Max Funding',str(max_funding) + 'Cr')
    with col3:
        st.metric('Avg Funding',str(round(avg_funding)) + 'Cr')
    with col4:
        st.metric('No. of Funded Startups',str(num_startups))

    #MoM Graph
    st.header('MoM graph')
    mom_selected_option = st.selectbox('Select Type',['Total','Count'])
    if mom_selected_option == 'Total':
        temp_df = df.groupby(['year','month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year','month'])['amount'].count().reset_index()
    temp_df['x_axis'] = temp_df['year'].astype(str) + '-' + temp_df['month'].astype(str)
    fig6, ax6 = plt.subplots()
    ax6.plot(temp_df['x_axis'],temp_df['amount'])
    ax6.set_xticklabels(temp_df['x_axis'], rotation='vertical')
    st.pyplot(fig6)

    #Sector Analysis
    st.header('Sector Analysis Pie-Chart')
    sector_selected_option = st.selectbox('Select Type',['Sum','Count'])
    if sector_selected_option == 'Sum':
        sector_data = df.groupby('vertical')['amount'].sum().sort_values(ascending=False).head(10)
    else:
        sector_data = df.groupby('vertical')['amount'].count().sort_values(ascending=False).head(10)
    fig7, ax7 = plt.subplots()
    ax7.pie(sector_data, labels=sector_data.index, autopct="%0.01f")
    st.pyplot(fig7)

    #Type of funding
    st.header('Round Analysis')
    funding_selected_option = st.selectbox('Select_Type',['Sum','Count'])
    if funding_selected_option == 'Sum':
        funding_series = df.groupby('round')['amount'].sum().sort_values(ascending=False)
    else:
        funding_series = df.groupby('round')['amount'].count().sort_values(ascending=False)
    fig8, ax8 = plt.subplots()
    ax8.bar(funding_series.index , funding_series.values)
    ax8.set_xticklabels(funding_series.index, rotation='vertical')       
    st.pyplot(fig8)

    #City wise funding
    st.header('City wise funding Analysis')
    city_funding = df.groupby('city')['amount'].sum().sort_values(ascending=False)
    fig9, ax9 = plt.subplots()
    ax9.pie(city_funding, labels=city_funding.index, autopct="%0.01f")
    st.pyplot(fig9)


def load_investor_details(investor): 
    st.header(investor)

    #load the recent 5 investments of investor
    last5_df = df[df['investors'].str.contains(investor)].head()[['date','startup','vertical','city','round','amount']]
    st.subheader("Most Recent Investments")
    st.dataframe(last5_df)
    col1, col2 = st.columns(2)
    with col1:
        #biggest investments
        big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader("Biggest Investments")
        fig, ax = plt.subplots()
        ax.bar(big_series.index,big_series.values)
        st.pyplot(fig)
    with col2:
        vertical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        st.subheader("Sector Invested In")
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series, labels=vertical_series.index,autopct= "%0.01f")
        st.pyplot(fig1)
    col3,col4 = st.columns(2)
    with col3:
    #Investment Round
        round_series = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()
        st.subheader("Round of Investments")
        fig3, ax3 = plt.subplots()
        ax3.pie(round_series,labels=round_series.index,autopct= "%0.01f")
        st.pyplot(fig3)
    with col4:
    #Investment of money in which city
        city_series = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()
        st.subheader("City-wise Investment")
        fig4, ax4 = plt.subplots()
        ax4.pie(city_series,labels=city_series.index,autopct= "%0.01f")
        st.pyplot(fig4)
    #YoY Investment
    df['year'] = df['date'].dt.year
    year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
    st.subheader("YoY Investment")
    fig5, ax5 = plt.subplots()
    ax5.plot(year_series.index,year_series.values)
    st.pyplot(fig5)


def load_startup_deatils(Startup):
    st.header(Startup)

    #Funding Rounds
    stage = df[df['startup'].str.contains(Startup)][['date','round','investors','city','vertical','subvertical']]
    st.dataframe(stage)
    

st.sidebar.title('Starup Funding Analysis') 

option = st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investor'])

if option == 'Overall Analysis':
        load_overall_analysis()
elif option == 'Startup':
    st.title('Startup Details...')
    selected_startup = st.sidebar.selectbox('Select Startup',sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup Details')
    if btn1:
        load_startup_deatils(selected_startup)

else:
    st.title('Investor Analysis')
    selected_investor = st.sidebar.selectbox('Select Investor',sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)

