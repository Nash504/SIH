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
uv run fastapi dev src/sih/main.py
```

For a local MongoDB server, use `mongodb://localhost:27017` (the default) and set only
`MONGODB_DATABASE` if needed. Do not commit credentials or a `.env` file containing them.

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
