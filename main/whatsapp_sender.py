# import pywhatkit as kit
import streamlit as st

def send_whatsapp_message(phone_number, message):
    # kit.sendwhatmsg_instantly(phone_number, message)
    if phone_number and message:
        whatsapp_url = f"https://web.whatsapp.com/send?phone={phone_number}&text={message}"
        st.markdown(f'<meta http-equiv="refresh" content="0; url={whatsapp_url}">', unsafe_allow_html=True)

