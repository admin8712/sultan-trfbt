from flask import Flask, jsonify, request
import re
from datetime import datetime

app = Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'HEAD'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'HEAD'])
def catch_all(path):
    # 1. RESPON CONFIG (WAJIB SAMA PERSIS DENGAN CANARY)
    if 'config.php' in path or request.method == 'HEAD':
        return jsonify({
            "status": "success",
            "device_id": "WD-9a3e30f84ede3662d2a99b59cbc1b335",
            "remaining_credits": 999999,
            "show_promo": False,
            "admin_wa": "6285161442237",
            "min_version": 25,
            "is_clean_pro": 0,
            "user_type": "pro",
            "subscription_until": None,
            "wa_linked": False,
            "whatsapp_number": None,
            "referral_code": "CBC1B335",
            "referred_by": None,
            "is_ref_changed": 0,
            "commission_balance": 0,
            "has_rated": 0,
            "bank_name": None,
            "bank_account": None,
            "bank_owner": None,
            "created_at": "2026-02-28 07:51:55"
        })

    # 2. LOGIKA SCAN (Ambil nominal murni dari struk)
    data = request.get_json(silent=True) or request.form.to_dict()
    raw_text = str(data.get('text', ''))
    
    # Mencari nominal struk DANA 104.000
    numbers = re.findall(r'\d+', raw_text.replace('.', '').replace(',', ''))
    price_val = numbers[0] if numbers else "0"

    # 3. RESPON HASIL SCAN (Agar tidak REF123 dan Rp 0)
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
