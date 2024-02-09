import streamlit as st
from web3 import Web3
from web3.utils.address import to_checksum_address

# Connect to Ethereum node
web3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/b18cbd493ed447e39e0cbc5b6670651a "))  # Update with your Infura project ID
contract_address = to_checksum_address("0x776a1e56d80fec35c7b16476116c4257e061c223")  # Replace with your contract address in checksum format
contract_abi = [{"constant":True,"inputs":[],"name":"getData","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"newValue","type":"uint256"}],"name":"updateData","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"}]
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Streamlit web interface
st.title("River Basin Management Interface")

# Function to get data from the smart contract
def get_data():
    data = contract.functions.getData().call()
    return data

# Function to update data in the smart contract
def update_data(new_value):
    account = web3.eth.accounts[0]  # Update with your Ethereum account address
    nonce = web3.eth.getTransactionCount(account)
    tx = contract.functions.updateData(new_value).buildTransaction({
        'chainId': 1,  # Update with your chain ID
        'gas': 100000,
        'gasPrice': web3.toWei('5', 'gwei'),
        'nonce': nonce,
    })
    signed_tx = web3.eth.account.signTransaction(tx, private_key="your_private_key")  # Replace with your private key
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    return tx_hash.hex()

# Main interface
option = st.selectbox("Select an action", ["Get Data", "Update Data"])

if option == "Get Data":
    st.subheader("Current Data")
    data = get_data()
    st.write("Data:", data)
elif option == "Update Data":
    st.subheader("Update Data")
    new_value = st.number_input("Enter new value")
    if st.button("Update"):
        tx_hash = update_data(new_value)
        st.write("Transaction Hash:", tx_hash)
