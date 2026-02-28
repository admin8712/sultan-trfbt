from flask import Flask, jsonify, request
import re
from datetime import datetime

app = Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT'])
def catch_all(path):
    data = request.get_json(silent=True) or request.form.to_dict()
    
    # 1. MENGAMBIL TEKS MURNI DARI HASIL SCAN KAMERA
    raw_text = str(data.get('text', ''))
    
    # 2. LOGIKA EKSTRAKSI DINAMIS
    # Mencari semua pola angka (contoh: 5.000, 10,000, atau 15000)
    found_numbers = re.findall(r'(\d+(?:[\.,]\d{3})*)', raw_text)
    
    final_price = "0"
    if found_numbers:
        # Filter: Cari angka yang paling mungkin jadi harga (minimal 3 digit)
        valid_prices = [n.replace('.', '').replace(',', '') for n in found_numbers if len(n.replace('.', '').replace(',', '')) >= 3]
        
        if valid_prices:
            # Mengambil angka pertama yang terdeteksi kamera sebagai harga utama
            final_price = valid_prices[0]

    # 3. GENERATE REFERENSI UNIK (BERDASARKAN WAKTU)
    # Agar tidak REF123 terus-menerus
    ref_final = "REF" + datetime.now().strftime("%H%M%S")

    # 4. RESPON JSON SESUAI KEMAUAN SERVER ASLI
    return jsonify({
        "admin": "0",
        "amount": final_price,
        "nominal": final_price,
        "ref_kode": ref_final,
        "remaining_credits": 999999,
        "status": "success",
        "tanggal": datetime.now().strftime("%d-%m-%Y"),
        "total": final_price,
        "user_type": "unlimited",
        "waktu": datetime.now().strftime("%H:%M:%S")
    })

if __name__ == '__main__':
    app.run()
