import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:yupiburger@localhost:5432/fix_scraping')

# Baca semua tabel
nike = pd.read_sql('SELECT * FROM zalora_nike', engine)
adidas = pd.read_sql('SELECT * FROM zalora_adidas', engine)
converse = pd.read_sql('SELECT * FROM zalora_converse', engine)

# Gabungkan jadi satu DataFrame
all_products = pd.concat([nike, adidas, converse], ignore_index=True)

# Simpan ke tabel baru bernama 'products'
all_products.to_sql('products', engine, if_exists='replace', index=False)

print("✅ Data berhasil digabungkan ke dalam tabel 'products'")