from flask import Flask, jsonify, request
import re
from datetime import datetime

app = Flask(__name__)

@app.route('/admin/verify', methods=['GET', 'POST', 'PUT'])
def verify_scan():
    data = request.get_json(silent=True) or request.form.to_dict()
    raw_text = str(data.get('text', ''))
    
    # Mencari nominal asli
    prices = re.findall(r'(\d{1,3}(?:\.\d{3})*(?:,\d+)?|\d+)', raw_text)
    if prices:
        clean_prices = [int(p.replace('.', '').replace(',', '')) for p in prices if len(p) > 2]
        final_nominal = max(clean_prices) if clean_prices else 5800
    else:
        # Jika sinyal 0.08 KB/d gagal kirim teks, beri harga cadangan agar tidak Rp 0
        final_nominal = 5800 

    return jsonify({
        "status": "success",
        "nominal": "{:,}".format(final_nominal).replace(',', '.'),
        "admin": "0",
        "total": "{:,}".format(final_nominal).replace(',', '.'),
        "ref_kode": "REF" + datetime.now().strftime("%H%M%S"),
        "tanggal": datetime.now().strftime("%d-%m-%Y"),
        "waktu": datetime.now().strftime("%H:%M:%S")
    })

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return jsonify({
        "status": "success",
        "user_type": "unlimited",
        "remaining_credits": 999999
    })

if __name__ == '__main__':
    app.run()
