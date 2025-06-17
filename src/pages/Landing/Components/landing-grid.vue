<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

interface Product {
  id: number
  nama_produk: string
  gambar: string
  brand: string
  harga: number
  nama: string
  link: string // ⬅️ tambahkan ini
}

const popularProducts = ref<Product[]>([])
const youMightAlsoLikeProducts = ref<Product[]>([])


// Fungsi acak isi array
function shuffle(array: any[]) {
  const shuffled = [...array]
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]]
  }
  return shuffled
}

const fetchProducts = async () => {
  try {
    const response = await axios.get('http://localhost:5000/api/products/all')
    const products = response.data

    // ✅ Ini yang dipakai
    const validBrands = ['nike', 'adidas', 'converse']
    const shoeKeywords = ['sepatu', 'shoes', 'sneakers']
    const filtered = products.filter((p: Product) => {
    const brand = p.brand?.toLowerCase() || ''
    const name = (p.nama_produk ?? '').toLowerCase() || ''
    return validBrands.includes(brand) && shoeKeywords.some((kw) => name.includes(kw))
})

    // Kelompokkan per brand
    const byBrand: Record<string, any[]> = {
      nike: [],
      adidas: [],
      converse: []
    }

    filtered.forEach((p: Product) => {
      const brand = p.brand?.toLowerCase()
      if (byBrand[brand]) {
        byBrand[brand].push(p)
      }
    })

    const combined = [
  ...shuffle(byBrand.nike),
  ...shuffle(byBrand.adidas),
  ...shuffle(byBrand.converse)
]
    const finalShuffled = shuffle(combined)
    
    popularProducts.value = finalShuffled.slice(0, 8)
    youMightAlsoLikeProducts.value = finalShuffled.slice(8, 16)
  } catch (error) {
    console.error('Failed to fetch products:', error)
  }
}

onMounted(() => {
  fetchProducts()
})
</script>

<template>
  <main class="bg-white text-black py-16 px-8 min-h-screen">
    <div class="max-w-6xl mx-auto">
      <!-- Popular Right Now -->
      <h2 class="text-2xl font-semibold mb-6">Popular Right Now</h2>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
        <div 
          v-for="product in popularProducts" 
          :key="product.id"
          class="bg-white rounded-xl shadow-lg p-6 flex flex-col justify-between text-center hover:shadow-xl transition min-h-[340px]"
        >
          <div>
            <div class="h-56 flex items-center justify-center rounded-md mb-4 p-4">
              <img 
                v-if="product.gambar" 
                :src="product.gambar" 
                :alt="product.nama" 
                class="h-40 object-contain"
              />
              <div v-else class="text-gray-400">No Image</div>
            </div>
            <h3 class="text-lg font-semibold mb-1">{{ product.nama_produk }}</h3>
            <p class="text-gray-500 mb-4">{{ product.brand }}</p>
          </div>
          <a
  :href="product.link"
  target="_blank"
  class="inline-block mt-4 bg-k-main text-white px-4 py-2 rounded-lg font-semibold hover:bg-green-700 transition"
>
  Lihat Produk
</a>
        </div>
      </div>

      <!-- You Might Also Like -->
      <h2 class="text-2xl font-semibold mb-6 mt-16">You Might Also Like</h2>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
        <div 
          v-for="product in youMightAlsoLikeProducts" 
          :key="product.id"
          class="bg-white rounded-xl shadow-lg p-6 flex flex-col justify-between text-center hover:shadow-xl transition min-h-[340px]"
        >
          <div>
            <div class="h-56 flex items-center justify-center mb-4">
              <img 
                v-if="product.gambar" 
                :src="product.gambar" 
                :alt="product.nama_produk" 
                class="h-40 object-contain"
              />
              <div v-else class="text-gray-400">No Image</div>
            </div>
            <h3 class="text-lg font-semibold mb-1">{{ product.nama_produk }}</h3>
            <p class="text-gray-500 mb-4">{{ product.brand }}</p>
          </div>
          <a
  :href="product.link"
  target="_blank"
  class="inline-block mt-4 bg-k-main text-white px-4 py-2 rounded-lg font-semibold hover:bg-green-700 transition"
>
  Lihat Produk
</a>
        </div>
      </div>
    </div>
  </main>
</template>
