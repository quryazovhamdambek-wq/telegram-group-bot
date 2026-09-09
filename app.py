import os
from flask import Flask, redirect

app = Flask(__name__)

# Render Environment Variables orqali beriladi.
# INVITE_LINK — Telegram kanal/guruhingizning rasmiy taklif havolasi.
INVITE_LINK = os.environ.get("INVITE_LINK", "")

@app.route("/")
def home():
    if INVITE_LINK:
        return redirect(INVITE_LINK, code=302)
    return (
        "Bot ishlayapti. INVITE_LINK environment variable ni kiriting.",
        200,
    )

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
