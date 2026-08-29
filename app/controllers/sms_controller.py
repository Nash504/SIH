import os

from dotenv import load_dotenv
from twilio.rest import Client

from models.sensor import SmsPayload


load_dotenv()


def send_sms(payload: SmsPayload):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_PHONE_NUMBER")

    if not all([account_sid, auth_token, from_number]):
        raise ValueError(
            "Twilio credentials are not configured. Set TWILIO_ACCOUNT_SID, "
            "TWILIO_AUTH_TOKEN, and TWILIO_PHONE_NUMBER in the environment."
        )

    client = Client(account_sid, auth_token)
    twilio_message = client.messages.create(
        body=payload.message,
        from_=from_number,
        to=payload.phone_number,
    )

    print(f"SMS sent to {payload.phone_number}: {payload.message}")

    return {
        "message": "SMS sent successfully",
        "phone_number": payload.phone_number,
        "twilio_sid": twilio_message.sid,
    }