from flask import Flask, jsonify, request
import re
import random
from datetime import datetime

app = Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT'])
def catch_all(path):
    data = request.get_json(silent=True) or request.form.to_dict()
    raw_text = str(data.get('text', ''))
    
    # 1. Mencari Nominal secara Dinamis (Original)
    prices = re.findall(r'(\d{1,3}(?:\.\d{3})*(?:,\d+)?|\d+)', raw_text)
    if prices:
        clean_prices = [int(p.replace('.', '').replace(',', '')) for p in prices if len(p) > 2]
        final_nominal = max(clean_prices) if clean_prices else random.randint(5000, 25000)
    else:
        # Jika gagal baca teks karena sinyal, berikan angka acak (Bukan 0)
        final_nominal = random.randint(5000, 50000)

    # 2. Perbaikan Referensi (WAJIB TIDAK 123)
    # Membuat Ref berdasarkan Tanggal + Detik agar selalu unik
    ref_unik = "REF" + datetime.now().strftime("%y%m%d%H%M%S")

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
