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
    


def apx():
    st.markdown("##")
    df = data("3271669")

    df['day'] = pd.to_datetime(df['day'])


    st.altair_chart(
        alt.Chart(df).mark_line().encode(
            x=alt.X('day:T', title='Time'),
            y=alt.Y('TotalVol:Q', stack=None, title='TotalVol'),
            color=alt.Color('symbol:N', legend=alt.Legend(title='symbol')),
            tooltip=['time:T', 'symbol:N', 'tvl:Q']
        ).properties(
            width=800,
            height=400,
            title='Opbnb - APX v2 Trading Trend'
        ),
        use_container_width=True
    )

    csv_data_str = df.to_string(index=False)
    # Format the string to be used as input for ChatGPT
    prompt = f"Here is APX opbnb data:\n{csv_data_str}\ngive some short summary insights about the data insights in 4 sentences"

    # response = get_response(prompt)
    st.write(chat_bot(prompt))
    st.markdown("##")
    st.subheader("Opbnb - APX v2 Income")
    st.markdown("##")
    a,b = st.columns([2,2])
    df = data("3271702")
    df['day'] = pd.to_datetime(df.day, errors='coerce')
    with a:
        st.altair_chart(
    alt.Chart(df).mark_line(color='brown').encode(
        x=alt.X('day:T', title='Time'),
        y=alt.Y('daily_income:Q', title='daily_income')
    ).properties(
        width=800,
        height=300
    ), use_container_width=True
    )
        
        st.altair_chart(
        alt.Chart(df).mark_line(color='red').encode(
            x=alt.X('day:T', title='Time'),
            y=alt.Y('Accumulated_income:Q', title='Accumulated_income')
        ).properties(
            width=800,
            height=300
        ), use_container_width=True
        )

        st.altair_chart(
        alt.Chart(df).mark_line(color='blue').encode(
            x=alt.X('day:T', title='Time'),
            y=alt.Y('total_trade_fee:Q', title='total_trade_fee')
        ).properties(
            width=800,
            height=300
        ), use_container_width=True
        )
    
    with b:
        st.altair_chart(
    alt.Chart(df).mark_line(color='brown').encode(
        x=alt.X('day:T', title='Time'),
        y=alt.Y('total_funding_fee:Q', title='total_funding_fee')
    ).properties(
        width=800,
        height=300
    ), use_container_width=True
    )
        
        st.altair_chart(
        alt.Chart(df).mark_line(color='red').encode(
            x=alt.X('day:T', title='Time'),
            y=alt.Y('liq_margin:Q', title='liq_margin')
        ).properties(
            width=800,
            height=300
        ), use_container_width=True
        )

        st.altair_chart(
        alt.Chart(df).mark_line(color='blue').encode(
            x=alt.X('day:T', title='Time'),
            y=alt.Y('accumlated_trade_fee:Q', title='accumlated_trade_fee')
        ).properties(
            width=800,
            height=300
        ), use_container_width=True
        )


    st.markdown("##")
    st.subheader("V- Core Report -Opbnb")
    st.markdown("##")
    a,b = st.columns([2,2])
    df = data("3266062")
    df['day_day'] = pd.to_datetime(df.day_day, errors='coerce')
    with a:
        st.altair_chart(
    alt.Chart(df).mark_bar(color='orange').encode(
        x=alt.X('day_day:T', title='Time'),
        y=alt.Y('opbnb_daily_total_trade_volume:Q', title='opbnb_daily_total_trade_volume')
    ).properties(
        width=800,
        height=300
    ), use_container_width=True
    )
        
        st.altair_chart(
        alt.Chart(df).mark_bar(color='red').encode(
            x=alt.X('day_day:T', title='Time'),
            y=alt.Y('opbnb_daily_trades:Q', title='opbnb_daily_trades')
        ).properties(
            width=800,
            height=300
        ), use_container_width=True
        )

        st.altair_chart(
        alt.Chart(df).mark_bar(color='blue').encode(
            x=alt.X('day_day:T', title='Time'),
            y=alt.Y('opbnb_daily_trades:Q', title='opbnb_daily_trades')
        ).properties(
            width=800,
            height=300
        ), use_container_width=True
        )
    
    with b:
        st.altair_chart(
    alt.Chart(df).mark_bar(color='green').encode(
        x=alt.X('day_day:T', title='Time'),
        y=alt.Y('opbnb_daily_total_funding_fee:Q', title='opbnb_daily_total_funding_fee')
    ).properties(
        width=800,
        height=300
    ), use_container_width=True
    )
        
        st.altair_chart(
        alt.Chart(df).mark_bar(color='red').encode(
            x=alt.X('day_day:T', title='Time'),
            y=alt.Y('opbnb_daily_liq_trade_volume:Q', title='opbnb_daily_liq_trade_volume')
        ).properties(
            width=800,
            height=300
        ), use_container_width=True
        )

        st.altair_chart(
        alt.Chart(df).mark_bar(color='blue').encode(
            x=alt.X('day_day:T', title='Time'),
            y=alt.Y('opbnb_cum_user_realized_pnl:Q', title='opbnb_cum_user_realized_pnl')
        ).properties(
            width=800,
            height=300
        ), use_container_width=True
        )


    st.markdown("##")
    st.subheader("Opbnb - V2 Liquidation Status")
    st.markdown("##")
    st.dataframe( data("3271777"), width=1200)

    