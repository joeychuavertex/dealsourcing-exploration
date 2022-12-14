import streamlit as st
import pandas as pd

st.title("Preqin, Tracxn, Pitchbook Deduplication")

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
pitchbook_count = len(pitchbook)
st.header("Pitchbook")
st.metric(label="Count", value=pitchbook_count)
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
tracxn = tracxn.drop_duplicates()
tracxn_count = len(tracxn)
st.header("Tracxn")
st.metric(label="Count", value=tracxn_count)
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
preqin_count = len(preqin)
st.header("Preqin")
st.metric(label="Count", value=preqin_count)
st.dataframe(preqin)

dealroom = pd.read_csv("dealroom.csv")
dealroom['source'] = 'dealroom'
dealroom.sort_values(by=['r.year'])
dealroom = dealroom[['name', 'source', 'r.year', 'r.roundKind', 'headquarterCountry']]
dealroom.rename(columns={
    "name": "Company",
    "source": "Source",
    "r.year": "Last Financing Date",
    "r.roundKind": "Last Financing Deal Type",
    "headquarterCountry": "Location"
}, inplace=True)
dealroom = dealroom.drop_duplicates(subset=['Company'], keep='last')
dealroom_count = len(dealroom)
st.header("Dealroom")
st.metric(label="Count", value=dealroom_count)
st.dataframe(dealroom)


data = pd.concat([pitchbook, tracxn, preqin, dealroom])
data.sort_values('Company', ascending=True, inplace=True)
combined_count = len(data)
st.header("Combined")
st.metric(label="Count", value=combined_count)
st.dataframe(data)


data_same = pd.concat([pitchbook, tracxn, preqin, dealroom])

data_exact = data_same[data_same.duplicated('Company', keep=False)]
data_exact.sort_values('Company', ascending=True, inplace=True)
st.header("Same Companies")
samedata_count = len(data_exact)
samecompany_count = len(data_exact.drop_duplicates(subset=['Company'], keep='last'))

count, unique = st.columns(2)
count.metric(label="Total Same Companies Count", value=samedata_count)
unique.metric(label="Unique Companies Count", value=samecompany_count)
st.dataframe(data_exact)
