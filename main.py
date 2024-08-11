import streamlit as st
from dashboard import home
from explore import explorer
from opbnb_bridge import Bridge
from page import page
from protocols.protocols_list import protocols_types

# Set page configuration
st.set_page_config(
    page_title="L2 Analytics",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "This app generates scripts for data clean rooms!"
    }
)

# Custom CSS for a glassy, analytics-oriented sidebar
st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        background: rgba(255, 255, 255, 0.5);
        backdrop-filter: blur(10px);
        border-radius: 10px;
        padding: 20px;
    }
    .sidebar .sidebar-content img {
        margin-bottom: 20px;
    }
    .sidebar .sidebar-content .block-container {
        padding: 0 10px;
    }
    .sidebar .sidebar-content h1, .sidebar .sidebar-content h2, .sidebar .sidebar-content h3 {
        color: #333333;
    }
    .sidebar .sidebar-content .stRadio div {
        margin-bottom: 20px;
    }
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.8);
        border: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar settings
st.sidebar.image("https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExZDFjb2UzaWFwMnZqZWE1b2N3Yjc5OTltYzdxM2h5YXY2MWd6MXBxbyZlcD12MV9pbnRlcm5naWZfYnlfaWQmY3Q9cw/UAragLbg9oKRfZLThq/giphy.webp", use_column_width=True)
st.sidebar.title("L2 Analytics Dashboard")

# Add icons to each action
actions = {
    "Home": ("🏠",page),
    "OPBNB Analytics": ("📊", home),
    "L2 Protocols": ("🔗", protocols_types),
    "Bridge Visualization": ("🌉", Bridge),
    "Contracts": ("📜", explorer)
}

# Create a radio button with icons
action = st.sidebar.radio("Choose an action:", list(actions.keys()), format_func=lambda x: f"{actions[x][0]} {x}")

# Main function to handle different actions
def main():
    actions[action][1]()

if __name__ == "__main__":
    main()
