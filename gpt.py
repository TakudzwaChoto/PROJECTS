import streamlit as st
import sqlite3

# Create or connect to the SQLite database
conn = sqlite3.connect('blog_app.db')
c = conn.cursor()

# Create tables for users and blog posts
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        content TEXT,
        author TEXT,
        likes INTEGER DEFAULT 0
    )
''')

def create_account(username, password):
    try:
        # Insert the new user account into the database
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def login(username, password):
    # Check if the provided username and password match a user account
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    result = c.fetchone()
    if result is not None:
        return True
    else:
        return False

def create_post(title, content, author):
    # Insert the new blog post into the database
    c.execute("INSERT INTO posts (title, content, author) VALUES (?, ?, ?)", (title, content, author))
    conn.commit()

def like_post(post_id):
    # Update the likes count for the specified post
    c.execute("UPDATE posts SET likes = likes + 1 WHERE id = ?", (post_id,))
    conn.commit()

def get_all_posts():
    # Retrieve all blog posts from the database
    c.execute("SELECT * FROM posts")
    return c.fetchall()

def main():
    st.title("Blog App")

    # Page state
    page = st.sidebar.selectbox("Select a page", ["Create Account", "Login", "Write Post"])

    if page == "Create Account":
        st.header("Create Account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Create Account"):
            if username and password:
                if create_account(username, password):
                    st.success("Account created successfully!")
                else:
                    st.error("Username already exists. Please choose a different username.")
            else:
                st.warning("Please enter a username and password.")

    elif page == "Login":
        st.header("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username and password:
                if login(username, password):
                    st.success("Login successful!")
                    st.sidebar.success(f"Logged in as {username}")
                else:
                    st.error("Invalid username or password.")
            else:
                st.warning("Please enter a username and password.")

    elif page == "Write Post":
        st.header("Write Post")

        # Check if the user is logged in
        if 'username' not in st.session_state:
            st.warning("Please log in to write a post.")
            return

        title = st.text_input("Title")
        content = st.text_area("Content")

        if st.button("Post"):
            if title and content:
                author = st.session_state['username']
                create_post(title, content, author)
                st.success("Post created successfully!")
            else:
                st.warning("Please enter a title and content.")

    # Display all blog posts
    posts = get_all_posts()
    if posts:
        st.header("Blog Posts")
        for post in posts:
            st.subheader(post[1])
            st.write(post[2])
            st.write(f"Author: {post[3]}")
            st.write(f"Likes: {post[4]}")
            if st.button(f"Like ({post[4]})"):
                like_post(post[0])
                st.success("Post liked!")
            st.write("---")

if __name__ == "__main__":
    main()
