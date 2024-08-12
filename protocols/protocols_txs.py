import streamlit as st
import requests
import pandas as pd
import altair as alt
from datetime import datetime
import g4f

# Function to fetch data from the API
def fetch_data(page, sort_granularity):
    url = f"https://dappbay.bnbchain.org/api/v1/ranking/dapp-list-v2?page={page}&pageSize=10&sortRankingKey=users&sortGranularity={sort_granularity}&sortType=desc&category=&chainInfoId=3&keyword=&is_new=0"
    response = requests.get(url)
    data = response.json()
    return data

# Function to convert timestamp to readable date
def timestamp_to_date(timestamp):
    return datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d')

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
    prompt = f"Here opbnb protocols data\n{csv_data_str}\ngive some short summary insights about the data in 6 sentences and which is good investment for future in points"
    st.write(chat_bot(prompt))


def pro_txt():

    # Streamlit app layout
    st.title("List of Protocols")

    # Select boxes for user input
    page = st.selectbox("Select Page", options=range(1, 21), index=0)  # Page range from 1 to 20
    sort_granularity = st.selectbox("Select Granularity", options=['daily', 'weekly', 'monthly'], index=2)

    # Fetch data based on user inputs
    data = fetch_data(page, sort_granularity)

    pools = data.get('list', [])
    formatted_data = []
    history = []
    txns = []

    st.markdown("##")

    for pool in pools:
        attributes = pool['dapp']
        formatted_data.append(attributes)

        if  sort_granularity == 'monthly' or sort_granularity == 'weekly':
            history.append(pool['history']['users'])
            txns.append(pool['history']['txns'])

    formatted_data = pd.DataFrame(formatted_data)

    dapp_names = formatted_data['name'].to_list()

    st.data_editor(formatted_data)
    def timestamp_to_date(timestamp):
        return datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d')
    
    a,b = st.columns([2,2])

    with a:

        # Iterate through each dataset in the list of lists
        for i, dataset in enumerate(history):
            # Convert data to DataFrame
            df = pd.DataFrame(dataset)
            df['timestamp'] = df['timestamp'].apply(timestamp_to_date)
            df.rename(columns={'timestamp': 'Date', 'value': 'Value'}, inplace=True)
            
            # Plot the dataset
            st.write(f"### {dapp_names[i]} Users Over Time")
            chart = alt.Chart(df).mark_line(color='burlywood').encode(
                x='Date:T',
                y='Value:Q',
                tooltip=['Date:T', 'Value:Q']
            ).interactive()
            
            st.altair_chart(chart, use_container_width=True)

    with b:

        # Iterate through each dataset in the list of lists
        for i, dataset in enumerate(txns):
            # Convert data to DataFrame
            df = pd.DataFrame(dataset)
            df['timestamp'] = df['timestamp'].apply(timestamp_to_date)
            df.rename(columns={'timestamp': 'Date', 'value': 'Value'}, inplace=True)
            
            # Plot the dataset
            st.write(f"### {dapp_names[i]} txns Over Time")
            chart = alt.Chart(df).mark_line(color='aquamarine').encode(
                x='Date:T',
                y='Value:Q',
                tooltip=['Date:T', 'Value:Q']
            ).interactive()
            
            st.altair_chart(chart, use_container_width=True)


        #st.dataframe(pools)

    generate_summary(formatted_data)


                    
                    