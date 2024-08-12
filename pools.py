import streamlit as st
import pandas as pd
import requests
import altair as alt
import g4f

# Streamlit UI

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
    prompt = f"Here opbnb Dex data\n{csv_data_str}\ngive some short summary insights about the data in 6 sentences and  inverstments ideas in points"
    st.write(chat_bot(prompt))




def pools():
    st.title("OPBNB Pools Data Viewer")

    # User inputs for API parameters
    page = st.number_input("Page", min_value=1, value=1)
    sort = st.selectbox("Sort by", ["-24h_volume", "-pool_creation_date","-24h_transactions","-1h_trend_score","-6h_trend_score","-24h_price_percent_change"])

    # DEX selection as radio button
    dex = st.radio("Select DEX", ["All","allinxswap-opbnb","binaryswap","cubiswap","pancakeswap-v3-opbnb","thena-opbnb","pancakeswap-v2-opbnb","pixelswap-opbnb","luigiswap","fourdex"], horizontal=True)

    if dex == 'All':
        # API request
        url = f"https://app.geckoterminal.com/api/p1/opbnb/pools?page={page}&include_network_metrics=true&sort={sort}&networks=opbnb"
    else:
        url = f"https://app.geckoterminal.com/api/p1/opbnb/pools?page={page}&include_network_metrics=true&sort={sort}&networks=opbnb&?dex={dex}&dexes={dex}"

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
    response = requests.get(url,headers=headers)
    data = response.json()

    # Extract relevant data
    pools = data.get('data', [])
    formatted_data = []

    for pool in pools:
        attributes = pool['attributes']
        formatted_data.append({
            "Pool Name": attributes["name"],
            "Address": attributes["address"],
            "24h Volume (USD)": attributes["from_volume_in_usd"],
            "Price Change (24h)": attributes["price_percent_change"],
            "Swap Count (24h)": attributes["swap_count_24h"],
            "Price (USD)": attributes["price_in_usd"],
            "Reserve (USD)": attributes["reserve_in_usd"],
            "Created At": attributes["pool_created_at"]
        })

    # Display data in DataFrame
    df = pd.DataFrame(formatted_data)

    st.write("### Pool Data")
    st.dataframe(df)

    st.markdown("##")

    # Convert to DataFrame
    df = pd.DataFrame(formatted_data)

    # Create columns
    col1, col2 = st.columns(2)

    # Pie chart for Pool Name / 24h Volume
    with col1:
        st.write("### Pool Name / 24h Volume (USD)")
        pie_chart_24h_volume = alt.Chart(df).mark_arc().encode(
            theta=alt.Theta(field="24h Volume (USD)", type="quantitative"),
            color=alt.Color(field="Pool Name", type="nominal"),
            tooltip=["Pool Name", "24h Volume (USD)"]
        ).properties(width=350, height=350)
        st.altair_chart(pie_chart_24h_volume, use_container_width=True)

    # Pie chart for Pool Name / Reserve (USD)
    with col2:
        st.write("### Pool Name / Reserve (USD)")
        pie_chart_reserve = alt.Chart(df).mark_arc().encode(
            theta=alt.Theta(field="Reserve (USD)", type="quantitative"),
            color=alt.Color(field="Pool Name", type="nominal"),
            tooltip=["Pool Name", "Reserve (USD)"]
        ).properties(width=350, height=350)
        st.altair_chart(pie_chart_reserve, use_container_width=True)

    st.markdown("##")
    generate_summary(df)
