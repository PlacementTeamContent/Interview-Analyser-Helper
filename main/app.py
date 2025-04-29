from .sheet_connector import GoogleSheetsCRUD
from .mail_sender import send_email
from pathlib import Path
import pandas as pd
import streamlit as st
import pandas as pd
import sys
import time
from .utils import *
from datetime import datetime, timedelta, time


BASE_DIR = Path(__file__).parent.parent

def get_endtime(start_time, duration):
    start_datetime = datetime.combine(datetime.today(), start_time)
    end_datetime = start_datetime + timedelta(minutes=duration)
    return end_datetime.time()

def home_page():
    if "data" not in st.session_state:
        st.session_state.data = load_data()

    st.title("Send Message Template")

    # Sample data
    interviewers = get_interviewers(st.session_state.data)
    all_domains = get_domains()

    # Interviewer selection
    selected_interviewers = st.multiselect("Interviewer Names", interviewers)

    # Domain selection via checkboxes
    st.subheader("Interview Domain")
    selected_domains = []
    cols = st.columns(3)
    for i, domain in enumerate(all_domains):
        if cols[i % 3].checkbox(domain, value=False):
            selected_domains.append(domain)
    st.subheader("Interview Duration (in minutes)")
    duration = st.number_input(label='Duration', min_value=5, max_value=(24*60), value=60, step=5)

    # Generate message preview
    # if selected_interviewers and selected_domains:
    #     preview_message = (
    #         get_message(temp=True)
    #     )
    # else:
    #     preview_message = "Please select at least one interviewer and one domain."

    divider()

    mail_template =(""
               "Hi {name},\n"
               "\nAre you available tomorrow, {date} to conduct the {domains} interview?\n"
               "If yes, please share your available time slots using the form below?\n\n"
               "{form_link}\n"
               "\nInterview Duration: {duration}"
               )

    st.subheader("Mail Configuration")
    subject = st.text_input("Subject")
    mail_template = st.text_area("Mail Body Template", mail_template, height=200)
    st.warning("Make sure mail template will contain these 5 placeholders.\n[{name}, {date}, {domains}, {form_link},{duration}]")

    if selected_interviewers and selected_domains and len(subject)>0 and len(mail_template)>0:
        refined_df = pd.DataFrame(get_contact_list(
                df=st.session_state.data,
                names=selected_interviewers,
                date=get_next_day_date(),
                domains='/'.join(selected_domains),
                duration= f"{duration} Minutes",
                template=mail_template
            ),
            columns=["Name", "Email_Id", "Message"]
        )

        divider()

        st.dataframe(refined_df)

        if st.button("Send Mail"):
            log_box = st.empty()
            for row in refined_df.itertuples():
                if(len(row.Email_Id) > 0):
                    log_box.write(f"Sending Mail to {row.Name} with Mail {row.Email_Id}")
                    send_email(subject, row.Message, [row.Email_Id])

            log_box.write("Sent Messsage to Everyone")

def form_page(form_id, data):

    if "valid" not in st.session_state:
        st.session_state.valid = validate_form(form_id)

    if not st.session_state.valid:
        st.error("Your form has already been submitted. Thank you!")
        return

    interview_duration = int(data['duration'].split()[0])

    # Interviewer Name
    interviewer_name = st.text_input("Interviewer Name", value=data['name'])

    parsed_date = datetime.strptime(data['date'], DATE_FORMAT)
    # Available Date
    available_date = st.date_input("Available Date", format="MM/DD/YYYY", value=parsed_date)

    # Number of Slots
    num_slots = st.number_input("Number of Available Slots", min_value=1, step=1)

    # Timeframe Inputs
    st.markdown("### Select the Timeframes")
    timeframes = []

    for i in range(num_slots):
        col1, col2 = st.columns(2)
        with col1:
            t = t = time(0, 0) if len(timeframes)==0 else timeframes[-1][1]
            start_time = st.time_input(f"Slot {i + 1} Start Time", key=f"start_{i}", value=t)
        with col2:
            end_time = st.time_input(f"Slot {i + 1} End Time", key=f"end_{i}", value=get_endtime(start_time, interview_duration))

        timeframes.append((start_time, end_time))

    # Additional Notes
    notes = st.text_area("Anything else you wish to convey?")

    # Submit Button
    if st.button("Submit Response"):
        # st.success("Form submitted successfully!")

        form_data = {
            "form_id": form_id,
            "name": interviewer_name,
            "date": available_date.strftime('%m/%d/%Y'),
            "slot_count": num_slots,
            "slots": timeframes,
            "notes": notes
        }

        if write_form_data(form_data):
            st.success("Form submitted successfully!")
        else:
            st.error("Error In Submitting Form.")

def main_app():
    query_params = st.query_params
    if "config" not in st.session_state:
        st.session_state.config = get_configs()

    if "form_id" in query_params:
        form_page(query_params.get("form_id", [None]), parse_data(query_params.get("form_id", [None])))
    else:

        if "authenticated" not in st.session_state:
            st.session_state.authenticated = False

        if not st.session_state.authenticated:
            st.subheader('Help me to Identify You...')
            password = st.text_input("Password", type="password")

            if st.button("Authenticate"):
                if check_password(password):
                    st.session_state.authenticated = True
                    st.rerun()

        if st.session_state.authenticated:
            home_page()

if __name__ == '__main__':
    main_app()
