from flask import Flask, jsonify, request
import re
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home(): return "VERCEL_V60_ULTRA_ONLINE"

# Jalur yang kamu suntikkan di MT Manager
@app.route('/admin/verify', methods=['GET', 'POST'])
@app.route('/check_credits.php', methods=['GET', 'POST']) # Tambahan jalur kuota
def verify():
    # Logika deteksi harga dinamis
    data = request.get_json(silent=True) or request.form.to_dict()
    raw_text = str(data.get('text', ''))
    prices = re.findall(r'(\d{1,3}(?:\.\d{3})*(?:,\d+)?|\d+)', raw_text)
    
    if prices:
        clean_prices = [int(p.replace('.', '').replace(',', '')) for p in prices if len(p) > 2]
        nominal_value = max(clean_prices) if clean_prices else 5800
    else:
        nominal_value = 5800

    # Respons lengkap agar status FREE hilang
    return jsonify({
        "status": "success",
        "nominal": "{:,}".format(nominal_value).replace(',', '.'),
        "amount": str(nominal_value),
        "user_type": "unlimited",
        "premium": True,
        "remaining_credits": 999999,
        "quota": "Unlimited",
        "tanggal": datetime.now().strftime("%d-%m-%Y")
    })

if __name__ == '__main__':
    app.run()
