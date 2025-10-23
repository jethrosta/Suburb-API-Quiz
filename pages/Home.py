import streamlit as st

st.title("🏡 Welcome to the Real Estate CMA Tool")
st.markdown("""
    This web application provides a **Comparative Market Analysis (CMA)** for properties in Australia.
    
    It is powered by the [Microburbs API](https://www.microburbs.com.au/report_generator/api/sandbox/cma/cma) sandbox.

    ### How to use this tool:
    1.  Navigate to the **CMA Search** page using the sidebar.
    2.  **Click on the map** at any location in Australia.
    3.  The app will find the address for that location.
    4.  It will then generate the CMA report for you automatically.
    
    You can also visit the **Contact** page to get in touch.
""")

# Adding an image for visual appeal
st.image("images/house.jpg", 
         caption="Find your property's value", use_container_width=True)