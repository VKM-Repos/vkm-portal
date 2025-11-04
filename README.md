# ERPNext Email Integration (Gmail + Local Instance)

A comprehensive guide for setting up bidirectional email integration in your local ERPNext environment using Gmail.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Gmail App Password Setup](#gmail-app-password-setup)
- [Outgoing Mail Configuration](#outgoing-mail-configuration)
- [Incoming Mail Configuration](#incoming-mail-configuration)
- [Enable Scheduler](#enable-scheduler)
- [User Guide](#user-guide)
- [API Usage](#api-usage)
- [Troubleshooting](#troubleshooting)
- [Summary](#summary)

---

## ⚙️ Prerequisites

Before you begin, ensure you have:

- ✅ A working local ERPNext instance (e.g., `mysite.local`)
- ✅ Administrator access to ERPNext
- ✅ A Gmail account with **2-Step Verification** enabled

---

## 🔐 Gmail App Password Setup

Gmail requires App Passwords for IMAP/SMTP access. Follow these steps:

1. Navigate to [Google Account Security Settings](https://myaccount.google.com/security)
2. Under **"Signing in to Google"**, enable **2-Step Verification**
3. Go to **App Passwords** and create a new one:
   - **App**: Mail
   - **Device**: Other → Enter "ERPNext"
4. **Copy the 16-character password** (you'll need this in ERPNext)

> ⚠️ **Important**: Save this password securely. You won't be able to view it again.

---

## ✉️ Outgoing Mail Configuration

Configure ERPNext to send emails through Gmail:

1. In ERPNext, go to: **Settings → Email Account → New**
2. Fill in the following details:

| Field | Value |
|-------|-------|
| **Email Id** | `yourname@gmail.com` |
| **Enable Outgoing** | ✅ Checked |
| **Service** | Gmail |
| **SMTP Server** | `smtp.gmail.com` |
| **SMTP Port** | `587` |
| **Use TLS** | ✅ Checked |
| **Username** | `yourname@gmail.com` |
| **Password** | *Your 16-character App Password* |

3. Click **Save**
4. Click **"Send Test Email"** to verify the configuration

✅ If successful, you'll see: **"Email Sent Successfully"**

---

## 📥 Incoming Mail Configuration

Configure ERPNext to receive emails from Gmail:

1. In the same or a new **Email Account**, configure:

| Field | Value |
|-------|-------|
| **Email Id** | `yourname@gmail.com` |
| **Enable Incoming** | ✅ Checked |
| **Use IMAP** | ✅ Checked |
| **Service** | Gmail |
| **Incoming Server** | `imap.gmail.com` |
| **Incoming Port** | `993` |
| **Use SSL** | ✅ Checked |
| **Username** | `yourname@gmail.com` |
| **Password** | *Your 16-character App Password* |

2. Click **Save**
3. Click **"Test Connection"** to verify

### Auto-Create Support Tickets

To automatically create support tickets from incoming emails:
- Under **"Append To"**, select **Issue**

---

## 🔄 Enable Scheduler

ERPNext uses a background scheduler to automatically fetch incoming emails.

Run these commands in your bench directory:

```bash
cd frappe-bench
bench --site mysite.local enable-scheduler
bench restart
```

### Manual Email Fetch (for testing)

```bash
bench execute frappe.email.doctype.email_account.email_account.pull
```

---

## 🧠 User Guide

### ✅ Sending Emails

Users can send emails in three ways:

#### Option 1: From a Document
1. Open any record (e.g., Quotation, Invoice, Customer)
2. Click **Email** button
3. Fill in recipient and message
4. Click **Send**

#### Option 2: From Communication
1. Navigate to **Email → Communication → New**
2. Compose your email
3. Click **Send**

#### Option 3: Automatic Emails
Administrators can configure:
- **Email Alerts** for automated notifications
- **Auto Email Reports** for scheduled reports (e.g., overdue invoice reminders)

### 📬 Receiving Emails

Once IMAP is configured:

- Incoming messages appear in **Email → Communication**
- ERPNext automatically links emails to related records (Customer, Lead, Issue, etc.)
- If "Append To = Issue" is set, a new **Issue** document is created for each email
- Replies are tracked in conversation threads under the document **Timeline**

---

## 🧩 API Usage (Optional)

### Python (Frappe Script)

Create a custom script in your `frappe-bench` directory:

```python
import frappe

frappe.sendmail(
    recipients=["user@example.com"],
    sender="admin@example.com",
    subject="ERPNext Local API Email Test",
    message="Hello from ERPNext local API"
)
```

### REST API

```bash
curl -X POST http://mysite.local:8000/api/method/frappe.core.doctype.communication.email.make \
  -H "Authorization: token <API_KEY>:<API_SECRET>" \
  -H "Content-Type: application/json" \
  -d '{
    "recipients": "user@example.com",
    "subject": "ERP Email Test",
    "content": "Hello from REST API"
  }'
```

---

## 🧰 Troubleshooting

| Problem | Solution |
|---------|----------|
| **Emails not received** | Run: `bench execute frappe.email.doctype.email_account.email_account.pull` |
| **IMAP authentication failed** | Verify you're using the Gmail App Password, not your regular password |
| **Nothing in Email Queue** | Check **Email Queue** in ERPNext and ensure scheduler is running |
| **Emails stuck in queue** | Run: `bench enqueue --site mysite.local sendmail` |
| **Still not working?** | Check `frappe-bench/logs/worker.error.log` for detailed errors |

### Additional Debug Commands

```bash
# Check scheduler status
bench --site mysite.local scheduler status

# View email queue
bench --site mysite.local console
>>> frappe.get_all("Email Queue", filters={"status": "Not Sent"})

# Check background jobs
bench --site mysite.local console
>>> frappe.get_all("RQ Job")
```

---

## 🚀 Summary

- ✅ **Outgoing (SMTP)** → Send emails via Gmail
- ✅ **Incoming (IMAP)** → Fetch and link emails to records automatically
- 🔁 **Scheduler** → Keeps email sync automated
- 🧠 **User-Friendly** → Send/reply directly in ERPNext (no coding required)
- 🔧 **Developer-Ready** → Full API support for custom integrations

---

## 📚 Additional Resources

- [ERPNext Documentation](https://docs.erpnext.com/)
- [Frappe Framework Email API](https://frappeframework.com/docs/user/en/api/email)
- [Gmail SMTP Settings](https://support.google.com/mail/answer/7126229)

---

## 📝 License

This documentation is provided as-is for ERPNext users and developers.

---

**Questions or Issues?** Open an issue in this repository or consult the [ERPNext Community Forum](https://discuss.erpnext.com/).
