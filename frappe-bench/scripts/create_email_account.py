import os
import requests
from dotenv import load_dotenv

load_dotenv()

ERP_URL = os.getenv("ERP_URL")
API_KEY = os.getenv("ERP_API_KEY")
API_SECRET = os.getenv("ERP_API_SECRET")

email_account = {
    "doctype": "Email Account",
    "email_id": os.getenv("EMAIL_ID"),
    "password": os.getenv("EMAIL_PASSWORD"),
    "enable_outgoing": 1,
    "smtp_server": os.getenv("SMTP_SERVER"),
    "smtp_port": int(os.getenv("SMTP_PORT")),
    "use_tls": 1,
    "default_outgoing": 1,
    "awaiting_password": 0
}

headers = {
    "Authorization": f"token {API_KEY}:{API_SECRET}",
    "Content-Type": "application/json"
}

# --- 1. Create Email Account ---
endpoint = f"{ERP_URL}/api/resource/Email Account"
response = requests.post(endpoint, json=email_account, headers=headers)

if response.status_code == 200:
    print(" Email Account created successfully.")
else:
    print(" Could not create Email Account (might already exist).")
    print(response.text)

# --- 2. Send Test Email ---
send_endpoint = f"{ERP_URL}/api/method/frappe.core.doctype.communication.email.make"
test_email_data = {
    "recipients": "imamkhaleel2@gmail.com",
    "subject": "ERPNext Local API Email Test",
    "content": "<p>Hello from ERPNext local API </p>",
    "send_email": 1
}
send_response = requests.post(send_endpoint, json=test_email_data, headers=headers)

if send_response.status_code == 200:
    print(" Test email sent successfully!")
else:
    print(" Failed to send email:", send_response.status_code, send_response.text)
