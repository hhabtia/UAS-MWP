<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const query = route.query.q as string

interface Product {
  nama: string
  gambar: string
  harga: string
}

const products = ref<Product[]>([])

onMounted(async () => {
  if (query) {
    const res = await axios.get(`http://localhost:5000/api/products/search?q=${query}`)
    products.value = res.data
  }
})
</script>

<template>
  <div class="p-6">
    <h2 class="text-2xl font-bold mb-4">Search results for "{{ query }}"</h2>

    <div v-if="products.length === 0">No products found.</div>

    <div v-else class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div v-for="(product, index) in products" :key="index" class="border p-2 rounded">
        <img :src="product.gambar" class="w-full h-32 object-contain" />
        <div class="font-semibold">{{ product.nama }}</div>
        <div class="text-green-600">{{ product.harga }}</div>
      </div>
    </div>
  </div>
</template>
