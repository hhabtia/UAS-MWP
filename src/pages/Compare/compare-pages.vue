<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import Navigation from '@/components/navigation-global.vue'
import Footer from '@/components/footer-global.vue'

interface Product {
  brand: string
  nama: string
  harga: string
  harga_diskon?: string 
  gambar: string
  link: string
  rating?: string
  material_atas?: string
  material_dalam?: string
  material_sol?: string
  pengikat?: string
  [key: string]: any
}

const route = useRoute()
const comparedProducts = ref<Product[]>([])

const fallbackDetails: Record<string, any> = {
  material_atas: '-',
  material_dalam: '-',
  material_sol: '-',
  pengikat: '-',
  rating: null
}

const parseCompareQuery = (data: unknown) => {
  if (typeof data === 'string') {
    try {
      const rawData = JSON.parse(decodeURIComponent(data))
      comparedProducts.value = rawData.map((item: Product) => {
        const filled = { ...item }
        for (const key in fallbackDetails) {
          if (!(key in filled)) {
            filled[key] = fallbackDetails[key]
          }
        }
        return filled
      })
    } catch (e) {
      console.error('Error parsing compare data:', e)
    }
  }
}

onMounted(() => {
  parseCompareQuery(route.query.compare)
})

watch(() => route.query.compare, (newVal) => {
  parseCompareQuery(newVal)
})
</script>

<template>
  <div class="min-h-screen flex flex-col bg-white text-black">
    <Navigation color="black" />

    <div class="px-6 py-10 max-w-7xl mx-auto">
      <h1 class="text-3xl font-bold mb-8">Perbandingan Produk</h1>

      <div v-if="comparedProducts.length >= 2">
        <!-- Product cards -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
          <div
            v-for="(p, i) in comparedProducts"
            :key="i"
            class="border rounded-lg p-6 h-[420px] flex flex-col justify-between text-center"
          >
            <!-- Atas -->
            <div>
              <h2 class="text-xl font-bold mb-1 truncate">{{ p.brand || 'Brand' }}</h2>
              <h3 class="text-lg mb-4 line-clamp-2">{{ p.nama }}</h3>
              <div class="flex justify-center mb-4">
                <img :src="p.gambar" class="h-32 w-auto object-contain" />
              </div>
            </div>

            <!-- Bawah -->
<div>
  <p class="text-green-600 font-bold text-lg mb-1">
  {{ p.harga_diskon ?? p.harga }}
</p>
  <a
    :href="p.link || '#'"
    target="_blank"
    class="text-blue-600 hover:underline block"
  >
    Lihat Produk
  </a>
  <div v-if="p.rating" class="flex justify-center items-center mt-2">
    <span class="text-yellow-500 mr-1">⭐</span>
    <span>{{ p.rating }}</span>
  </div>
</div>

          </div>
        </div>

        <!-- Tabel material -->
        <div class="border rounded-lg overflow-hidden mb-8">
          <table class="w-full">
            <thead class="bg-gray-100">
  <tr>
    <th class="text-left p-4 font-semibold">Material</th>
    <th
      v-for="(p, i) in comparedProducts"
      :key="'head-' + i"
      class="text-left p-4 font-semibold"
    >
      {{ p.brand }} – <span class="font-normal">{{ p.nama }}</span>
    </th>
  </tr>
</thead>

            <tbody>
              <tr class="border-t">
                <td class="p-4 font-medium">Atas</td>
                <td v-for="(p, i) in comparedProducts" :key="i" class="p-4">
                  {{ (p.material_atas || '-').replace(/^:\s*/, '') }}
                </td>
              </tr>
              <tr class="border-t">
                <td class="p-4 font-medium">Dalam</td>
                <td v-for="(p, i) in comparedProducts" :key="i" class="p-4">
                  {{ (p.material_dalam || '-').replace(/^:\s*/, '') }}
                </td>
              </tr>
              <tr class="border-t">
                <td class="p-4 font-medium">Sol</td>
                <td v-for="(p, i) in comparedProducts" :key="i" class="p-4">
                  {{ (p.material_sol || '-').replace(/^:\s*/, '') }}
                </td>
              </tr>
              <tr class="border-t">
                <td class="p-4 font-medium">Pengikat</td>
                <td v-for="(p, i) in comparedProducts" :key="i" class="p-4">
                  {{ (p.pengikat || '-').replace(/^:\s*/, '') }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Jika belum pilih 2 produk -->
      <div v-else class="text-center py-20">
        <p class="text-gray-500 text-lg">Pilih minimal 2 produk untuk dibandingkan</p>
        <button class="mt-4 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
          Cari Produk
        </button>
      </div>
    </div>

    <Footer />
  </div>
</template>
