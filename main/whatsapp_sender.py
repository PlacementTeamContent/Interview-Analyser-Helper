# import pywhatkit as kit
import streamlit as st

def send_whatsapp_message(phone_number, message):
    # kit.sendwhatmsg_instantly(phone_number, message)
    if phone_number and message:
        whatsapp_url = f"https://web.whatsapp.com/send?phone={phone_number}&text={message}"
        st.markdown(f"""
        <a href="{whatsapp_url}" target="_blank">Send Message to {phone_number}</a>
    """, unsafe_allow_html=True)
    else:
        st.error("Invalid Details")

