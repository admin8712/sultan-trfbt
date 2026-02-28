from flask import Flask, jsonify, request
import re
from datetime import datetime

app = Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT'])
def catch_all(path):
    data = request.get_json(silent=True) or request.form.to_dict()
    
    # Mencari nominal dari segala kemungkinan variabel
    res_nominal = data.get('nominal') or data.get('amount') or data.get('price')
    
    if not res_nominal:
        # Jika variabel di atas kosong, cari angka di dalam raw text
        raw_text = str(data.get('text', ''))
        prices = re.findall(r'(\d{1,3}(?:\.\d{3})*)', raw_text)
        if prices:
            clean_prices = [p for p in prices if len(p.replace('.', '')) >= 4]
            res_nominal = clean_prices[0] if clean_prices else "0"
        else:
            res_nominal = "0"

    # Referensi dinamis (Menghapus kutukan REF123)
    ref_unik = "REF" + datetime.now().strftime("%H%M%S")

    return jsonify({
        "status": "success",
        "nominal": str(res_nominal),
        "admin": "0",
        "total": str(res_nominal),
        "amount": str(res_nominal).replace('.', '').replace(',', ''),
        "ref_kode": ref_unik,
        "user_type": "unlimited",
        "remaining_credits": 999999,
        "tanggal": datetime.now().strftime("%d-%m-%Y"),
        "waktu": datetime.now().strftime("%H:%M:%S")
    })

if __name__ == '__main__':
    app.run()
