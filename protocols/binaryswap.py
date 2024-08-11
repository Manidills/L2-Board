from io import StringIO
import requests
import streamlit as st
import pandas as pd
import datetime
import altair as alt
import time
import os
import g4f

def hour(timerange):
    url = f'https://www.coingecko.com/exchanges/1270/usd/{timerange}.json'
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data
    

def binaryswap():
    # normalized_volumes
    st.markdown("##")

    a,b = st.columns([2,2])

    with a :
        st.metric("Reported Trading Volume", "$178.02")

    with b:
        st.metric("Average Bid-Ask Spread", "-")    
    
    st.markdown("##")


    data = hour("24_hours")
# Extract and convert data to DataFrame
    df = pd.DataFrame(data['volumes'], columns=['timestamp', 'volume'])

    # Convert timestamp to datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    st.altair_chart(
        alt.Chart(df).mark_area(color='green',opacity=0.4).encode(
            x=alt.X('timestamp:T', title='Time'),
            y=alt.Y('volume:Q', stack=None, title='TotalVol'),
        ).properties(
            width=800,
            height=400,
            title='Exchange Trade Volume 24H'
        ),
        use_container_width=True
    )

    data = hour("7_days")
# Extract and convert data to DataFrame
    df = pd.DataFrame(data['volumes'], columns=['timestamp', 'volume'])

    # Convert timestamp to datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    st.altair_chart(
        alt.Chart(df).mark_area(color='red',opacity=0.4).encode(
            x=alt.X('timestamp:T', title='Time'),
            y=alt.Y('volume:Q', stack=None, title='TotalVol'),
        ).properties(
            width=800,
            height=400,
            title='Exchange Trade 7d'
        ),
        use_container_width=True
    )

    data = hour("14_days")
# Extract and convert data to DataFrame
    df = pd.DataFrame(data['volumes'], columns=['timestamp', 'volume'])

    # Convert timestamp to datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    st.altair_chart(
        alt.Chart(df).mark_area(color='blue',opacity=0.4).encode(
            x=alt.X('timestamp:T', title='Time'),
            y=alt.Y('volume:Q', stack=None, title='TotalVol'),
        ).properties(
            width=800,
            height=400,
            title='Exchange Trade 14d'
        ),
        use_container_width=True
    )

    data = hour("30_days")
# Extract and convert data to DataFrame
    df = pd.DataFrame(data['volumes'], columns=['timestamp', 'volume'])

    # Convert timestamp to datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    st.altair_chart(
        alt.Chart(df).mark_area(color='pink',opacity=0.4).encode(
            x=alt.X('timestamp:T', title='Time'),
            y=alt.Y('volume:Q', stack=None, title='TotalVol'),
        ).properties(
            width=800,
            height=400,
            title='Exchange Trade 30d'
        ),
        use_container_width=True
    )

    data = hour("3_months")
# Extract and convert data to DataFrame
    df = pd.DataFrame(data['volumes'], columns=['timestamp', 'volume'])

    # Convert timestamp to datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    st.altair_chart(
        alt.Chart(df).mark_area(color='grey',opacity=0.4).encode(
            x=alt.X('timestamp:T', title='Time'),
            y=alt.Y('volume:Q', stack=None, title='TotalVol'),
        ).properties(
            width=800,
            height=400,
            title='Exchange Trade 3 Months'
        ),
        use_container_width=True
    )


    st.markdown("##")
    data = hour("1_year")
   # Extract and convert data to DataFrame
    df = pd.DataFrame(data['volumes'], columns=['timestamp', 'volume'])

    # Convert timestamp to datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    st.altair_chart(
        alt.Chart(df).mark_area(color='orange',opacity=0.4).encode(
            x=alt.X('timestamp:T', title='Time'),
            y=alt.Y('volume:Q', stack=None, title='TotalVol'),
        ).properties(
            width=800,
            height=400,
            title='Exchange Trade Volume 1 year'
        ),
        use_container_width=True
    )


    