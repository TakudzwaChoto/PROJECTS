import streamlit as st
import hashlib
import datetime
import sqlite3

# Initialize SQLite database
conn = sqlite3.connect("blockchain.db")
cursor = conn.cursor()

# Create a table to store blockchain data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS blockchain (
        index INTEGER PRIMARY KEY,
        previous_hash TEXT,
        timestamp TEXT,
        data TEXT,
        hash TEXT
    )
''')
conn.commit()

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

# Function to add a block to the blockchain
def add_block(block):
    cursor.execute('''
        INSERT INTO blockchain (index, previous_hash, timestamp, data, hash)
        VALUES (?, ?, ?, ?, ?)
    ''', (block.index, block.previous_hash, block.timestamp, block.data, block.hash))
    conn.commit()

# Function to initialize the blockchain
def initialize_blockchain():
    genesis_block = Block(0, "0", datetime.datetime.now(), "Genesis Block", "0")
    add_block(genesis_block)

# Function to fetch all blocks from the database
def fetch_blocks():
    cursor.execute("SELECT * FROM blockchain")
    return cursor.fetchall()

# Create a Streamlit app
def main():
    st.title("Blockchain App with Streamlit and SQLite")

    if "initialized" not in st.session_state:
        initialize_blockchain()
        st.session_state.initialized = True

    if st.button("Mine Block"):
        # Create a new block and add it to the blockchain
        latest_block = fetch_blocks()[-1]
        data = st.text_input("Enter block data:")
        new_block = create_block(latest_block, data)
        add_block(new_block)
        st.success("Block mined and added to the blockchain!")

    st.markdown("## Blockchain")

    # Display the blockchain
    blockchain = fetch_blocks()
    for block in blockchain:
        st.write(f"**Index:** {block[0]}")
        st.write(f"**Timestamp:** {block[2]}")
        st.write(f"**Data:** {block[3]}")
        st.write(f"**Hash:** {block[4]}")
        st.write(f"**Previous Hash:** {block[1]}")
        st.write("---")

if __name__ == "__main__":
    main()
