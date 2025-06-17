import csv
import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Setup headless browser
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=options)

# URL produk adidas
base_url = "https://www.zalora.co.id/search?q=sepatu+converse"
results = []
page = 1
MAX_PRODUCTS = 100

while len(results) < MAX_PRODUCTS:
    print(f"🔄 Scraping page {page}...")

    driver.get(f"{base_url}&page={page}")
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    products = soup.select('a[data-test-id="productLink"]')

    if not products:
        print("⚠️ Tidak ada produk lagi.")
        break

    for product in products:
        if len(results) >= MAX_PRODUCTS:
            break

        try:
            brand_elem = product.select_one('h3[data-test-id="productBrandName"]')
            title_elem = product.select_one('h3[data-test-id="productTitle"]')

            # Coba ambil harga diskon dulu
            price_elem = product.select_one('div[data-test-id="productPrice"] span.font-bold')
            # Kalau tidak ada (produk tidak diskon), ambil originalPrice
            if not price_elem:
                price_elem = product.select_one('div[data-test-id="originalPrice"]')

            img_elem = product.select_one('img')

            brand = brand_elem.get_text(strip=True) if brand_elem else "-"
            title = title_elem.get_text(strip=True) if title_elem else "-"
            price = price_elem.get_text(strip=True) if price_elem else "-"
            img = img_elem.get('src') if img_elem else "-"
            link = product.get('href')
            if not link.startswith("http"):
                link = "https://www.zalora.co.id" + link

            results.append({
                "Brand": brand,
                "Nama Produk": title,
                "Harga": price,
                "Link": link,
                "Gambar": img,
            })
        except Exception as e:
            print("⚠️ Lewat produk error:", e)
            continue

    page += 1

driver.quit()

# Simpan ke CSV zalora_adidas.csv
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, "..", "scraping_hasil", "zalora_converse.csv")

with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Brand", "Nama Produk", "Harga", "Link", "Gambar"])
    writer.writeheader()
    writer.writerows(results)

print("✅ Data selesai disimpan")
