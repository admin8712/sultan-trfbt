from flask import Flask, jsonify, request
import re
from datetime import datetime

app = Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT'])
def catch_all(path):
    data = request.get_json(silent=True) or request.form.to_dict()
    raw_text = str(data.get('text', ''))
    
    # 1. Mencari Angka Harga Asli dari Scan
    prices = re.findall(r'(\d{1,3}(?:\.\d{3})*(?:,\d+)?|\d+)', raw_text)
    if prices:
        clean_prices = [int(p.replace('.', '').replace(',', '')) for p in prices if len(p) > 2]
        final_nominal = max(clean_prices) if clean_prices else 0
    else:
        final_nominal = 0 

    # 2. Membuat Kode Referensi Unik (Berdasarkan Jam-Menit-Detik)
    # Contoh hasil: REF013522 (01:35:22)
    ref_unik = "REF" + datetime.now().strftime("%H%M%S")

    return jsonify({
        "status": "success",
        "nominal": "{:,}".format(final_nominal).replace(',', '.'),
        "admin": "0",
        "total": "{:,}".format(final_nominal).replace(',', '.'),
        "amount": str(final_nominal),
        "ref_kode": ref_unik,
        "user_type": "unlimited",
        "remaining_credits": 999999,
        "tanggal": datetime.now().strftime("%d-%m-%Y"),
        "waktu": datetime.now().strftime("%H:%M:%S")
    })

if __name__ == '__main__':
    app.run()
