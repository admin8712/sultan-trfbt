from flask import Flask, jsonify, request, make_response
import re
from datetime import datetime

app = Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'HEAD'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'HEAD'])
def catch_all(path):
    # 1. Menangani Request Config/Ping dari APK
    if 'config.php' in path or request.method == 'HEAD':
        return jsonify({
            "status": "success",
            "device_id": "WD-9a3e30f84ede3662d2a99b59cbc1b335",
            "remaining_credits": 999999,
            "show_promo": False,
            "admin_wa": "6285161442237",
            "min_version": 25,
            "is_clean_pro": 1,
            "user_type": "pro",
            "subscription_until": "2099-12-31",
            "wa_linked": True,
            "referral_code": "CBC1B335",
            "is_ref_changed": 1,
            "commission_balance": 0,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    # 2. Menangani Request Scan Transaksi
    data = request.get_json(silent=True) or request.form.to_dict()
    raw_text = str(data.get('text', ''))
    
    # Ekstraksi angka nominal secara dinamis dari struk (Contoh: 104000)
    numbers = re.findall(r'\d+', raw_text.replace('.', '').replace(',', ''))
    price_val = numbers[0] if numbers else "104000"

    # 3. Output JSON Identik dengan Server Pusat
    return jsonify({
        "status": "success",
        "nominal": str(price_val),
        "amount": str(price_val),
        "total": str(price_val),
        "admin": "0",
        "ref_kode": "REF" + datetime.now().strftime("%H%M%S"),
        "tanggal": datetime.now().strftime("%d-%m-%Y"),
        "waktu": datetime.now().strftime("%H:%M:%S"),
        "user_type": "pro",
        "remaining_credits": 999999
    })

if __name__ == '__main__':
    app.run()
