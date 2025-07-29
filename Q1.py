
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, redirect
import string
import random

app = Flask(__name__)

BASE_URL = "http://localhost:5000"
url_store = {}
DEFAULT_VALIDITY_MINUTES = 30
SHORTCODE_LENGTH = 6

def generate_shortcode():
    characters = string.ascii_letters + string.digits
    while True:
        shortcode = ''.join(random.choice(characters) for _ in range(SHORTCODE_LENGTH))
        if shortcode not in url_store:
            return shortcode

def is_valid_custom_shortcode(code):
    return code.isalnum()

@app.route("/shorturls", methods=["POST"])
def create_short_url():
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({"error": "pls provide url in request"}), 400

        long_url = data['url']
        shortcode = data.get('shortcode')

        if shortcode:
            if not is_valid_custom_shortcode(shortcode):
                return jsonify({"error": "custom shortcode must be alphanumeric"}), 400
            if shortcode in url_store:
                return jsonify({"error": "shortcode already taken"}), 409
        else:
            shortcode = generate_shortcode()

        validity_minutes = data.get('validity', DEFAULT_VALIDITY_MINUTES)
        try:
            validity_minutes = int(validity_minutes)
        except:
            return jsonify({"error": "validity must be an integer"}), 400

        expiry_time = datetime.now() + timedelta(minutes=validity_minutes)

        url_store[shortcode] = {
            "long_url": long_url,
            "expiry_time": expiry_time
        }

        shortlink = f"{BASE_URL}/{shortcode}"
        print(f"Created shortlink: {shortlink} for URL: {long_url}")

        return jsonify({
            "shortlink": shortlink,
            "expiry": expiry_time.isoformat()
        }), 201

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "server error"}), 500

@app.route("/<shortcode>", methods=["GET"])
def redirect_to_long_url(shortcode):
    record = url_store.get(shortcode)

    if not record:
        return jsonify({"error": "shortcode not found"}), 404

    if datetime.now() > record["expiry_time"]:
        del url_store[shortcode]
        print(f"Expired shortcode accessed: {shortcode}")
        return jsonify({"error": "This link expired"}), 410

    print(f"Redirecting {shortcode} to {record['long_url']}")
    return redirect(record["long_url"], code=302)




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)