import streamlit as st

# Simple in-memory "database"
USERS = {
    "admin": "admin123"
}


def login(username, password):
    if username in USERS and USERS[username] == password:
        st.session_state["logged_in"] = True
        st.session_state["user"] = username
        return True
    return False


def signup(username, password):
    if username in USERS:
        return False
    USERS[username] = password
    return True


def logout():
    st.session_state["logged_in"] = False
    st.session_state["user"] = None