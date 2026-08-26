from models.sensor import SmsPayload


def send_sms(payload: SmsPayload):
    # Mock SMS sending for the prototype.
    # Later, this will call an actual SMS provider.

    print(f"SMS to {payload.phone_number}: {payload.message}")

    return {
        "message": "SMS sent successfully",
        "phone_number": payload.phone_number,
    }