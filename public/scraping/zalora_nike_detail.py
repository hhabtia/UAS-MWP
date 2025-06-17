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
base_url = "https://www.zalora.co.id/search?q=sepatu+nike"
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

            brand = product.select_one('[data-test-id="productBrandName"]')
            if not brand:
                continue
            brand = brand.get_text(strip=True)

            if "nike" not in brand.lower():
                continue
            if "sepatu" not in nama_produk.lower() and "shoe" not in nama_produk.lower():
                continue

            harga_diskon_el = product.select_one('[data-test-id="productPrice"] span.font-bold')
            harga_asli_el = product.select_one('[data-test-id="originalPrice"]')
            diskon_el = product.select_one('[data-test-id="discountPercentage"]')

            harga_diskon = harga_diskon_el.get_text(strip=True) if harga_diskon_el else ""
            harga_asli = harga_asli_el.get_text(strip=True) if harga_asli_el else harga_diskon
            diskon_persen = diskon_el.get_text(strip=True) if diskon_el else ""

            href = product.get('href', '')
            link = "https://www.zalora.co.id" + href if href and not href.startswith('http') else href

            img_element = product.select_one('img')
            gambar = img_element.get('src') if img_element else "-"

            product_data = {
                "Brand": brand,
                "Nama Produk": nama_produk,
                "Harga Asli": harga_asli,
                "Harga Diskon": harga_diskon,
                "Diskon Persen": diskon_persen,
                "Link": link,
                "Gambar": gambar
            }

            if link and link != "-":
                specs = scrape_product_detail(link)
                product_data.update(specs)

            results.append(product_data)
            print(f"✅ Berhasil scrape: {product_data['Nama Produk']}")

        except Exception as e:
            print(f"⚠️ Gagal scrape produk: {e}")
            continue

    if len(results) >= MAX_PRODUCTS:
        break
    page += 1

driver.quit()

# Simpan hasil ke CSV
csv_path = os.path.join("public", "scraping_hasil", "zalora_nike_detail.csv")
os.makedirs(os.path.dirname(csv_path), exist_ok=True)

with open(csv_path, "w", newline="", encoding="utf-8") as f:
    fieldnames = [
        "Brand", "Nama Produk", "Harga Asli", "Harga Diskon", "Diskon Persen",
        "Link", "Gambar", "Material Atas", "Material Dalam", "Material Sol", "Pengikat"
    ]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)

print(f"✅ Data disimpan ke {csv_path}")
print(f"📦 Total produk: {len(results)}")
