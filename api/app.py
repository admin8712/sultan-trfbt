from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT'])
def catch_all(path):
    # Mengambil data mentah (raw) yang dikirimkan oleh APK ke Vercel
    data = request.get_json(silent=True) or request.form.to_dict()
    
    # Menangkap teks asli hasil scan server OCR
    raw_nominal = str(data.get('nominal', '0'))
    raw_ref = str(data.get('ref_kode', ''))
    
    # Jika ref_kode kosong dari server, kita buatkan berdasarkan waktu agar tidak REF123
    if not raw_ref or raw_ref == "123":
        raw_ref = "REF" + datetime.now().strftime("%H%M%S")

    return jsonify({
        "status": "success",
        "nominal": raw_nominal,
        "admin": "0",
        "total": raw_nominal,
        "amount": raw_nominal.replace('.', '').replace(',', ''),
        "ref_kode": raw_ref,
        "user_type": "unlimited",
        "remaining_credits": 999999,
        "tanggal": datetime.now().strftime("%d-%m-%Y"),
        "waktu": datetime.now().strftime("%H:%M:%S")
    })

if __name__ == '__main__':
    app.run()
