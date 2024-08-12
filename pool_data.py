import streamlit as st
import pandas as pd
import requests
import altair as alt
import g4f


def fetch_ohlcv_data(address, day):
    url = f"https://api.geckoterminal.com/api/v2/networks/opbnb/pools/{address}/ohlcv/{day}"
    response = requests.get(url)
    return response.json()

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
    prompt = f"Here opbnb Dex Pool data\n{csv_data_str}\ngive some short summary insights about the data in 6 sentences and  inverstments ideas in points"
    st.write(chat_bot(prompt))




def pool_data():

    # Streamlit UI for input
    st.title("OPBNB Pool Data Viewer")

    # Address input
    pool_address = st.text_input("Enter Pool Address", placeholder="e.g., 0x8a322bf307aa673424c445f576f2992f381521fb")
    day = st.selectbox("Select time range", ["day", "hour", "minute"])

    if pool_address:
        # API request
        url = f"https://api.geckoterminal.com/api/v2/networks/opbnb/pools/{pool_address}"
        response = requests.get(url)
        data = response.json()

        # Extract relevant data
        attributes = data['data']['attributes']

        # Create DataFrame for general pool data
        df_pool_data = pd.DataFrame({
            "Metric": ["Name","Base Token Price (USD)", "Quote Token Price (USD)", "Base Token Price (Native)", 
                    "Quote Token Price (Native)", "Base Token Price (Quote)", "Quote Token Price (Base)", 
                    "FDV (USD)", "Reserve (USD)", "24h Volume (USD)"],
            "Value": [attributes['name'],attributes["base_token_price_usd"], attributes["quote_token_price_usd"], 
                    attributes["base_token_price_native_currency"], attributes["quote_token_price_native_currency"], 
                    attributes["base_token_price_quote_token"], attributes["quote_token_price_base_token"], 
                    attributes["fdv_usd"], attributes["reserve_in_usd"], attributes["volume_usd"]["h24"]]
        })

        # Create DataFrame for transactions data
        df_transactions = pd.DataFrame({
            "Timeframe": ["5 Minutes", "15 Minutes", "30 Minutes", "1 Hour", "24 Hours"],
            "Buys": [attributes["transactions"]["m5"]["buys"], attributes["transactions"]["m15"]["buys"],
                    attributes["transactions"]["m30"]["buys"], attributes["transactions"]["h1"]["buys"],
                    attributes["transactions"]["h24"]["buys"]],
            "Sells": [attributes["transactions"]["m5"]["sells"], attributes["transactions"]["m15"]["sells"],
                    attributes["transactions"]["m30"]["sells"], attributes["transactions"]["h1"]["sells"],
                    attributes["transactions"]["h24"]["sells"]],
            "Buyers": [attributes["transactions"]["m5"]["buyers"], attributes["transactions"]["m15"]["buyers"],
                    attributes["transactions"]["m30"]["buyers"], attributes["transactions"]["h1"]["buyers"],
                    attributes["transactions"]["h24"]["buyers"]],
            "Sellers": [attributes["transactions"]["m5"]["sellers"], attributes["transactions"]["m15"]["sellers"],
                        attributes["transactions"]["m30"]["sellers"], attributes["transactions"]["h1"]["sellers"],
                        attributes["transactions"]["h24"]["sellers"]]
        })
        st.markdown("##")
        a,b = st.columns([2,2])
        # Display DataFrames

        with a:
            st.write("### Pool Data")
            st.dataframe(df_pool_data)

        with b:

            st.write("### Transactions Data")
            st.dataframe(df_transactions)

        # Create columns for charts
        col1, col2 = st.columns(2)

        # Bar chart for price changes
        with col1:
            st.write("### Price Change Percentage")
            price_change_df = pd.DataFrame({
                "Timeframe": ["5 Minutes", "1 Hour", "6 Hours", "24 Hours"],
                "Price Change (%)": [attributes["price_change_percentage"]["m5"], attributes["price_change_percentage"]["h1"],
                                    attributes["price_change_percentage"]["h6"], attributes["price_change_percentage"]["h24"]]
            })
            bar_chart = alt.Chart(price_change_df).mark_bar().encode(
                x='Timeframe',
                y='Price Change (%)',
                color='Timeframe',
                tooltip=['Timeframe', 'Price Change (%)']
            ).properties(width=350, height=350)
            st.altair_chart(bar_chart, use_container_width=True)

        # Pie chart for buy/sell transactions
        with col2:
            st.write("### Transactions (24h)")
            transaction_pie_df = pd.DataFrame({
                "Type": ["Buys", "Sells"],
                "Count": [attributes["transactions"]["h24"]["buys"], attributes["transactions"]["h24"]["sells"]]
            })
            pie_chart = alt.Chart(transaction_pie_df).mark_arc().encode(
                theta=alt.Theta(field="Count", type="quantitative"),
                color=alt.Color(field="Type", type="nominal"),
                tooltip=['Type', 'Count']
            ).properties(width=350, height=350)
            st.altair_chart(pie_chart, use_container_width=True)

        generate_summary(df_pool_data)
        st.markdown("##")
        generate_summary(df_transactions)
        st.markdown("##")

        url = f"https://api.geckoterminal.com/api/v2/networks/opbnb/pools/{pool_address}/trades"
        response = requests.get(url)
        data = response.json()

        # Extract relevant data
        attributes = data['data']

        pools = data.get('data', [])
        formatted_data = []

        st.markdown("##")

        for pool in pools:
            attributes = pool['attributes']
            formatted_data.append(attributes)

        formatted_data = pd.DataFrame(formatted_data)

        st.data_editor(formatted_data)
        st.markdown("##")

        formatted_data['block_timestamp'] = pd.to_datetime(formatted_data.block_timestamp, errors='coerce')

        formatted_data['volume_in_usd'] = pd.to_numeric(formatted_data.volume_in_usd, errors='coerce')



        st.altair_chart(
        alt.Chart(formatted_data).mark_bar().encode(
            x=alt.X('block_timestamp:T', title='Time'),
            y=alt.Y('volume_in_usd:Q', stack=None, title='TVL')
        ).properties(
            width=800,
            height=400,
            title='Trades'
        ),
        use_container_width=True
    )
        st.markdown("##")

        ohlcv_data = fetch_ohlcv_data(pool_address, day)
        if ohlcv_data:
            # Extract and format OHLCV data
            ohlcv_list = ohlcv_data['data']['attributes']['ohlcv_list']
            ohlcv_df = pd.DataFrame(ohlcv_list, columns=["Timestamp", "Open", "High", "Low", "Close", "Volume"])
            ohlcv_df['Date'] = pd.to_datetime(ohlcv_df['Timestamp'], unit='s')
            ohlcv_df = ohlcv_df.set_index('Date')

            # Draw improved candlestick chart
            st.write("### OHLCV Data")
            st.dataframe(ohlcv_df, width=1200)
            st.markdown("##")

            # Base chart for wicks (high-low range)
            wick_chart = alt.Chart(ohlcv_df.reset_index()).mark_rule().encode(
                x='Date:T',
                y='Low:Q',
                y2='High:Q',
                color=alt.condition("datum.Open <= datum.Close", alt.value("green"), alt.value("red")),
                tooltip=["Date", "Open", "High", "Low", "Close", "Volume"]
            )

            # Rectangles for the candles (open-close range)
            candle_chart = alt.Chart(ohlcv_df.reset_index()).mark_bar(size=10).encode(
                x='Date:T',
                y='Open:Q',
                y2='Close:Q',
                color=alt.condition("datum.Open <= datum.Close", alt.value("green"), alt.value("red")),
                tooltip=["Date", "Open", "High", "Low", "Close", "Volume"]
            )

            combined_chart = alt.layer(wick_chart, candle_chart).interactive()

            st.altair_chart(combined_chart, use_container_width=True)

            generate_summary(ohlcv_df)