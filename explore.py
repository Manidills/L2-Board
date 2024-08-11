import streamlit as st
import requests
import json

# Streamlit page setup


# API key and base URL
APIkey = "1f8c991daf6942d4a222ded23215719b"
base_url = f"https://open-platform.nodereal.io/{APIkey}/op-bnb-mainnet/contract/"



def fetch_source_code(address):
    """Fetch source code for a given contract address."""
    if st.button("Fetch"):
        if address:
            api_url = f"{base_url}?action=getsourcecode&address={address}"
            response = requests.get(api_url)
            response.raise_for_status()
            return response.json()
        
def Contract_details(address):
    if st.button("Fetch"):
    # Define the JSON-RPC request payload
        api_url = "https://opbnb-mainnet.nodereal.io/v1/1f8c991daf6942d4a222ded23215719b"
        payload = {
            "jsonrpc":"2.0",
            "method":"nr_getContractCreationTransaction",
            "params":[
                address
            ],
            "id":1
        }

        # Set the headers
        headers = {
            "Content-Type": "application/json"
        }

        # Send the POST request
        response = requests.post(api_url, headers=headers, data=json.dumps(payload))

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            result = response.json()
            st.write(result)
        else:
            print(f"Request failed with status code {response.status_code}")
            st.write(response.text)



def abi(wallet_address):
    # Fetch ABI when button is clicked
    if st.button("Fetch"):
        if wallet_address:
            # Construct API URL
            api_url = f"{base_url}?action=getabi&address={wallet_address}"
            
            try:
                # Make API request
                response = requests.get(api_url)
                response.raise_for_status()  # Raise an error for bad responses

                # Parse JSON response
                abi_data = response.json()
                
                # Display ABI in a pretty format
                st.json(abi_data)

                # Provide download option
                abi_json = json.dumps(abi_data, indent=4)
                st.download_button(
                    label="Download ABI as JSON",
                    data=abi_json,
                    file_name=f"{wallet_address}_ABI.json",
                    mime="application/json"
                )

            except requests.exceptions.RequestException as e:
                st.error(f"API request failed: {e}")
        else:
            st.error("Please enter a valid wallet address.")


def explorer():
    # Input field for wallet address
    wallet_address = st.text_input("Contract Address", "0xce0e4e4d2dc0033ce2dbc35855251f4f3d086d0a")

    # Radio button for actions
    action = st.radio("Action", ["Get ABI", "Get Source Code", "Contract Creation Transaction"],horizontal=True)

    if action == 'Get ABI':
        abi(wallet_address)
    elif action == 'Get Source Code':
        source_code_data=fetch_source_code(wallet_address)
        st.json(source_code_data)
        source_code_json = json.dumps(source_code_data, indent=4)
        st.download_button(
            label="Download Source Code as JSON",
            data=source_code_json,
            file_name=f"{wallet_address}_SourceCode.json",
            mime="application/json"
        )
    elif action == 'Contract Creation Transaction':
        Contract_details(wallet_address)

