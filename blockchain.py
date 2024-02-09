import streamlit as st
import hashlib
import datetime

# Define a Block class
class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

# Function to create a new block
def create_block(previous_block, data):
    index = previous_block.index + 1
    timestamp = datetime.datetime.now()
    previous_hash = previous_block.hash
    raw_data = f"{index}{previous_hash}{timestamp}{data}"
    hash = hashlib.sha256(raw_data.encode()).hexdigest()
    return Block(index, previous_hash, timestamp, data, hash)

# Function to initialize the blockchain
def initialize_blockchain():
    genesis_block = Block(0, "0", datetime.datetime.now(), "Genesis Block", "0")
    blockchain = [genesis_block]
    return blockchain

# Create a Streamlit app
def main():
    st.title("Blockchain Viewer")

    # Initialize the blockchain
    blockchain = initialize_blockchain()

    if st.button("Add Block"):
        # Create a new block and add it to the blockchain
        data = st.text_input("Enter block data:")
        new_block = create_block(blockchain[-1], data)
        blockchain.append(new_block)
        st.success("Block added successfully!")

    st.markdown("## Blockchain")

    # Display the blockchain
    for block in blockchain:
        st.write(f"**Index:** {block.index}")
        st.write(f"**Timestamp:** {block.timestamp}")
        st.write(f"**Data:** {block.data}")
        st.write(f"**Hash:** {block.hash}")
        st.write(f"**Previous Hash:** {block.previous_hash}")
        st.write("---")

if __name__ == "__main__":
    main()
