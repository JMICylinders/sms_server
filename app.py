from flask import Flask, render_template, request, session
import requests
import os

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersecretkey")  # required for session

# SMS API Configuration
API_URL = "http://bulksmsbd.net/api/smsapi"
API_KEY = os.getenv("SMS_API_KEY")
SENDER_ID = os.getenv("SENDER_ID")

# Assistant Drillers and their crew phone groups (placeholders)
ASSISTANT_DRILLERS = {
    "Kuddus": ["+8801725692402", ],
    "Folik": ["+8801569132204", ],
    "Rokon": ["+8801878287485",]
}

@app.route("/", methods=["GET", "POST"])
def index():
    status = None

    if request.method == "POST":
        # Check if this is predefined or custom
        if "predefined" in request.form:
            driller = request.form.get("driller")
            session['selected_driller'] = driller  # store selected driller in session
            recipients = ASSISTANT_DRILLERS.get(driller, [])
            numbers = ",".join(recipients)

            message = f"""⚠️ EMERGENCY ALERT for crew under Assistant Driller {driller}!\n\nEvacuate the area IMMEDIATELY.\nFollow the nearest emergency exit signs and report to the assembly point.\nDo NOT use elevators.\nStay calm and assist others if possible.\n\n🚨 Emergency Response Team: Take Immediate Action."""

        elif "custom" in request.form:
            driller = session.get('selected_driller')  # get driller from session
            if not driller:
                status = "⚠️ Please select an Assistant Driller first using the predefined message form."
                return render_template("index.html", status=status, drillers=list(ASSISTANT_DRILLERS.keys()))
            recipients = ASSISTANT_DRILLERS.get(driller, [])
            numbers = ",".join(recipients)
            message = request.form.get("custom_message")

        # Send SMS
        payload = {
            "api_key": API_KEY,
            "senderid": SENDER_ID,
            "number": numbers,
            "message": message
        }

        try:
            response = requests.post(API_URL, data=payload, timeout=10)
            if "SMS SUBMITTED" in response.text.upper():
                status = f"✅ SMS sent successfully to {driller}'s crew!"
            else:
                status = f"⚠️ SMS sending failed. Response: {response.text}"
        except requests.exceptions.RequestException as e:
            status = f"Request failed: {e}"

    return render_template("index.html", status=status, drillers=list(ASSISTANT_DRILLERS.keys()))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)


