from io import StringIO
import requests
import streamlit as st
import pandas as pd
import datetime
import altair as alt
import time
import os
import g4f

def chat_bot(prompt):
    response = g4f.ChatCompletion.create(
        # model="gpt-3.5-turbo",
        model=g4f.models.default,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )

    return response

@st.cache_resource
def generate_summary(df):
    csv_data_str = df.to_string(index=False)
    prompt = f"Here opbnb L2 chain myshell.ai data\n{csv_data_str}\ngive some short summary insights about the data in 6 sentences and there connections in points"
    st.write(chat_bot(prompt))


# Define the API endpoint and your API key
API_URL = "https://api.dune.com/api/v1/query/{query_id}/results/csv"
API_KEY = "NJoI9Yz7jPHhaaOmtalgfARPLI9p0x8H"

def fetch_data(api_url, api_key):
    # Prepare headers with API key
    headers = {
        "X-Dune-Api-Key": api_key
    }

    # Make GET request to the API URL with headers
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        # Read CSV data into pandas DataFrame
        df = pd.read_csv(StringIO(response.text))
        return df
    else:
        st.error(f"Failed to load data: {response.status_code} - {response.reason}")
        return None
    
def data(query_id):
    query_id = query_id  # Replace with actual query ID
    api_url = API_URL.format(query_id=query_id)

    df = fetch_data(api_url, API_KEY)

    if df is not None:
        return df
    


def myshell():
    prompt = f"Explain about  myshell.ai decentralized sta king AI native apps protocol  in 3 points"
    st.write(chat_bot(prompt))
    st.markdown("##")
    a,b = st.columns([2,2])
    df = data("3933070")
    df_1 = data("3933101")
    df['date'] = pd.to_datetime(df.date, errors='coerce')
    df_1['date'] = pd.to_datetime(df_1.date, errors='coerce')
    with a:
        st.altair_chart(
    alt.Chart(df).mark_area(color='brown').encode(
        x=alt.X('date:T', title='Hour'),
        y=alt.Y('interaction_count:Q', title='interaction_count'),
        tooltip=[alt.Tooltip('hour:T', title='Hour'), alt.Tooltip('interaction_count:Q', title='interaction_count')],
    ).properties(
        width=800,
        height=300,
        title='Myshell AIpp interaction count'
    ), use_container_width=True
    )
        
        st.markdown("##")
        st.altair_chart(
    alt.Chart(df_1).mark_area(color='blue').encode(
        x=alt.X('date:T', title='Hour'),
        y=alt.Y('inflow_bnb:Q', title='inflow_bnb'),
        tooltip=[alt.Tooltip('hour:T', title='Hour'), alt.Tooltip('inflow_bnb:Q', title='inflow_bnb')],
    ).properties(
        width=800,
        height=300,
        title='Myshell AIpp Inflow'
    ), use_container_width=True
    )
    with b:
        st.altair_chart(
    alt.Chart(df_1).mark_line(color='yellow').encode(
        x=alt.X('date:T', title='Hour'),
        y=alt.Y('daily_volume_bnb:Q', title='daily_volume_bnb'),
        tooltip=[alt.Tooltip('hour:T', title='Hour'), alt.Tooltip('daily_volume_bnb:Q', title='daily_volume_bnb')],
    ).properties(
        width=800,
        height=300,
        title='Myshell AIpp volume'
    ), use_container_width=True
    )
        
        st.markdown("##")
        st.altair_chart(
    alt.Chart(df_1).mark_line(color='red').encode(
        x=alt.X('date:T', title='Hour'),
        y=alt.Y('outflow_bnb:Q', title='outflow_bnb'),
        tooltip=[alt.Tooltip('hour:T', title='Hour'), alt.Tooltip('outflow_bnb:Q', title='outflow_bnb')],
    ).properties(
        width=800,
        height=300,
        title='Myshell AIpp Outflow'
    ), use_container_width=True
    )
        

    st.markdown("##")
    st.altair_chart(
    alt.Chart(df_1).mark_area (color='brown').encode(
        x=alt.X('date:T', title='Hour'),
        y=alt.Y('cumulative_tvl_bnb:Q', title='cumulative_tvl_bnb'),
        tooltip=[alt.Tooltip('hour:T', title='Hour'), alt.Tooltip('cumulative_tvl_bnb:Q', title='cumulative_tvl_bnb')],
    ).properties(
        width=800,
        height=300,
        title='Myshell AIpp Cumulative tvl bnb'
    ), use_container_width=True
    )

    generate_summary(df)

    st.markdown("##")
    st.subheader("Net BNB income in AIpp")
    st.dataframe( data("3933139"), width=1200)

    st.markdown("##")
    st.subheader("Cumulative Total Withdraw BNB from AIpp")
    st.dataframe( data("3932933"), width=1200)

    st.markdown("##")
    st.subheader("Cumulative Total Invest BNB")
    st.dataframe( data("3932993"), width=1200)



