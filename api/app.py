from flask import Flask, jsonify, request
import re
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home(): return "VERCEL_V60_ONLINE"

@app.route('/check_credits.php', methods=['GET', 'POST'])
def credits():
    return jsonify({"status": "success", "user_type": "unlimited", "remaining_credits": 999999})

@app.route('/scan/ocr.php', methods=['POST'])
def ocr():
    return jsonify({"status": "success", "nominal": "5.800", "amount": "5800", "tanggal": datetime.now().strftime("%d-%m-%Y")})

if __name__ == '__main__':
    app.run()
