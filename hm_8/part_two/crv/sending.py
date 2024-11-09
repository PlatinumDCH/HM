import time

def send_email(contact):
    print(f"Sending email to {contact.email}")
    time.sleep(1)
    # imitation send email
    print("Email sent successfully")

def send_email_stub(contact):
    print(f"Sending email to {contact.email}")
    time.sleep(1)
    # imitation send email
    return True

def send_sms_stub(contact):
    print(f"Sending SMS to {contact.phone_number}")
    time.sleep(1)
    # imitation send msg
    return True
