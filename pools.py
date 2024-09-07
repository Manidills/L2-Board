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
    st.title("OPBNB DEXs Data Viewer")

    # User inputs for API parameters
    page = st.number_input("Page", min_value=1, value=1)
    sort = st.selectbox("Sort by", ["h24_tx_count_desc", "h24_volume_usd_desc"])

    # DEX selection as radio button
    dex = st.radio("Select DEX", ["All","allinxswap-opbnb","binaryswap","cubiswap","pancakeswap-v3-opbnb","thena-opbnb","pancakeswap-v2-opbnb","pixelswap-opbnb","luigiswap","fourdex"], horizontal=True)

    if dex == 'All':
        # API request
        url = f"https://api.geckoterminal.com/api/v2/networks/opbnb/pools?page={page}&sort={sort}"
    else:
        url = f"https://api.geckoterminal.com/api/v2/networks/opbnb/dexes/{dex}/pools?page={page}&sort={sort}"

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
    response = requests.get(url,headers=headers)
    data = response.json()

    st.markdown("##")

    # Extract relevant data
    pools = data.get('data', [])
    formatted_data = []

    for pool in pools:
        attributes = pool['attributes']
        formatted_data.append({
            "Pool Name": attributes["name"],
            "Address": attributes["address"],
            "Volume (USD)": attributes["volume_usd"],
            "24h Volume (USD)": attributes["volume_usd"]['h24'],
            "Price Change": attributes["price_change_percentage"],
            "Price (USD)": attributes["base_token_price_usd"],
            "Reserve (USD)": attributes["reserve_in_usd"],
            "Created At": attributes["pool_created_at"]
        })

    # Display data in DataFrame
    df = pd.DataFrame(formatted_data)

    st.write("### Pool Data")
    st.dataframe(df)

    st.markdown("##")

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
