from flask import Flask, jsonify, request
import re
from datetime import datetime

app = Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT'])
def catch_all(path):
    # Mengambil data mentah yang dikirim oleh aplikasi
    data = request.get_json(silent=True) or request.form.to_dict()
    raw_text = str(data.get('text', ''))
    
    # Mencari angka harga secara murni dari hasil scan
    # Hanya mengambil angka tanpa titik/koma agar sesuai 'amount': '5000'
    found_numbers = re.findall(r'(\d+(?:[\.,]\d{3})*)', raw_text)
    
    if found_numbers:
        price_val = found_numbers[0].replace('.', '').replace(',', '')
    else:
        price_val = "0"

    # STRUKTUR JSON MURNI DARI SERVER ASLI
    # Urutan dan variabel disesuaikan dengan hasil 'print' Termux kamu
    return jsonify({
        "admin": "0",
        "amount": str(price_val),
        "nominal": str(price_val),
        "ref_kode": "REF" + datetime.now().strftime("%H%M%S"),
        "remaining_credits": 999999,
        "status": "success",
        "tanggal": datetime.now().strftime("%d-%m-%Y"),
        "total": str(price_val),
        "user_type": "unlimited",
        "waktu": datetime.now().strftime("%H:%M:%S")
    })

if __name__ == '__main__':
    app.run()
