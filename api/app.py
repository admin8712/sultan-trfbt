from flask import Flask, jsonify, request
import re
from datetime import datetime

app = Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT'])
def catch_all(path):
    # Ambil data mentah dari APK
    data = request.get_json(silent=True) or request.form.to_dict()
    raw_text = str(data.get('text', ''))
    
    # Mencari Nominal Asli (Hanya jika ada di teks)
    price_match = re.search(r'(\d{1,3}(?:\.\d{3})*(?:,\d+)?|\d+)', raw_text)
    nominal_original = price_match.group(0) if price_match else "0"
    
    # Mencari Kode Referensi Asli (Mencari kata REF atau KODE)
    ref_match = re.search(r'(REF[:\s]*\w+|KODE[:\s]*\w+)', raw_text, re.IGNORECASE)
    ref_original = ref_match.group(0) if ref_match else "-"

    return jsonify({
        "status": "success",
        "nominal": nominal_original,
        "amount": nominal_original.replace('.', '').replace(',', ''),
        "ref_kode": ref_original,
        "user_type": "unlimited",
        "remaining_credits": 999999,
        "tanggal": datetime.now().strftime("%d-%m-%Y"),
        "waktu": datetime.now().strftime("%H:%M:%S")
    })

if __name__ == '__main__':
    app.run()
