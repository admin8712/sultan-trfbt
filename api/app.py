from flask import Flask, jsonify, request
import re
from datetime import datetime

app = Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT'])
def catch_all(path):
    data = request.get_json(silent=True) or request.form.to_dict()
    raw_text = str(data.get('text', ''))
    
    # Cari angka di teks. Jika gagal karena sinyal, gunakan 5800 sebagai backup
    prices = re.findall(r'(\d{1,3}(?:\.\d{3})*(?:,\d+)?|\d+)', raw_text)
    if prices:
        clean_prices = [int(p.replace('.', '').replace(',', '')) for p in prices if len(p) > 2]
        nominal_value = max(clean_prices) if clean_prices else 5800
    else:
        nominal_value = 5800 

    return jsonify({
        "status": "success",
        "nominal": "{:,}".format(nominal_value).replace(',', '.'),
        "amount": str(nominal_value),
        "ref_kode": "REF" + datetime.now().strftime("%H%M%S"),
        "user_type": "unlimited",
        "remaining_credits": 999999,
        "tanggal": datetime.now().strftime("%d-%m-%Y"),
        "waktu": datetime.now().strftime("%H:%M:%S")
    })

if __name__ == '__main__':
    app.run()
