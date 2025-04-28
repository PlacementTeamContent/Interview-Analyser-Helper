# Interview Analyser Helper

## Description

This project allows you to send custom invitation emails to a list of people, including unique form links. Once a recipient submits their form, it becomes invalid, ensuring one submission per person. The system uses Google Sheets to manage the list of recipients and track form submissions, and it integrates with an SMTP server to send the invitation emails.

## Features

- Generate unique form links for each recipient.
- Track active and invalid forms.
- Send personalized emails with custom messages and form links.
- Google Sheets integration for managing recipients and form submissions.
- Form submissions are tracked in Google Sheets, and invalid forms are automatically removed after submission.

## Technologies Used

- Python
- Streamlit
- Google Sheets API
- SMTP (for sending emails)

## Installation

### Prerequisites

Before running the app, ensure you have the following:

- **Python 3.x** installed on your machine.
- **Streamlit** installed. You can install it via pip:
  ```bash
  pip install streamlit
  ```

### Setting Up a Virtual Environment (Recommended)

It is highly recommended to use a virtual environment to isolate project dependencies.

1. Install `virtualenv` if you don't have it already:
   ```bash
   pip install virtualenv
   ```

2. Create a new virtual environment:
   ```bash
   virtualenv venv
   ```

3. Activate the virtual environment:

   - On Windows:
     ```bash
     .venv\Scriptsa\ctivate
     ```

   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. After activating the virtual environment, install the project dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Setting Up Google Sheets API

1. Create a Google Cloud project and enable the Google Sheets API.
2. Download the `google-client.json` file (Service Account credentials).
3. Place the `google-client.json` file in the `config/` directory of the project.
4. Set up the necessary environment variables in the `.env` file.

### Setting Up SMTP

1. Set up an email account (e.g., Gmail) and enable App Passwords.
2. In the `main/mail_sender.py` file, configure the following SMTP settings:
    - SMTP server (e.g., `smtp.gmail.com` for Gmail)
    - SMTP port (e.g., `587`)
    - Email and app password for the sender email account.

### Install Dependencies

Run the following command to install all required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

To run the app, navigate to the project directory and execute the following command:
```bash
streamlit run main/main.py
```

This will launch the Streamlit app in your browser.

### Google Sheets Integration

- The app reads the list of recipients from the Google Sheet and allows you to select individuals to send invitations.
- The app also logs form submissions in a separate sub-sheet.

### Sending Emails

- The app will send personalized emails with the unique form links and custom messages.
- Once a form is submitted, it will be marked as invalid and removed from the list of active forms.

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.