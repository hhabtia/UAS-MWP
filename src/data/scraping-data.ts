import * as Papa from 'papaparse'

export interface ScrapedProduct {
  Brand: string
  "Nama Produk": string
  Harga: string
  "Harga Diskon"?: string
  "Diskon Persen"?: string
  Link: string
  Gambar: string
  "Material Atas"?: string
  "Material Dalam"?: string
  "Material Sol"?: string
  Pengikat?: string
  [key: string]: any  // untuk fleksibilitas tambahan
}

export async function getScrapedProductById(id: number): Promise<ScrapedProduct | null> {
  const response = await fetch('/scraping_hasil/zalora_nike.csv')
  const csvText = await response.text()

  return new Promise((resolve) => {
    Papa.parse<ScrapedProduct>(csvText, {
      header: true,
      skipEmptyLines: true,
      complete: (result) => {
        const product = result.data[id]
        console.log('✅ Produk hasil parsing:', product) // debug log
        resolve(product ?? null)
      }
    })
  })
}
