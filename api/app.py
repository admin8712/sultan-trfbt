from flask import Flask, jsonify, request
import re
from datetime import datetime

app = Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'HEAD', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'HEAD', 'OPTIONS'])
def catch_all(path):
    # 1. BYPASS OTP KIRIM
    if 'send_otp.php' in path:
        return jsonify({
            "status": "success",
            "message": "Kode OTP simulasi telah dikirim ke WhatsApp"
        })

    # 2. BYPASS OTP VERIFIKASI (Input apa saja pasti sukses)
    if 'verify_otp.php' in path:
        return jsonify({
            "status": "success",
            "message": "WhatsApp berhasil diverifikasi! Akun Anda kini PRO."
        })

    # 3. RESPON CONFIG (Ubah FREE jadi PRO & Kuota 999999)
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
            "subscription_until": None,
            "wa_linked": True,
            "referral_code": "CBC1B335",
            "is_ref_changed": 1,
            "created_at": "2026-02-28 07:51:55"
        })

    # 4. LOGIKA SCAN DINAMIS (Anti Rp 0)
    data = request.get_json(silent=True) or request.form.to_dict()
    raw_text = str(data.get('text', ''))
    numbers = re.findall(r'\d+', raw_text.replace('.', '').replace(',', ''))
    price_val = numbers[0] if numbers else "0"

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
