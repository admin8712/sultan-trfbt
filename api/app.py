from flask import Flask, jsonify, request
import re
from datetime import datetime

app = Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT'])
def catch_all(path):
    data = request.get_json(silent=True) or request.form.to_dict()
    raw_text = str(data.get('text', ''))
    
    # Mencari angka murni, menghapus 'Rp', titik, dan koma
    # Logika baru: Mencari deretan angka yang panjangnya 3-7 digit
    numbers = re.findall(r'\d+', raw_text.replace('.', '').replace(',', ''))
    
    price_val = "0"
    if numbers:
        # Cari angka yang paling masuk akal sebagai nominal (di atas 100)
        valid_prices = [n for n in numbers if 100 <= int(n) <= 10000000]
        if valid_prices:
            price_val = valid_prices[0]

    # Ref Kode dinamis agar tidak REF123
    ref_final = "REF" + datetime.now().strftime("%H%M%S")

    return jsonify({
        "admin": "0",
        "amount": str(price_val),
        "nominal": str(price_val),
        "ref_kode": ref_final,
        "remaining_credits": 999999,
        "status": "success",
        "tanggal": datetime.now().strftime("%d-%m-%Y"),
        "total": str(price_val),
        "user_type": "unlimited",
        "waktu": datetime.now().strftime("%H:%M:%S")
    })

if __name__ == '__main__':
    app.run()
