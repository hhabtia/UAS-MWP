import csv
import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup browser
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=options)

def scrape_product_detail(url):
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    specs = {
        "Material Atas": "-",
        "Material Dalam": "-",
        "Material Sol": "-",
        "Pengikat": "-"
    }

    try:
        details_section = soup.find('div', string='Rincian')
        if details_section:
            ul = details_section.find_next('ul')
            if ul:
                for li in ul.find_all('li'):
                    label = li.find('span', class_='font-bold')
                    if label:
                        label_text = label.get_text(strip=True)
                        value = label.find_next('span')
                        value_text = value.get_text(strip=True) if value else "-"
                        
                        if "Material Atas" in label_text:
                            specs["Material Atas"] = value_text
                        elif "Material Bagian Dalam" in label_text:
                            specs["Material Dalam"] = value_text
                        elif "Material Sol" in label_text:
                            specs["Material Sol"] = value_text
                        elif "Pengikat" in label_text:
                            specs["Pengikat"] = value_text

    except Exception as e:
        print(f"⚠️ Gagal scrape detail produk: {e}")

    return specs

# Scraping utama
base_url = "https://www.zalora.co.id/search?q=sepatu+converse"
results = []
page = 1
MAX_PRODUCTS = 200

while True:
    print(f"🔄 Scraping page {page}...")

    driver.get(f"{base_url}&page={page}")
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test-id="productLink"]'))
        )
    except:
        print("⛔ Produk tidak ditemukan atau halaman habis.")
        break

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    products = soup.select('a[data-test-id="productLink"]')

    if not products:
        break

    for product in products:
        if len(results) >= MAX_PRODUCTS:
            break

        try:
            nama_produk = product.select_one('[data-test-id="productTitle"]')
            if not nama_produk:
                continue
            nama_produk = nama_produk.get_text(strip=True)
            nama_produk_lower = nama_produk.lower()

            brand = product.select_one('[data-test-id="productBrandName"]')
            if not brand:
                continue
            brand = brand.get_text(strip=True)

            # Filter brand
            if "converse" not in brand.lower():
                continue

            # Filter hanya sepatu
            keywords_sepatu = ["sepatu", "shoe", "sneaker", "low top", "high top", "mid top", "canvas", "slip-on", "chuck taylor"]
            exclude_keywords = ["lace", "sock", "kaus kaki", "sandal", "tas", "shoelace", "paket", "kaos"]

            if not any(k in nama_produk_lower for k in keywords_sepatu):
                print(f"❌ Dibuang (tidak ada kata sepatu): {nama_produk}")
                continue
            if any(k in nama_produk_lower for k in exclude_keywords):
                print(f"❌ Dibuang (mengandung kata bukan sepatu): {nama_produk}")
                continue

            # Get harga diskon dan harga asli
            harga_diskon_elem = product.select_one('[data-test-id="productPrice"] span.font-bold')
            harga_asli_elem = product.select_one('[data-test-id="originalPrice"]')
            diskon_persen_elem = product.select_one('[data-test-id="discountPercentage"]')

            harga_diskon = harga_diskon_elem.get_text(strip=True) if harga_diskon_elem else ""
            harga_asli = harga_asli_elem.get_text(strip=True) if harga_asli_elem else (harga_diskon or "-")
            diskon_persen = diskon_persen_elem.get_text(strip=True) if diskon_persen_elem else ""

            # Get product link
            href = product.get('href', '')
            link = "https://www.zalora.co.id" + href if href and not href.startswith('http') else href

            # Get image
            img_element = product.select_one('img')
            gambar = img_element.get('src') if img_element else "-"

            product_data = {
                "Brand": brand,
                "Nama Produk": nama_produk,
                "Harga": harga_asli,
                "Harga Diskon": harga_diskon,
                "Diskon Persen": diskon_persen,
                "Link": link,
                "Gambar": gambar
            }

            # Get detailed specs
            if link and link != "-":
                specs = scrape_product_detail(link)
                product_data.update(specs)

            results.append(product_data)
            print(f"✅ Diterima: {nama_produk}")

        except Exception as e:
            print(f"⚠️ Gagal scrape produk: {e}")
            continue

    if len(results) >= MAX_PRODUCTS:
        break
    page += 1

driver.quit()

# Simpan hasil ke CSV
csv_path = os.path.join("public", "scraping_hasil", "zalora_converse_detail.csv")
os.makedirs(os.path.dirname(csv_path), exist_ok=True)

with open(csv_path, "w", newline="", encoding="utf-8") as f:
    fieldnames = [
        "Brand", "Nama Produk", "Harga", "Harga Diskon", "Diskon Persen",
        "Link", "Gambar",
        "Material Atas", "Material Dalam", "Material Sol", "Pengikat"
    ]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)

print(f"✅ Data disimpan ke {csv_path}")
print(f"📦 Total produk: {len(results)}")
