from flask import Flask, jsonify, request
import re
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home(): return "VERCEL_V60_DYNAMIC_ONLINE"

@app.route('/admin/verify', methods=['GET', 'POST'])
def verify():
    # Mengambil data teks hasil scan dari APK
    data = request.get_json(silent=True) or request.form.to_dict()
    raw_text = str(data.get('text', ''))
    
    # Logika mencari angka nominal (Contoh: 15.000 atau 5000)
    prices = re.findall(r'(\d{1,3}(?:\.\d{3})*(?:,\d+)?|\d+)', raw_text)
    
    # Ambil angka terbesar yang ditemukan (biasanya Total Harga)
    if prices:
        # Membersihkan titik/koma untuk konversi ke angka murni
        clean_prices = [int(p.replace('.', '').replace(',', '')) for p in prices if len(p) > 2]
        nominal_value = max(clean_prices) if clean_prices else 5800
    else:
        nominal_value = 5800 # Fallback jika sinyal terlalu buruk untuk baca teks

    return jsonify({
        "status": "success",
        "nominal": "{:,}".format(nominal_value).replace(',', '.'),
        "amount": str(nominal_value),
        "user_type": "unlimited",
        "remaining_credits": 999999,
        "tanggal": datetime.now().strftime("%d-%m-%Y")
    })

if __name__ == '__main__':
    app.run()
