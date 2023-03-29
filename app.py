import streamlit as st
import requests
import pandas as pd

blockchair_base_url = "https://api.blockchair.com/bitcoin"

def fetch_transaction_data(tx_hash):
    url = f"{blockchair_base_url}/dashboards/transaction/{tx_hash}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

st.title("Bitcoin Transaction Visualizer")

tx_hash_input = st.text_input("Enter a Bitcoin transaction hash:")

if tx_hash_input:
    tx_data = fetch_transaction_data(tx_hash_input)

    if tx_data:
        st.subheader("Transaction Details")
        st.write(f"Transaction hash: {tx_data['data'][tx_hash_input]['transaction']['hash']}")
        st.write(f"Size: {tx_data['data'][tx_hash_input]['transaction']['size']} bytes")
        st.write(f"Fee: {tx_data['data'][tx_hash_input]['transaction']['fee']} satoshis")

        st.subheader("Inputs")
        inputs_df = pd.DataFrame(tx_data['data'][tx_hash_input]['inputs'])
        if not inputs_df.empty:
            st.dataframe(inputs_df[['recipient', 'value']])
        else:
            st.write("No inputs data available")

        st.subheader("Outputs")
        outputs_df = pd.DataFrame(tx_data['data'][tx_hash_input]['outputs'])
        if not outputs_df.empty:
            st.dataframe(outputs_df[['recipient', 'value']])
        else:
            st.write("No outputs data available")
    else:
        st.error("Error fetching transaction data. Please check the transaction hash and try again.")