import streamlit as st

st.title("📫 Contact Us")
st.write("Please fill out the form below to get in touch with us.")

# --- Contact Form ---
with st.form(key="contact_form"):
    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    message = st.text_area("Message")
    
    submit_button = st.form_submit_button(label="Send Message")
    
    if submit_button:
        if not name or not email or not message:
            st.warning("Please fill out all fields.")
        else:
            # In a real app, you'd email this or save it to a database
            st.success(f"Thank you for your message, {name}! We will get back to you soon.")