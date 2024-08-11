from io import StringIO
import streamlit as st
import pandas as pd
import requests
import json
from pyvis.network import Network
import tempfile
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
    prompt = f"Here opbnb bridgeing related data\n{csv_data_str}\ngive some short summary insights about the data in 6 sentences and there connections in points"
    st.write(chat_bot(prompt))

def create_deposit_erc20_network_graph():
    # User input for the query parameters
    first = st.number_input("Number of records to fetch", min_value=1, max_value=50, value=5)
    orderBy_options = st.selectbox("Order By", ["amount", "id","l1Token", "l2Token", "extraData", "from", "to"])
    orderD = st.selectbox("Order Direction", ['desc', 'asc'])
    submit_button = st.button('Submit')
    
    if submit_button:
        # Constructing the query with user input
        query = f"""
        {{
          depositERC20S(first: {first}, orderBy: {orderBy_options}, orderDirection: {orderD}) {{
            id
            l1Token
            l2Token
            from
            amount
            extraData
            to
          }}
          _meta {{
            hasIndexingErrors
            deployment
            block {{
              hash
              number
              parentHash
              timestamp
            }}
          }}
        }}
        """
        
        # Updated URL for the GraphQL endpoint
       # url = "https://gateway-arbitrum.network.thegraph.com/api/535e83a86f270e66f83c6227ae349334/subgraphs/id/HTkQvHkKroPxygp8B2yrwSrRe1MMzvSpvUmXoPypfXAw"
        url = "https://gateway-arbitrum.network.thegraph.com/api/535e83a86f270e66f83c6227ae349334/subgraphs/id/34BDYDFAm5Twh6hpBygKQdC9NEE34K3TweDSvTadXbUp"
        response = requests.post(url, json={'query': query})
        
        if response.status_code == 200:
            data = response.json()['data']
            st.dataframe(data['depositERC20S'])

            st.markdown("##")
            generate_summary(pd.DataFrame(data['depositERC20S']))
            st.markdown("##")
        else:
            raise Exception(f"Query failed to run by returning code of {response.status_code}. {query}")
        
        # Extracting data for nodes and edges
        nodes = []
        edges = []
        
        for deposit in data['depositERC20S']:
            l1_token = deposit['l1Token']
            l2_token = deposit['l2Token']
            from_address = deposit['from']
            to_address = deposit['to']
            amount = deposit['amount']
            extra_data = deposit['extraData']
            
            # Adding nodes
            nodes.extend([
                {'id': f"From: {from_address}", 'label': f"From: {from_address}", 'title': ''},
                {'id': f"To: {to_address}", 'label': f"To: {to_address}", 'title': ''},
                {'id': f"L1 Token: {l1_token}", 'label': f"L1 Token: {l1_token}", 'title': ''},
                {'id': f"L2 Token: {l2_token}", 'label': f"L2 Token: {l2_token}", 'title': ''},
                {'id': f"Amount: {amount}", 'label': f"Amount: {amount}", 'title': f"Extra Data: {extra_data}"}
            ])
            
            # Adding edges
            edges.extend([
                {'source': f"From: {from_address}", 'target': f"To: {to_address}"},
                {'source': f"From: {from_address}", 'target': f"L1 Token: {l1_token}"},
                {'source': f"To: {to_address}", 'target': f"L2 Token: {l2_token}"},
                {'source': f"L2 Token: {l2_token}", 'target': f"Amount: {amount}"}
            ])
        
        # Creating the network graph
        graph = Network(height="800px", width="100%", notebook=True)
        
        for node in nodes:
            graph.add_node(node['id'], label=node['label'], title=node['title'])
        
        for edge in edges:
            graph.add_edge(edge['source'], edge['target'])

        # Using a temporary file to display the graph
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpfile:
            graph.show(tmpfile.name)
            tmpfile.seek(0)
            html_content = tmpfile.read().decode("utf-8")


        return html_content


def create_deposit_eth_network_graph():
    # User input for the query parameters
    first = st.number_input("Number of records to fetch", min_value=1, max_value=50, value=10)
    orderBy_options = st.selectbox("Order By", ["amount","extraData", "from", "to"])
    orderD = st.selectbox("Order Direction", ['desc', 'asc'])
    submit_button = st.button('Submit')
    
    if submit_button:
        # Constructing the query with user input
        query = """
        {
          depositETHs(first: %d, orderBy: %s, orderDirection: desc ) {
            amount
            extraData
            from
            id
            to
          }
          _meta {
            deployment
            hasIndexingErrors
            block {
              hash
              number
              parentHash
              timestamp
            }
          }
        }
        """ % (first, orderBy_options)
        
        # Updated URL for the GraphQL endpoint
        url = "https://gateway-arbitrum.network.thegraph.com/api/535e83a86f270e66f83c6227ae349334/subgraphs/id/34BDYDFAm5Twh6hpBygKQdC9NEE34K3TweDSvTadXbUp"
        response = requests.post(url, json={'query': query})
        
        if response.status_code == 200:
            data = response.json()['data']
            depositETHs = data['depositETHs']
            st.dataframe(depositETHs)
            st.markdown("##")
            generate_summary(pd.DataFrame(data['depositETHs']))
            st.markdown("##")
        else:
            raise Exception(f"Query failed to run by returning code of {response.status_code}. {query}")
        
        # Extracting data for nodes and edges
        nodes = []
        edges = []
        
        for deposit in depositETHs:
            from_address = deposit['from']
            to_address = deposit['to']
            amount = deposit['amount']
            extra_data = deposit['extraData']
            
            # Adding nodes
            nodes.extend([
                {'id': f"From: {from_address}", 'label': f"From: {from_address}", 'title': ''},
                {'id': f"To: {to_address}", 'label': f"To: {to_address}", 'title': ''},
                {'id': f"Amount: {amount}", 'label': f"Amount: {amount}", 'title': f"Extra Data: {extra_data}"}
            ])
            
            # Adding edges
            edges.extend([
                {'source': f"From: {from_address}", 'target': f"To: {to_address}"},
                {'source': f"To: {to_address}", 'target': f"Amount: {amount}"}
            ])
        
        # Creating the network graph
        graph = Network(height="800px", width="100%", notebook=True)
        
        for node in nodes:
            graph.add_node(node['id'], label=node['label'], title=node['title'])
        
        for edge in edges:
            graph.add_edge(edge['source'], edge['target'])

        # Using a temporary file to display the graph
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpfile:
            graph.show(tmpfile.name)
            tmpfile.seek(0)
            html_content = tmpfile.read().decode("utf-8")

        return html_content
    

def create_withdrawal_erc20_network_graph():
    # User input for the query parameters
    first = st.number_input("Number of records to fetch", min_value=1, max_value=50, value=10)
    orderBy_options = st.selectbox("Order By", ["amount", "from", "to", "id", "l1Token", "l2Token"])
    skip = st.number_input("Number of records to skip", min_value=0, max_value=100, value=10)
    orderD = st.selectbox("Order Direction", ['desc', 'asc'])
    submit_button = st.button('Submit')
    
    if submit_button:
        # Constructing the query with user input
        query = f"""
        {{
          withdrawalERC20S(first: {first}, orderBy: {orderBy_options}, orderDirection: {orderD}, skip: {skip}) {{
            amount
            extraData
            from
            id
            l1Token
            l2Token
            to
          }}
          _meta {{
            deployment
            hasIndexingErrors
            block {{
              hash
              number
              parentHash
              timestamp
            }}
          }}
        }}
        """
        
        # Updated URL for the GraphQL endpoint
        url = "https://gateway-arbitrum.network.thegraph.com/api/535e83a86f270e66f83c6227ae349334/subgraphs/id/34BDYDFAm5Twh6hpBygKQdC9NEE34K3TweDSvTadXbUp"
        response = requests.post(url, json={'query': query})
        
        if response.status_code == 200:
            data = response.json()['data']
            withdrawalERC20S = data['withdrawalERC20S']
            st.dataframe(withdrawalERC20S)
            st.markdown("##")
            generate_summary(pd.DataFrame(withdrawalERC20S))
            st.markdown("##")
        else:
            raise Exception(f"Query failed to run by returning code of {response.status_code}. {query}")
        
        # Extracting data for nodes and edges
        nodes = []
        edges = []
        
        for withdrawal in withdrawalERC20S:
            l1_token = withdrawal['l1Token']
            l2_token = withdrawal['l2Token']
            from_address = withdrawal['from']
            to_address = withdrawal['to']
            amount = withdrawal['amount']
            extra_data = withdrawal['extraData']
            
            # Adding nodes
            nodes.extend([
                {'id': f"From: {from_address}", 'label': f"From: {from_address}", 'title': ''},
                {'id': f"To: {to_address}", 'label': f"To: {to_address}", 'title': ''},
                {'id': f"L1 Token: {l1_token}", 'label': f"L1 Token: {l1_token}", 'title': ''},
                {'id': f"L2 Token: {l2_token}", 'label': f"L2 Token: {l2_token}", 'title': ''},
                {'id': f"Amount: {amount}", 'label': f"Amount: {amount}", 'title': f"Extra Data: {extra_data}"}
            ])
            
            # Adding edges
            edges.extend([
                {'source': f"From: {from_address}", 'target': f"To: {to_address}"},
                {'source': f"From: {from_address}", 'target': f"L1 Token: {l1_token}"},
                {'source': f"To: {to_address}", 'target': f"L2 Token: {l2_token}"},
                {'source': f"L2 Token: {l2_token}", 'target': f"Amount: {amount}"}
            ])
        
        # Creating the network graph
        graph = Network(height="800px", width="100%", notebook=True)
        
        for node in nodes:
            graph.add_node(node['id'], label=node['label'], title=node['title'])
        
        for edge in edges:
            graph.add_edge(edge['source'], edge['target'])

        # Using a temporary file to display the graph
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpfile:
            graph.show(tmpfile.name)
            tmpfile.seek(0)
            html_content = tmpfile.read().decode("utf-8")

        return html_content
    

def create_withdrawal_eth_network_graph():
    # User input for the query parameters
    first = st.number_input("Number of records to fetch", min_value=1, max_value=50, value=10)
    orderBy_options = st.selectbox("Order By", ["amount", "from", "to", "id"])
    skip = st.number_input("Number of records to skip", min_value=0, max_value=100, value=10)
    orderD = st.selectbox("Order Direction", ['desc', 'asc'])
    submit_button = st.button('Submit')
    
    if submit_button:
        # Constructing the query with user input
        query = f"""
        query MyQuery {{
          _meta {{
            deployment
            hasIndexingErrors
            block {{
              hash
              number
              parentHash
              timestamp
            }}
          }}
          withdrawalETHs(first: {first}, orderBy: {orderBy_options}, orderDirection: {orderD}, skip: {skip}) {{
            amount
            extraData
            from
            id
            to
          }}
        }}
        """
        
        # Updated URL for the GraphQL endpoint
        url = "https://gateway-arbitrum.network.thegraph.com/api/535e83a86f270e66f83c6227ae349334/subgraphs/id/34BDYDFAm5Twh6hpBygKQdC9NEE34K3TweDSvTadXbUp"
        response = requests.post(url, json={'query': query})
        
        if response.status_code == 200:
            data = response.json()['data']
            withdrawalETHs = data['withdrawalETHs']
            st.dataframe(withdrawalETHs)
            st.markdown("##")
            generate_summary(pd.DataFrame(withdrawalETHs))
            st.markdown("##")
        else:
            raise Exception(f"Query failed to run by returning code of {response.status_code}. {query}")
        
        # Extracting data for nodes and edges
        nodes = []
        edges = []
        
        for withdrawal in withdrawalETHs:
            from_address = withdrawal['from']
            to_address = withdrawal['to']
            amount = withdrawal['amount']
            extra_data = withdrawal['extraData']
            
            # Adding nodes
            nodes.extend([
                {'id': f"From: {from_address}", 'label': f"From: {from_address}", 'title': ''},
                {'id': f"To: {to_address}", 'label': f"To: {to_address}", 'title': ''},
                {'id': f"Amount: {amount}", 'label': f"Amount: {amount}", 'title': f"Extra Data: {extra_data}"}
            ])
            
            # Adding edges
            edges.extend([
                {'source': f"From: {from_address}", 'target': f"To: {to_address}"},
                {'source': f"To: {to_address}", 'target': f"Amount: {amount}"}
            ])
        
        # Creating the network graph
        graph = Network(height="800px", width="100%", notebook=True)
        
        for node in nodes:
            graph.add_node(node['id'], label=node['label'], title=node['title'])
        
        for edge in edges:
            graph.add_edge(edge['source'], edge['target'])

        # Using a temporary file to display the graph
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpfile:
            graph.show(tmpfile.name)
            tmpfile.seek(0)
            html_content = tmpfile.read().decode("utf-8")

        return html_content
    

def create_withdrawal_eth():
    # Hardcoded ID for the specific withdrawalETH query
    withdrawal_id = st.text_input("")
    submit_button = st.button('Fetch Data')
    
    if submit_button:
        # Constructing the query with the specific ID
        query = f"""
        {{
          _meta {{
            deployment
            hasIndexingErrors
            block {{
              hash
              number
              parentHash
              timestamp
            }}
          }}
          withdrawalETH(id: "{withdrawal_id}") {{
            amount
            extraData
            from
            id
            to
          }}
        }}
        """
        
        # Updated URL for the GraphQL endpoint
        url = "https://gateway-arbitrum.network.thegraph.com/api/535e83a86f270e66f83c6227ae349334/subgraphs/id/34BDYDFAm5Twh6hpBygKQdC9NEE34K3TweDSvTadXbUp"
        response = requests.post(url, json={'query': query})
        
        if response.status_code == 200:
            data = response.json()['data']
            withdrawalETH = data['withdrawalETH']
            st.dataframe(withdrawalETH)
            st.markdown("##")
            generate_summary(pd.DataFrame(withdrawalETH))
            st.markdown("##")
        else:
            raise Exception(f"Query failed to run by returning code of {response.status_code}. {query}")
        
        # Extracting data for nodes and edges
        nodes = []
        edges = []
        
        if withdrawalETH:
            from_address = withdrawalETH['from']
            to_address = withdrawalETH['to']
            amount = withdrawalETH['amount']
            extra_data = withdrawalETH['extraData']
            
            # Adding nodes
            nodes.extend([
                {'id': f"From: {from_address}", 'label': f"From: {from_address}", 'title': ''},
                {'id': f"To: {to_address}", 'label': f"To: {to_address}", 'title': ''},
                {'id': f"Amount: {amount}", 'label': f"Amount: {amount}", 'title': f"Extra Data: {extra_data}"}
            ])
            
            # Adding edges
            edges.extend([
                {'source': f"From: {from_address}", 'target': f"To: {to_address}"},
                {'source': f"To: {to_address}", 'target': f"Amount: {amount}"}
            ])
        
        # Creating the network graph
        graph = Network(height="800px", width="100%", notebook=True)
        
        for node in nodes:
            graph.add_node(node['id'], label=node['label'], title=node['title'])
        
        for edge in edges:
            graph.add_edge(edge['source'], edge['target'])

        # Using a temporary file to display the graph
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpfile:
            graph.show(tmpfile.name)
            tmpfile.seek(0)
            html_content = tmpfile.read().decode("utf-8")

        return html_content
    

def create_deposit_eth():
    # User input for the specific depositETH ID
    deposit_id = st.text_input("Enter Deposit ETH ID", value="0xba157df5056139d95ce456169de5152c15523c08790edb2f98cd569c3f42b4d7-57")
    submit_button = st.button('Fetch Data')
    
    if submit_button:
        # Constructing the query with the specific ID
        query = f"""
        {{
          _meta {{
            deployment
            hasIndexingErrors
            block {{
              hash
              number
              parentHash
              timestamp
            }}
          }}
          depositETH(id: "{deposit_id}") {{
            amount
            extraData
            from
            id
            to
          }}
        }}
        """
        
        # Updated URL for the GraphQL endpoint
        url = "https://gateway-arbitrum.network.thegraph.com/api/535e83a86f270e66f83c6227ae349334/subgraphs/id/34BDYDFAm5Twh6hpBygKQdC9NEE34K3TweDSvTadXbUp"
        response = requests.post(url, json={'query': query})
        
        if response.status_code == 200:
            data = response.json()['data']
            depositETH = data['depositETH']
            st.dataframe(depositETH)
            st.markdown("##")
            generate_summary(pd.DataFrame(depositETH))
            st.markdown("##")
        else:
            raise Exception(f"Query failed to run by returning code of {response.status_code}. {query}")
        
        # Extracting data for nodes and edges
        nodes = []
        edges = []
        
        if depositETH:
            from_address = depositETH['from']
            to_address = depositETH['to']
            amount = depositETH['amount']
            extra_data = depositETH['extraData']
            
            # Adding nodes
            nodes.extend([
                {'id': f"From: {from_address}", 'label': f"From: {from_address}", 'title': ''},
                {'id': f"To: {to_address}", 'label': f"To: {to_address}", 'title': ''},
                {'id': f"Amount: {amount}", 'label': f"Amount: {amount}", 'title': f"Extra Data: {extra_data}"}
            ])
            
            # Adding edges
            edges.extend([
                {'source': f"From: {from_address}", 'target': f"To: {to_address}"},
                {'source': f"To: {to_address}", 'target': f"Amount: {amount}"}
            ])
        
        # Creating the network graph
        graph = Network(height="800px", width="100%", notebook=True)
        
        for node in nodes:
            graph.add_node(node['id'], label=node['label'], title=node['title'])
        
        for edge in edges:
            graph.add_edge(edge['source'], edge['target'])

        # Using a temporary file to display the graph
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpfile:
            graph.show(tmpfile.name)
            tmpfile.seek(0)
            html_content = tmpfile.read().decode("utf-8")

        return html_content


def create_deposit_erc20():
    # User input for the specific depositERC20 ID
    deposit_id = st.text_input("Enter Deposit ERC20 ID", value="0xd87943ea7ef673b4f6ffe2f2638772861d3f81f91e4509dc07680c05e11d23ab-212")
    submit_button = st.button('Fetch Data')
    
    if submit_button:
        # Constructing the query with the specific ID
        query = f"""
        {{
          _meta {{
            deployment
            hasIndexingErrors
            block {{
              hash
              number
              parentHash
              timestamp
            }}
          }}
          depositERC20(id: "{deposit_id}") {{
            amount
            extraData
            from
            id
            l1Token
            l2Token
            to
          }}
        }}
        """
        
        # Updated URL for the GraphQL endpoint
        url = "https://gateway-arbitrum.network.thegraph.com/api/535e83a86f270e66f83c6227ae349334/subgraphs/id/34BDYDFAm5Twh6hpBygKQdC9NEE34K3TweDSvTadXbUp"
        response = requests.post(url, json={'query': query})
        
        if response.status_code == 200:
            data = response.json()['data']
            depositERC20 = data['depositERC20']
            st.dataframe(depositERC20)
            st.markdown("##")
            generate_summary(pd.DataFrame(depositERC20))
            st.markdown("##")
        else:
            raise Exception(f"Query failed to run by returning code of {response.status_code}. {query}")
        
        # Extracting data for nodes and edges
        nodes = []
        edges = []
        
        if depositERC20:
            l1_token = depositERC20['l1Token']
            l2_token = depositERC20['l2Token']
            from_address = depositERC20['from']
            to_address = depositERC20['to']
            amount = depositERC20['amount']
            extra_data = depositERC20['extraData']
            
            # Adding nodes
            nodes.extend([
                {'id': f"From: {from_address}", 'label': f"From: {from_address}", 'title': ''},
                {'id': f"To: {to_address}", 'label': f"To: {to_address}", 'title': ''},
                {'id': f"L1 Token: {l1_token}", 'label': f"L1 Token: {l1_token}", 'title': ''},
                {'id': f"L2 Token: {l2_token}", 'label': f"L2 Token: {l2_token}", 'title': ''},
                {'id': f"Amount: {amount}", 'label': f"Amount: {amount}", 'title': f"Extra Data: {extra_data}"}
            ])
            
            # Adding edges
            edges.extend([
                {'source': f"From: {from_address}", 'target': f"To: {to_address}"},
                {'source': f"From: {from_address}", 'target': f"L1 Token: {l1_token}"},
                {'source': f"To: {to_address}", 'target': f"L2 Token: {l2_token}"},
                {'source': f"L2 Token: {l2_token}", 'target': f"Amount: {amount}"}
            ])
        
        # Creating the network graph
        graph = Network(height="800px", width="100%", notebook=True)
        
        for node in nodes:
            graph.add_node(node['id'], label=node['label'], title=node['title'])
        
        for edge in edges:
            graph.add_edge(edge['source'], edge['target'])

        # Using a temporary file to display the graph
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpfile:
            graph.show(tmpfile.name)
            tmpfile.seek(0)
            html_content = tmpfile.read().decode("utf-8")

        return html_content


def Bridge():
    st.title('OpBNB Bridge Users')
    st.markdown("### Select an Option")
    option = st.radio(
        "Select Choice",
        ("Deposit_ERC20s", "Deposit_ETHs", "Withdraw_ERC20s", "Withdraw_ETHs", "ETH_Withdrawal_ID" ,"ETH_Deposit_ID", "ERC20s_Deposit_ID"),
        index=0,
        horizontal=True
    )

    if option == 'Deposit_ERC20s':
        html_content = create_deposit_erc20_network_graph()
        st.components.v1.html(html_content, height=800)
    elif option == 'Deposit_ETHs':
        html_content = create_deposit_eth_network_graph()
        st.components.v1.html(html_content, height=800)
    elif option == 'Withdraw_ERC20s':
        html_content = create_withdrawal_erc20_network_graph()
        st.components.v1.html(html_content, height=800)
    elif option == 'Withdraw_ETHs':
        html_content = create_withdrawal_eth_network_graph()
        st.components.v1.html(html_content, height=800)
    elif option == 'ETH_Withdrawal_ID':
        html_content = create_withdrawal_eth()
        st.components.v1.html(html_content, height=800)
    elif option == 'ETH_Deposit_ID':
        html_content = create_deposit_eth()
        st.components.v1.html(html_content, height=800)
    elif option == 'ERC20s_Deposit_ID':
        html_content = create_deposit_erc20()
        st.components.v1.html(html_content, height=800)
        