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
    prompt = f"Here opbnb L2 chain pancake perpetual data\n{csv_data_str}\ngive some short summary insights about the data in 6 sentences and there connections in points"
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
    

def pancake():
    prompt = f"Explain about  pancake perpetual protocol  3 points"
    st.write(chat_bot(prompt))
    st.markdown("##")
    st.subheader("PCS Perp V2 Monthly")
    st.markdown("##")
    a,b = st.columns([2,2])
    df = data("3294113")
    df['month'] = pd.to_datetime(df.month, errors='coerce')
    with a:
        st.altair_chart(
    alt.Chart(df).mark_line(color='orange').encode(
        x=alt.X('month:T', title='Time'),
        y=alt.Y('volume:Q', title='volume')
    ).properties(
        width=800,
        height=300
    ), use_container_width=True
    )
        
        st.altair_chart(
        alt.Chart(df).mark_line(color='red').encode(
            x=alt.X('month:T', title='Time'),
            y=alt.Y('trader:Q', title='trader')
        ).properties(
            width=800,
            height=300
        ), use_container_width=True
        )

    
    with b:
        st.altair_chart(
    alt.Chart(df).mark_area(color='green', opacity=0.3).encode(
        x=alt.X('month:T', title='Time'),
        y=alt.Y('fee_usd:Q', title='fee_usd')
    ).properties(
        width=800,
        height=300
    ), use_container_width=True
    )
        
        st.altair_chart(
        alt.Chart(df).mark_area(color='red', opacity=0.3).encode(
            x=alt.X('month:T', title='Time'),
            y=alt.Y('fee_rebate:Q', title='fee_rebate')
        ).properties(
            width=800,
            height=300
        ), use_container_width=True
        )



    st.markdown("##")
    st.subheader("PCS Perp V2 Daily")
    st.markdown("##")
    a,b = st.columns([2,2])
    df = data("3294105")
    df['dt'] = pd.to_datetime(df.dt, errors='coerce')
    with a:
        st.altair_chart(
    alt.Chart(df).mark_bar(color='orange').encode(
        x=alt.X('dt:T', title='Time'),
        y=alt.Y('volume:Q', title='volume')
    ).properties(
        width=800,
        height=300
    ), use_container_width=True
    )
        
        st.altair_chart(
        alt.Chart(df).mark_bar(color='brown').encode(
            x=alt.X('dt:T', title='Time'),
            y=alt.Y('trader:Q', title='trader')
        ).properties(
            width=800,
            height=300
        ), use_container_width=True
        )

    
    with b:
        st.altair_chart(
    alt.Chart(df).mark_bar(color='green').encode(
        x=alt.X('dt:T', title='Time'),
        y=alt.Y('fee_usd:Q', title='fee_usd')
    ).properties(
        width=800,
        height=300
    ), use_container_width=True
    )
        
        st.altair_chart(
        alt.Chart(df).mark_bar(color='pink').encode(
            x=alt.X('dt:T', title='Time'),
            y=alt.Y('fee_rebate:Q', title='fee_rebate')
        ).properties(
            width=800,
            height=300
        ), use_container_width=True
        )


    
    st.markdown("##")
    st.dataframe( df, width=1200)

    generate_summary(df)
