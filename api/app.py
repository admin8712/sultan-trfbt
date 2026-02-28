from flask import Flask, jsonify, request
import re
from datetime import datetime

app = Flask(__name__)

# Jaring laba-laba: Menangkap SEMUA URL yang diminta APK
@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT'])
def catch_all(path):
    data = request.get_json(silent=True) or request.form.to_dict()
    raw_text = str(data.get('text', ''))
    prices = re.findall(r'(\d{1,3}(?:\.\d{3})*(?:,\d+)?|\d+)', raw_text)
    
    if prices:
        clean_prices = [int(p.replace('.', '').replace(',', '')) for p in prices if len(p) > 2]
        nominal_value = max(clean_prices) if clean_prices else 5800
    else:
        nominal_value = 5800

    # Payload super lengkap untuk menipu segala jenis variabel APK
    return jsonify({
        "status": "success",
        "message": "success",
        "nominal": "{:,}".format(nominal_value).replace(',', '.'),
        "amount": str(nominal_value),
        "user_type": "unlimited",
        "premium": True,
        "is_premium": True,
        "role": "vip",
        "status_akun": "Premium",
        "remaining_credits": 999999,
        "quota": "Unlimited",
        "tanggal": datetime.now().strftime("%d-%m-%Y")
    })

if __name__ == '__main__':
    app.run()
