import os

from twilio.rest import Client


class SmsConfigurationError(RuntimeError):
    pass


def send_sms(phone_number: str, message: str) -> str:
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_FROM_NUMBER") or os.getenv("TWILIO_PHONE_NUMBER")

    if not account_sid:
        raise SmsConfigurationError("TWILIO_ACCOUNT_SID is not configured")
    if not auth_token:
        raise SmsConfigurationError(
            "TWILIO_AUTH_TOKEN is not configured; TWILIO_CLIENT_SECRET alone is not enough"
        )
    if not from_number:
        raise SmsConfigurationError(
            "TWILIO_FROM_NUMBER or TWILIO_PHONE_NUMBER is not configured"
        )

    sms = Client(account_sid, auth_token).messages.create(
        body=message,
        from_=from_number,
        to=phone_number,
    )
    return sms.sid