import requests
from flask import Flask, request, jsonify, redirect
app = Flask(__name__)

CLIENT_ID = "23PZW9"
CLIENT_SECRET = "18a0f5aaaf2111dfbc98cca8f14a116a"
REDIRECT_URI = "http://localhost:5000/callback"
TOKEN_URL = "https://api.fitbit.com/oauth2/token"
API_BASE_URL = "https://api.fitbit.com/1/user/-/"

TOKENS = {}

@app.route('/login')
def login():
    auth_url = (
        "https://www.fitbit.com/oauth2/authorize?"
        f"response_type=code&client_id={CLIENT_ID}&"
        f"redirect_uri={REDIRECT_URI}&scope=activity%20heartrate%20sleep"
    )
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get("code")
    if not code:
        return "Authorization failed.", 400
    
@app.route('/normalize-data', methods=['POST'])
def normalize_data():
    # Your logic to process the data
    return jsonify({"message": "Data normalized successfully"})
    data = {
        "client_id": CLIENT_ID,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
        "code": code,
    }
    headers = {"Authorization": f"Basic {CLIENT_ID}:{CLIENT_SECRET}"}
    response = requests.post(TOKEN_URL, data=data, headers=headers)
    if response.status_code == 200:
        TOKENS.update(response.json())
        return "Authorization successful! You can now fetch data."
    return "Authorization failed.", response.status_code

@app.route('/fetch-fitbit-data', methods=['GET'])
def fetch_fitbit_data():
    access_token = TOKENS.get("access_token")
    if not access_token:
        return jsonify({"error": "User not authenticated"}), 401
    
    headers = {"Authorization": f"Bearer {access_token}"}
    metrics = {}
    
    steps_response = requests.get(f"{API_BASE_URL}activities/steps/date/today/7d.json", headers=headers)
    if steps_response.status_code == 200:
        metrics["steps"] = steps_response.json()

    heart_response = requests.get(f"{API_BASE_URL}activities/heart/date/today/7d.json", headers=headers)
    if heart_response.status_code == 200:
        metrics["heart_rate"] = heart_response.json()

    sleep_response = requests.get(f"{API_BASE_URL}sleep/date/today/7d.json", headers=headers)
    if sleep_response.status_code == 200:
        metrics["sleep"] = sleep_response.json()

    return jsonify(metrics)

if __name__ == "__main__":
    app.run(debug=True)
