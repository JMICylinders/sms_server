from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# SMS API Configuration
API_URL = "http://bulksmsbd.net/api/smsapi"
API_KEY = "t6qElhvPR1nyZ8prIC0C"
SENDER_ID = "8809617625650"
RECIPIENTS = "+8801725692402,+8801830495936,+8801332549210,+8801313055747,+8801777742647,+8801313055741,+8801796705822,+8801871261324,+8801775575197,+8801886911535,+8801610225951,+8801964959091,+8801787450043,+8801877526952,+8801314867227"

@app.route("/", methods=["GET", "POST"])
def index():
    status = None
    if request.method == "POST":
        if "predefined" in request.form:
            location = request.form.get("location")
            message = f"""⚠️ FIRE ALERT at {location}!\n\nEvacuate the area IMMEDIATELY.\nFollow the nearest emergency exit signs and report to the assembly point.\nDo NOT use elevators.\nStay calm and assist others if possible.\n\n🚨 Emergency Response Team: Take Immediate Action."""
        elif "custom" in request.form:
            message = request.form.get("custom_message")

        payload = {
            "api_key": API_KEY,
            "senderid": SENDER_ID,
            "number": RECIPIENTS,
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
