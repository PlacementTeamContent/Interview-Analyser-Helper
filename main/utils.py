from pathlib import Path
import pandas as pd
from .sheet_connector import GoogleSheetsCRUD
import base64
import json
import streamlit as st
import datetime
from .form_validation import *
import hashlib


BASE_DIR = Path(__file__).parent.parent
DATE_FORMAT = "%m/%d/%Y"

def base64_encode(input_str: str) -> str:
    message_bytes = input_str.encode('utf-8')
    base64_bytes = base64.b64encode(input_str.encode('utf-8'))
    return base64_bytes.decode('utf-8')

def base64_decode(encoded_str: str) -> str:
    base64_bytes = encoded_str.encode('utf-8')
    message_bytes = base64.b64decode(base64_bytes)
    return message_bytes.decode('utf-8')

def parse_data(data):
    str = base64_decode(data)
    return json.loads(str)

def get_next_day_date():
    date = datetime.date.today() + datetime.timedelta(days=1)
    formated_date = date.strftime(DATE_FORMAT)
    return formated_date

def load_data():
    agent = GoogleSheetsCRUD( BASE_DIR / 'config' / 'google-client.json',
        f'{st.session_state.config.get("primary_sheet")}',
        f'{st.session_state.config.get("interviewer_data_sub_sheet")}'
    )

    return pd.DataFrame(agent.read_all_data())

def get_contact_list(df, names, date, domains, duration, template):

    mail_ids = []
    messages = []
    for name in names:
        try:
            mail_ids.append(f"{str(df[df['Full Name'] == name].iloc[0, 3])}")
            messages.append(get_message(template, name, date, domains, duration))
        except:
            mail_ids.append('')
            messages.append("Missing Contact Details")

    interviewers = list(zip(names, mail_ids, messages))

    return interviewers

def get_interviewers(df):
    return sorted(df['Full Name'].tolist())

def get_domains():
    domains = [
        "MERN",
        "Python",
        "Python+Java",
        "Domain Expert",
        "Java+SQL",
        "MERN+Node",
    ]

    return sorted(domains)

def get_new_form(data, temp=False):
    form_id = base64_encode(data)

    if not temp:
        add_form(form_id)

    return f"{st.session_state.config.get('base_url')}?form_id={form_id}"

def get_message(template, name='Ravi', date=get_next_day_date(), domains='python/java', duration='1 hour', temp=False):

    data = {
        'name':name,
        'date':date,
        'domains':domains,
        'duration':duration
    }

    message = template.format(
        name=name,
        date=date,
        domains=domains,
        form_link=get_new_form(json.dumps(data), temp),
        duration=duration
    )

    return message

def get_configs():
    with open(BASE_DIR / 'config' / 'config.json', 'r', encoding='utf-8') as f:
        file_content = json.loads(f.read())
        return file_content

def divider():
    st.markdown('---')

def write_form_data(form_data):

    agent = GoogleSheetsCRUD( BASE_DIR / 'config' / 'google-client.json',
        f'{st.session_state.config.get("primary_sheet")}',
        f'{st.session_state.config.get("form_response_sub_sheet")}'
    )

    rows = []
    for i in range(form_data.get("slot_count")):
        row = [form_data.get("name"), form_data.get("date")]
        row.append(form_data.get("slots")[i][0].strftime('%I:%M %p'))
        row.append(form_data.get("slots")[i][1].strftime('%I:%M %p'))
        row.append(form_data.get("notes"))
        rows.append(row)

    try:
        for row in rows:
            agent.append_to_sheet(row)

        remove_form(form_data.get("form_id"))

        return True
    except:
        return False

def sha256_hash(input_string):
    sha256 = hashlib.sha256()
    sha256.update(input_string.encode('utf-8'))
    return sha256.hexdigest()

def check_password(password):
    return sha256_hash(password) == get_configs().get("password")

