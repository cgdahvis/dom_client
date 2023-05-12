import pandas as pd
import streamlit as st

path=r"blotter.xlsx"
df=pd.read_excel(path)

df=df[df['Client'].str.contains('GU')]

#make column 'client name' from 'client' by removing the text in between the parentheses
df['Client Name']=df['Client'].str.split('(').str[0]


#create column for difference between 'Sett Date' and 'Trade Date'
df['Sett Date']=pd.to_datetime(df['Sett Date'])
df['Trade Date']=pd.to_datetime(df['Trade Date'])
df['Option Expiry']=df['Sett Date']-df['Trade Date']
df['Option Expiry']=df['Option Expiry'].dt.days

st.title('Client List')
coverage=df['Trade Swap'].unique()
selected_coverage=st.multiselect('Select Coverage', coverage, default="DSOOD")

#make client_list dependent on coverage
client_list = df[df['Trade Swap'].isin(selected_coverage)]['Client Name'].unique()
selected_cients = st.multiselect('Select Clients', client_list, default=client_list)
plot_df = df[df['Client Name'].isin(selected_cients)]

#display firsta dn last trade dates as just dates
st.write('First Trade Date:', plot_df['Trade Date'].min())
st.write('Last Trade Date:', plot_df['Trade Date'].max())


#list most recent trades
st.write('Most Recent Trades')
st.write(plot_df[['Client Name', 'Trade Date', 'Ccy Pair', 'B/S','Rate','Strike','C/P','Price','Expiry Date','Barrier Type','Lower Barrier','Upper Barrier','Knock In/Out','Touch Up/Dn']].sort_values(by='Trade Date', ascending=False).head(50))

#make graph displaying client frequency of each ccy pair using unique trade dates
st.write('Frequency of Trades by Ccy Pair')
st.bar_chart(plot_df.groupby('Ccy Pair')['Trade Date'].nunique())

#show most active clients in each ccy pair using nuique trade dates
st.write(plot_df.groupby('Ccy Pair')['Trade Date'].nunique(), )

#groupby client and show Sett trade diff
st.write('Avg. Option Expiry by Client')
st.bar_chart(plot_df.groupby('Client Name')['Option Expiry'].mean())

#groupby client and show median option expiry
st.write('Median Option Expiry by Client')
st.bar_chart(plot_df.groupby('Client Name')['Option Expiry'].median())


# st.write(plot_df)
