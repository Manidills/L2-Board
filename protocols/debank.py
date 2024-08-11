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
    prompt = f"Here opbnb L2 debank protocol data\n{csv_data_str}\ngive some short summary insights about the data in 6 sentences and there connections in points"
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
    
def debank():
    prompt = f"Explain about  debank  protocol  in 3 points"
    st.write(chat_bot(prompt))
    st.markdown("##")
    a,b = st.columns([2,2])
    df = data("2772498")
    df_1 = data("2770393")
    df_2 = data("2770386")
    # df['date'] = pd.to_datetime(df.date, errors='coerce')
    with a:
        st.altair_chart(
    alt.Chart(df).mark_bar(color='brown').encode(
        x=alt.X('Type', title='Chain'),
        y=alt.Y('Users:Q', title='Users'),
        tooltip=[alt.Tooltip('chain:T', title='chain'), alt.Tooltip('Users:Q', title='Users')],
    ).properties(
        width=800,
        height=300,
        title='DeBank - Registered Users'
    ), use_container_width=True
    )
        
        st.altair_chart(
        alt.Chart(df_1).mark_circle(color='red').encode(
            x=alt.X('Type', title='Chain'),
            y=alt.Y('Transactions:Q', title='Transactions'),
            tooltip=[alt.Tooltip('chain:T', title='chain'), alt.Tooltip('Transactions:Q', title='Transactions')],
        ).properties(
            width=800,
            height=300,
            title='DeBank - Deposits Transactions'
        ), use_container_width=True
        )

        st.altair_chart(
        alt.Chart(df_2).mark_bar(color='blue').encode(
            x=alt.X('Type', title='Chain'),
            y=alt.Y('Transactions:Q', title='Transactions'),
            tooltip=[alt.Tooltip('chain:T', title='chain'), alt.Tooltip('Transactions:Q', title='Transactions')],
        ).properties(
            width=800,
            height=300,
            title='DeBank - Withdrawal Transactions'
        ), use_container_width=True
        )
    
    with b:
        st.altair_chart(
    alt.Chart(df).mark_bar(color='pink').encode(
        x=alt.X('Type', title='Chain'),
        y=alt.Y('L2 accounts:Q', title='L2 accounts'),
        tooltip=[alt.Tooltip('chain:T', title='chain'), alt.Tooltip('L2 accounts:Q', title='L2 accounts')],
    ).properties(
        width=800,
        height=300,
        title='DeBank - Active accounts'
    ), use_container_width=True
    )
         
        st.altair_chart(
        alt.Chart(df_1).mark_circle(color='yellow').encode(
            x=alt.X('Type', title='Chain'),
            y=alt.Y('TotalValue:Q', title='TotalValue'),
            tooltip=[alt.Tooltip('chain:T', title='chain'), alt.Tooltip('TotalValue:Q', title='TotalValue')],
        ).properties(
            width=800,
            height=300,
            title='DeBank - Deposits TotalValue'
        ), use_container_width=True
        )

        st.altair_chart(
        alt.Chart(df_2).mark_bar(color='orange').encode(
            x=alt.X('Type', title='Chain'),
            y=alt.Y('TotalValue:Q', title='TotalValue'),
            tooltip=[alt.Tooltip('chain:T', title='chain'), alt.Tooltip('TotalValue:Q', title='TotalValue')],
        ).properties(
            width=800,
            height=300,
            title='DeBank - Withdrawal TotalValue'
        ), use_container_width=True
        )

    generate_summary(df)
    # response = get_response(prompt)
    st.write(chat_bot(prompt))

    csv_data_str = df_1.to_string(index=False)
    # Format the string to be used as input for ChatGPT
    prompt = f"Here is debank protocol Layer 2 data across blockchain:\n{csv_data_str}\ngive some short summary insights about the data in 3 sentances"

    # response = get_response(prompt)
    st.write(chat_bot(prompt))

    csv_data_str = df_2.to_string(index=False)
    # Format the string to be used as input for ChatGPT
    prompt = f"Here is debank protocol Layer 2 data across blockchain:\n{csv_data_str}\ngive some short summary insights about the data in 3 sentances"

    # response = get_response(prompt)
    st.write(chat_bot(prompt))




    st.markdown("##")
    df = data("2786350")

    df['Day'] = pd.to_datetime(df['Day'])


    st.altair_chart(
        alt.Chart(df).mark_line().encode(
            x=alt.X('Day:T', title='Time'),
            y=alt.Y('l2Account2:Q', stack=None, title='l2Account2'),
            color=alt.Color('Type:N', legend=alt.Legend(title='Type')),
            tooltip=['time:T', 'symbol:N', 'tvl:Q']
        ).properties(
            width=800,
            height=400,
            title='eBank - Statistic Accounts per chain/day'
        ),
        use_container_width=True
    )


    st.markdown("##")
    df = data("2772418")

    df['Day'] = pd.to_datetime(df['Day'])


    st.altair_chart(
        alt.Chart(df).mark_line().encode(
            x=alt.X('Day:T', title='Time'),
            y=alt.Y('Transactions:Q', stack=None, title='Transactions'),
            color=alt.Color('Type:N', legend=alt.Legend(title='Type')),
            tooltip=['time:T', 'symbol:N', 'tvl:Q']
        ).properties(
            width=800,
            height=400,
            title='eBank - Deposit Transactions'
        ),
        use_container_width=True
    )
    



    st.markdown("##")
    df = data("2772533")

    df['Day'] = pd.to_datetime(df['Day'])


    st.altair_chart(
        alt.Chart(df).mark_line().encode(
            x=alt.X('Day:T', title='Time'),
            y=alt.Y('Transactions:Q', stack=None, title='Transactions'),
            color=alt.Color('Type:N', legend=alt.Legend(title='Type')),
            tooltip=['time:T', 'symbol:N', 'tvl:Q']
        ).properties(
            width=800,
            height=400,
            title='eBank - Withdrawl Transactions'
        ),
        use_container_width=True
    )

    generate_summary(df)

    



    
        


