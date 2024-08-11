import streamlit as st




def page():

    # Homepage Title
    st.title("Welcome to the L2 Ecosystem Analytics Dashboard")

    # Project Overview
    st.markdown("""
    ### L2 Ecosystem Overview
    Explore high-level dashboards showcasing aggregated data and key metrics across various L2 solutions integrated with BNB Chain. Our platform provides detailed insights that help developers, investors, and newcomers understand complex data patterns over time.
    """)

    # Features Section
    st.markdown("## Core Features")

    # Feature 1: OPBNB Chain Analytics
    st.markdown("""
    ### 1. OPBNB Chain Analytics
    - **Visualize Deposits, Withdrawals, and TVL:** Get an in-depth view of the OPBNB chain with detailed metrics on deposits, withdrawals, and total value locked (TVL).
    - **AI-Driven Insights:** Our AI integration analyzes the data over time, providing actionable insights for better decision-making.
    """)

    # Feature 2: L2 Protocols Analytics
    st.markdown("""
    ### 2. L2 Protocols Analytics
    - **Comprehensive Insights:** Gain detailed analytics on top-performing protocols in the BNB L2 ecosystem, including Myshell, DeBank, APX, PancakeSwap Perpetual, Thena, Cubiswap, Binaryswap, and DerpDex.
    - **AI-Enhanced Analytics:** Our AI model continuously analyzes data, offering insights into protocol performance, trends, and opportunities for optimization.
    - **Expandable Coverage:** We're constantly adding new protocols to our analytics suite, ensuring you're always up-to-date with the latest in the L2 ecosystem.
    """)

    # Feature 3: Bridge Users Transactions Network Visualization
    st.markdown("""
    ### 3. Bridge Users Transactions Network Visualization
    - **Network Graphs:** Visualize user transactions across different bridges with interactive network graphs.
    - **Data Download:** Easily download transaction data for further analysis or reporting.
    - **AI-Powered Insights:** The AI integration highlights key patterns and trends, making it easier to understand cross-chain activities.
    """)

    # Feature 4: Contracts ABI and Source Code Data Extraction
    st.markdown("""
    ### 4. Contracts ABI and Source Code Data Extraction
    - **Detailed Data Extraction:** Access and extract ABI and source code data for L2 contracts.
    - **AI-Enhanced Analysis:** Our AI tools analyze contract data, providing insights into potential vulnerabilities, performance issues, and optimization opportunities.
    """)

    # AI Integration and Subscription Model
    st.markdown("""
    ## AI-Integrated Analytics Dashboard

    Our platform is AI-integrated, allowing for continuous analysis of data across the L2 ecosystem. Each dashboard provides insights that evolve with the data, offering clear, actionable intelligence to developers, investors, and newcomers. 

    ### Key Features:
    - **Automated Insights:** The AI model identifies important patterns and trends over time, providing notifications when significant changes or opportunities are detected.
    - **Subscription Model:** Stay ahead of the curve with our subscription service, which delivers timely notifications and updates on specific protocols or metrics.
    - **Protocol Inclusion:** Interested in having your protocol included? Connect with us to have your proposals added to our analytics suite as soon as possible.
    """)
