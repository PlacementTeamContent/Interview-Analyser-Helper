# import pywhatkit as kit
import streamlit as st

def send_whatsapp_message(phone_number, message):
    # kit.sendwhatmsg_instantly(phone_number, message)
    if phone_number and message:
        whatsapp_url = f"https://web.whatsapp.com/send?phone={phone_number}&text={message}"
        # Inject JavaScript to automatically redirect the user to WhatsApp Web
        redirection_script = f"""
            <script type="text/javascript">
                window.open("{whatsapp_url}", "_blank");
                console.log("Running...");
            </script>
            """

        st.markdown(redirection_script, unsafe_allow_html=True)
    else:
        st.error("Invalid Details")

