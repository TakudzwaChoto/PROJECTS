import streamlit as st
import requests

# Function to fetch cryptocurrency prices from an API
def fetch_crypto_prices():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin,ethereum,ripple",
        "vs_currencies": "usd",
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data

# Main Streamlit app
def main():
    st.title("Cryptocurrency Price Tracker")

    # Fetch cryptocurrency prices
    crypto_data = fetch_crypto_prices()

    # Display cryptocurrency prices
    st.header("Current Prices (USD)")
    st.subheader("Bitcoin (BTC): ${}".format(crypto_data["bitcoin"]["usd"]))
    st.subheader("Ethereum (ETH): ${}".format(crypto_data["ethereum"]["usd"]))
    st.subheader("Ripple (XRP): ${}".format(crypto_data["ripple"]["usd"]))

if __name__ == "__main__":
    main()
