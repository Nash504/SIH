## MongoDB setup

The API stores readings in the `sensor_readings` collection in the `sih` database.

### MongoDB Atlas

1. Create an account at [MongoDB Atlas](https://www.mongodb.com/atlas).
2. Create a free shared cluster and a database user.
3. In **Network Access**, add the IP address where the API will run.
4. Select **Connect > Drivers**, copy the Python connection string, and replace its password.
5. Set the connection variables before starting the API:

```powershell
$env:MONGODB_URI = "mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority"
$env:MONGODB_DATABASE = "sih"
uv sync
uv run fastapi dev app/main.py
```

For a local MongoDB server, use `mongodb://localhost:27017` (the default) and set only
`MONGODB_DATABASE` if needed. Do not commit credentials or a `.env` file containing them.

### SMS setup

The `POST /send-sms` endpoint uses Twilio. Set these variables before starting the API:

```powershell
$env:TWILIO_ACCOUNT_SID = "your-account-sid"
$env:TWILIO_AUTH_TOKEN = "your-auth-token"
$env:TWILIO_FROM_NUMBER = "+15551234567"
```

`TWILIO_FROM_NUMBER` must be a real Twilio phone number owned by your account,
not the example number above.

The request body must contain an E.164 phone number and message:

```json
{
	"phone_number": "+15558675309",
	"message": "Alert: check crops."
}
```

## Sending a reading

`POST /send` accepts JSON in this shape:

```json
{
	"b1": {"temp": 24.5, "humidity": 61.2},
	"b2": {"temp": 24.7, "humidity": 60.8},
	"b3": {"temp": 24.4, "humidity": 62.0},
	"timestamp": "2026-08-24T12:00:00Z",
	"sensor_id": "device-001"
}
```

For a quick database test, send `POST /send` with no request body. The API inserts
a dummy reading with `sensor_id` set to `dummy-sensor`, creating the
`sih.sensor_readings` collection in MongoDB if it does not already exist.
