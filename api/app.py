from flask import Flask, jsonify, request
import re
from datetime import datetime

app = Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'HEAD'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'HEAD'])
def catch_all(path):
    # 1. UPGRADE TAMPILAN BERANDA (Ubah FREE ke PRO)
    if 'config.php' in path or request.method == 'HEAD':
        return jsonify({
            "status": "success",
            "device_id": "WD-9a3e30f84ede3662d2a99b59cbc1b335",
            "remaining_credits": 999999,
            "user_type": "pro",        # Kunci untuk mengubah label FREE di Beranda
            "show_promo": False,
            "admin_wa": "6285161442237",
            "is_clean_pro": 1,
            "subscription_until": "2099-12-31",
            "referral_code": "CBC1B335",
            "is_ref_changed": 1
        })

    # 2. LOGIKA SCAN STRUK (Dinamis sesuai hasil kamera)
    data = request.get_json(silent=True) or request.form.to_dict()
    raw_text = str(data.get('text', ''))
    
    # Ekstraksi angka murni dari struk (Contoh: Rp104.000 -> 104000)
    numbers = re.findall(r'\d+', raw_text.replace('.', '').replace(',', ''))
    price_val = numbers[0] if numbers else "0"

    # 3. RESPON IDENTIK SERVER PRO (Sync dengan APK)
    return jsonify({
        "status": "success",
        "nominal": str(price_val),
        "amount": str(price_val),
        "total": str(price_val),
        "admin": "0",
        "ref_kode": "REF" + datetime.now().strftime("%H%M%S"),
        "tanggal": datetime.now().strftime("%d-%m-%Y"),
        "waktu": datetime.now().strftime("%H:%M:%S"),
        "user_type": "pro"             # Memastikan status pro saat transaksi
    })

if __name__ == '__main__':
    app.run()
