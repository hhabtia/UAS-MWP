import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

# Ambil URL database dari .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Koneksi ke PostgreSQL
engine = create_engine(DATABASE_URL)

# Load semua file CSV yang ingin dimasukkan ke database
csv_files = {
    "zalora_nike": "scraping_hasil/zalora_nike.csv",
    "zalora_adidas": "scraping_hasil/zalora_adidas.csv",
    "zalora_converse": "scraping_hasil/zalora_converse.csv"
    # Tambah file lain kalau perlu
}

for table_name, file_path in csv_files.items():
    print(f"📥 Importing {file_path} into table '{table_name}'...")
    df = pd.read_csv(file_path)
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print(f"✅ Selesai memasukkan ke '{table_name}'")

print("✅ Semua file CSV berhasil dimasukkan ke database PostgreSQL.")
