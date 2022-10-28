import streamlit as st
import pandas as pd

st.selectbox("Headquarter Region", ("Singapore", "Malaysia"))
st.selectbox("Last Funding Type", ("Seed", "Series A"))
st.selectbox("Last Funding Date", ("1-May-2022", "1-June-2021"))
st.selectbox("Investors", ("Vertex", "Other VC"))
st.write("*See entire list of filters in pitchbook/tracxn*")

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
pitchbook['Location'] = pitchbook['Location'].astype(str)
pitchbook = pitchbook[~pitchbook['Location'].str.contains('|'.join([
    'China',
    'CA',
    'MA',
    'WA',
    'WY',
    'DE',
    'Estonia',
    'Georgia',
    'NY',
    'British Virgin Islands',
    'Tajikistan',
    'CO',
    'NJ',
    'Seychelles',
]))]

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
tracxn = tracxn.drop_duplicates()

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

data = pd.concat([pitchbook, tracxn, preqin])
data.sort_values('Company', ascending=True, inplace=True)

data_csv = data.to_csv().encode('utf-8')

st.download_button(
    label="Download data as CSV",
    data=data_csv,
    file_name='large_df.csv',
    mime='text/csv',
)

st.dataframe(data)