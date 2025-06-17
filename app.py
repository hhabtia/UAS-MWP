from flask import Flask, jsonify 
from flask_cors import CORS
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# ✅ Pastikan .env dibaca dari lokasi yang benar
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)

# 🔍 Debug: tampilkan DATABASE_URL untuk memastikan benar
print("🔍 DATABASE_URL:", os.getenv("DATABASE_URL"))

app = Flask(__name__)
CORS(app,
     supports_credentials=True,
     resources={r"/api/*": {"origins": "http://127.0.0.1:5173"}})

# Ambil koneksi dari .env
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

@app.route("/api/products/<brand>")
def get_products(brand):
    table_map = {
        "nike": "zalora_nike",
        "adidas": "zalora_adidas",
        "converse": "zalora_converse"
        # Tambah brand lain jika perlu
    }

    table = table_map.get(brand.lower())
    if not table:
        return jsonify({"error": "Brand tidak ditemukan"}), 404

    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT * FROM {table} LIMIT 200"))
        products = [dict(row._mapping) for row in result]

        # 🔍 Tampilkan contoh 1 baris data dari database untuk debug
        if products:
            print("🧪 Contoh data:", products[0])

    return jsonify(products)

@app.route("/api/products/all")
def get_all_products():
    table_names = ["zalora_nike", "zalora_adidas", "zalora_converse"]
    all_products = []

    with engine.connect() as conn:
        for table in table_names:
            result = conn.execute(text(f"SELECT * FROM {table} LIMIT 200"))
            rows = [dict(row._mapping) for row in result]
            all_products.extend(rows)

    return jsonify(all_products)

if __name__ == "__main__":
    app.run(debug=True)
