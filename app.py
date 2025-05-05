from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# SMS API configuration
API_URL = "http://bulksmsbd.net/api/smsapi"
API_KEY = "t6qElhvPR1nyZ8prIC0C"
SENDER_ID = "8809617625650"

@app.route("/", methods=["GET", "POST"])
def index():
    status = None
    if request.method == "POST":
        location = request.form.get("location")
        number = "+8801725692402,+8801324436107,+8801332549219,+8801777742732"
        message = f"Fire Alert at {location}!"

        payload = {
            "api_key": API_KEY,
            "senderid": SENDER_ID,
            "number": number,
            "message": message
        }

        try:
            response = requests.post(API_URL, data=payload, timeout=10)
            status = response.text
        except requests.exceptions.RequestException as e:
            status = f"Request failed: {e}"

    return render_template("index.html", status=status)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
