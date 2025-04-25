import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()


# Function to send email
def send_email(subject, body, recipients):
    # Get secrets from Streamlit Cloud environment
    sender_email = st.secrets["auth"]["email"]
    sender_password = st.secrets["auth"]["password"]

    # sender_email = os.getenv("EMAIL")
    # sender_password = os.getenv("APP_PASSWORD")

    try:
        # Set up the server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        # Log in to the server
        server.login(sender_email, sender_password)

        # Prepare the message
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = ", ".join(recipients)
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        # Send the email
        server.sendmail(sender_email, recipients, message.as_string())
        server.quit()
        return "Email sent successfully!"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__=='__main__':
    print(send_email("Testing", "Hi, Test Mail", ['']))


