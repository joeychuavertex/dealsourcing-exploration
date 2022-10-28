import streamlit as st
import pandas as pd

pitchbook = pd.read_csv("pitchbook.csv")
pitchbook['source'] = 'pitchbook'
pitchbook = pitchbook[['Companies', 'source', 'Last Financing Date', 'Last Financing Deal Type', 'HQ Location']]
pitchbook.rename(columns={
    "Companies": "Company",
    "source": "Source",
    "Last Financing Date": "Last Financing Date",
    "Last Financing Deal Type": "Last Financing Deal Type",
    "HQ Location": "Location"
}, inplace=True)
st.header("Pitchbook")
st.dataframe(pitchbook)

tracxn = pd.read_csv("tracxn.csv")
tracxn['source'] = 'tracxn'
tracxn = tracxn[['Company Name', 'source', 'Latest Funded Date', 'Company Stage', 'Country']]
tracxn.rename(columns={
    "Company Name": "Company",
    "source": "Source",
    "Latest Funded Date": "Last Financing Date",
    "Company Stage": "Last Financing Deal Type",
    "Country": "Location"
}, inplace=True)
st.header("Tracxn")
st.dataframe(tracxn)

preqin = pd.read_csv("preqin.csv")
preqin['source'] = 'preqin'
preqin = preqin[['COMPANY NAME', 'source', 'MOST RECENT DEAL DATE', 'MOST RECENT DEAL TYPE/STAGE', 'COUNTRY']]
preqin.rename(columns={
    "COMPANY NAME": "Company",
    "source": "Source",
    "MOST RECENT DEAL DATE": "Last Financing Date",
    "MOST RECENT DEAL TYPE/STAGE": "Last Financing Deal Type",
    "COUNTRY": "Location"
}, inplace=True)
st.header("Preqin")
st.dataframe(preqin)

data = pd.concat([pitchbook, tracxn, preqin])
data.sort_values('Company', ascending=True, inplace=True)
st.header("Combined")
st.dataframe(data)