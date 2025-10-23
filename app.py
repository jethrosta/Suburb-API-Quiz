import streamlit as st

# --- Page Configuration ---
# Set the page config here for the entire app
st.set_page_config(
    page_title="Real Estate CMA",
    page_icon="🏘️",
    layout="wide"
)

# --- Page Definitions ---
# Define the pages in your app
# The 0_, 1_, 2_ prefixes are a common way to set the order
home_page = st.Page("pages/Home.py", title="Home", icon="🏠")
search_page = st.Page("pages/CMA_Search.py", title="CMA Search", icon="🗺️")
contact_page = st.Page("pages/Contact.py", title="Contact Us", icon="📫")

# --- Mock User Info ---
# In a real app, a login page would set this in st.session_state
if "user_info" not in st.session_state:
    st.session_state["user_info"] = {
        "name": "Feivel Jethro Ezhekiel",
        "email": "user@gmail.com",
        "picture": "https://images.unsplash.com/photo-1570295999919-56ceb5ecca61?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=256&q=80"
    }

# --- Sidebar ---
# Display user info in the sidebar
if "user_info" in st.session_state:
    user = st.session_state["user_info"]

    st.sidebar.markdown(
        f"""
        <div style="text-align:center;">
            <img src="{user['picture']}" 
                 style="width:100px;height:100px;border-radius:50%;object-fit:cover;margin-bottom:10px;">
            <h3>{user['name']}</h3>
            <p style="font-size:13px;color:gray;">{user['email']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.sidebar.divider()

# --- Navigation ---
# Set up the navigation logic
pg = st.navigation([home_page, search_page, contact_page])

# --- Run the App ---
st.sidebar.title("Navigation")
pg.run()