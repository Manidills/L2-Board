from io import StringIO
import requests
import streamlit as st
import pandas as pd
import datetime
import altair as alt
import time
import os
import g4f

def get_response(prompt):
    url = f"https://api.kastg.xyz/api/ai/chatgptV4?prompt={prompt}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            json_response = response.json()
            if json_response.get("status") == "true" and json_response.get("result"):
                return json_response["result"][0]["response"]
            else:
                return "Error in API response"
        else:
            return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"
    

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
    prompt = f"Here opbnb L2 chain data\n{csv_data_str}\ngive some short summary insights about the data in 6 sentences and there connections in points"
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
    

def home():

    a,b = st.columns([2,2])
    with a:
        st.metric("Total Value Locked", "$27,475,795",'0.9')
    with b:
        st.metric("24h Trading Volume", "$137,840",'-3.9')
    st.markdown("##")
    st.header("Deposits")
    st.markdown("##")
    a,b = st.columns([2,2])
    df = data("2873875")
    st.dataframe(df, width=1400)
    df['hour'] = pd.to_datetime(df.hour, errors='coerce')
    with a:
        st.altair_chart(
    alt.Chart(df).mark_bar().encode(
        x=alt.X('hour:T', title='Hour'),
        y=alt.Y('Txns:Q', title='Txns'),
        tooltip=[alt.Tooltip('hour:T', title='Hour'), alt.Tooltip('Cumulative_USD:Q', title='Cumulative USD Amount')],
    ).properties(
        width=800,
        height=300,
        title='opBNB Deposit Txns'
    ), use_container_width=True
    )
        st.markdown("##")

        st.altair_chart(
    alt.Chart(df).mark_bar(color='yellow').encode(
        x=alt.X('hour:T', title='Hour'),
        y=alt.Y('Amount_BNB:Q', title='Amount_BNB'),
        tooltip=[alt.Tooltip('hour:T', title='Hour'), alt.Tooltip('Amount BNB:Q', title='Amount BNB')],
    ).properties(
        width=800,
        height=300,
        title='opBNB Deposit Amount BNB'
    ), use_container_width=True
    )
        
        st.markdown("##")

        st.altair_chart(
    alt.Chart(df).mark_bar(color='brown').encode(
        x=alt.X('hour:T', title='Hour'),
        y=alt.Y('Amount_USD:Q', title='Amount_BNB'),
        tooltip=[alt.Tooltip('hour:T', title='Hour'), alt.Tooltip('Amount_USD:Q', title='Amount_USD')],
    ).properties(
        width=800,
        height=300,
        title='opBNB Deposit Amount USD'
    ), use_container_width=True
    )

    with b:
        st.altair_chart(
    alt.Chart(df).mark_bar(color='red',opacity=0.1).encode(
        x=alt.X('hour:T', title='Hour'),
        y=alt.Y('Cumulative_Tx:Q', title='Cumulative TXS'),
        tooltip=[alt.Tooltip('hour:T', title='Hour'), alt.Tooltip('Cumulative_USD:Q', title='Cumulative USD Amount')],
    ).properties(
        width=800,
        height=300,
        title='opBNB Deposit Cumulative TXS'
    ), use_container_width=True
    )
          
        st.markdown("##")
        st.altair_chart(
    alt.Chart(df).mark_bar(color='blue',opacity=0.1).encode(
        x=alt.X('hour:T', title='Hour'),
        y=alt.Y('Cumulative_BNB:Q', title='Cumulative_BNB'),
        tooltip=[alt.Tooltip('hour:T', title='Hour'), alt.Tooltip('Cumulative_BNB:Q', title='Cumulative_BNB')],
    ).properties(
        width=800,
        height=300,
        title='opBNB Deposit Cumulative BNB'
    ), use_container_width=True
    )
        
        st.markdown("##")
        st.altair_chart(
    alt.Chart(df).mark_bar(color='orange',opacity=0.1).encode(
        x=alt.X('hour:T', title='Hour'),
        y=alt.Y('Cumulative_USD:Q', title='Cumulative_USD'),
        tooltip=[alt.Tooltip('hour:T', title='Hour'), alt.Tooltip('Cumulative_USD:Q', title='Cumulative_USD')],
    ).properties(
        width=800,
        height=300,
        title='opBNB Deposit Cumulative USD'
    ), use_container_width=True
    )
        
    generate_summary(df)
        
    st.markdown("####")
    st.header("WITHDRAWAL")
    st.markdown("##")
    a,b = st.columns([2,2])
    df = data("2979178")
    st.dataframe(df, width=1400)
    df['hour'] = pd.to_datetime(df.hour, errors='coerce')
    
    with a:
        st.altair_chart(
    alt.Chart(df).mark_bar().encode(
        x=alt.X('hour:T', title='Hour'),
        y=alt.Y('Txns:Q', title='Txns'),
        tooltip=[alt.Tooltip('hour:T', title='Hour'), alt.Tooltip('Cumulative_USD:Q', title='Cumulative USD Amount')],
    ).properties(
        width=800,
        height=300,
        title='opBNB Withdrawal Txns'
    ), use_container_width=True
    )
        st.markdown("##")

        st.altair_chart(
    alt.Chart(df).mark_bar(color='yellow').encode(
        x=alt.X('hour:T', title='Hour'),
        y=alt.Y('Amount_BNB:Q', title='Amount_BNB'),
        tooltip=[alt.Tooltip('hour:T', title='Hour'), alt.Tooltip('Amount BNB:Q', title='Amount BNB')],
    ).properties(
        width=800,
        height=300,
        title='opBNB Withdrawal Amount BNB'
    ), use_container_width=True
    )
        
        st.markdown("##")

        st.altair_chart(
    alt.Chart(df).mark_bar(color='brown').encode(
        x=alt.X('hour:T', title='Hour'),
        y=alt.Y('Amount_USD:Q', title='Amount_BNB'),
        tooltip=[alt.Tooltip('hour:T', title='Hour'), alt.Tooltip('Amount_USD:Q', title='Amount_USD')],
    ).properties(
        width=800,
        height=300,
        title='opBNB Withdrawal Amount USD'
    ), use_container_width=True
    )

    with b:
        st.altair_chart(
    alt.Chart(df).mark_area(color='red',opacity=0.4).encode(
        x=alt.X('hour:T', title='Hour'),
        y=alt.Y('Cumulative_Tx:Q', title='Cumulative USD Amount'),
        tooltip=[alt.Tooltip('hour:T', title='Hour'), alt.Tooltip('Cumulative_USD:Q', title='Cumulative USD Amount')],
    ).properties(
        width=800,
        height=300,
        title='opBNB Withdrawal Cumulative USD Amount Over Time'
    ), use_container_width=True
    )
          
        st.markdown("##")
        st.altair_chart(
    alt.Chart(df).mark_area(color='blue',opacity=0.4).encode(
        x=alt.X('hour:T', title='Hour'),
        y=alt.Y('Cumulative_BNB:Q', title='Cumulative_BNB'),
        tooltip=[alt.Tooltip('hour:T', title='Hour'), alt.Tooltip('Cumulative_BNB:Q', title='Cumulative_BNB')],
    ).properties(
        width=800,
        height=300,
        title='opBNB Withdrawal Cumulative BNB'
    ), use_container_width=True
    )
        
        st.markdown("##")
        st.altair_chart(
    alt.Chart(df).mark_area(color='orange',opacity=0.4).encode(
        x=alt.X('hour:T', title='Hour'),
        y=alt.Y('Cumulative_USD:Q', title='Cumulative_USD'),
        tooltip=[alt.Tooltip('hour:T', title='Hour'), alt.Tooltip('Cumulative_USD:Q', title='Cumulative_USD')],
    ).properties(
        width=800,
        height=300,
        title='opBNB Withdrawal Cumulative USD'
    ), use_container_width=True
    )
        
    generate_summary(df)


    st.markdown("##")
    df = data("2872284")

    df['time'] = pd.to_datetime(df['time'])

    # Chart title and description
    st.markdown("## Total Value Locked (TVL) Over Time")

    # Creating the multi-area graph (stacked area chart)
    st.altair_chart(
        alt.Chart(df).mark_line().encode(
            x=alt.X('time:T', title='Time'),
            y=alt.Y('tvl:Q', stack=None, title='TVL'),
            color=alt.Color('symbol:N', legend=alt.Legend(title='Symbol')),
            tooltip=['time:T', 'symbol:N', 'tvl:Q']
        ).properties(
            width=800,
            height=400,
            title='Total Value Locked (TVL) Over Time'
        ),
        use_container_width=True
    )

    generate_summary(df.tail(500))