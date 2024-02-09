import streamlit as st
import sqlite3
from sqlite3 import Error
from passlib.hash import pbkdf2_sha256

# Create or connect to the SQLite database
def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('user.db')
        print('Successfully connected to SQLite database')
    except Error as e:
        print(e)
    return conn

# Create the users table if it doesn't exist
def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        print('Table created or already exists')
    except Error as e:
        print(e)

# Hash the provided password
def hash_password(password):
    return pbkdf2_sha256.hash(password)

# Verify the provided password with the stored hash
def verify_password(password, stored_hash):
    return pbkdf2_sha256.verify(password, stored_hash)

# Insert a new user into the database
def insert_user(conn, username, password):
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        print('User created successfully')
    except Error as e:
        print(e)

# Check if a user with the provided username exists in the database
def user_exists(conn, username):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    return user is not None

# Get the stored password hash for the provided username
def get_password_hash(conn, username):
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
    row = cursor.fetchone()
    return row[0] if row else None

# Create a new user account
def create_account(conn, username, password):
    if user_exists(conn, username):
        st.error('Username already exists. Please choose a different username.')
    else:
        hashed_password = hash_password(password)
        insert_user(conn, username, hashed_password)
        st.success('Account created successfully!')

# Verify the login credentials and log the user in
def login(conn, username, password):
    stored_hash = get_password_hash(conn, username)
    if stored_hash is not None and verify_password(password, stored_hash):
        st.success('Logged in successfully!')
        return True
    else:
        st.error('Invalid username or password!')
        return False

# Streamlit app
def main():
    st.title('User Authentication')

    # Create or connect to the database
    conn = create_connection()
    create_table(conn)

    # Pages
    page = st.sidebar.selectbox('Select Page', ['Login', 'Create Account'])

    if page == 'Login':
        st.header('Login')
        username = st.text_input('Username')
        password = st.text_input('Password', type='password')
        if st.button('Login'):
            if login(conn, username, password):
                # Store the logged-in user in the session
                st.session_state.username = username

    elif page == 'Create Account':
        st.header('Create Account')
        username = st.text_input('Username')
        password = st.text_input('Password', type='password')
        if st.button('Create Account'):
            create_account(conn, username, password)

    # Logout button
    if 'username' in st.session_state:
        st.write(f"Logged in as {st.session_state.username}")
        if st.button('Logout'):
            # Clear the session
            st.session_state.pop('username')
            st.success('Logged out successfully!')

if __name__ == '__main__':
    main()
