import { defineStore } from 'pinia'
import { ref } from 'vue'

interface Product {
  brand: string
  nama: string
  harga: string
  harga_diskon?: string | null
  harga_asli?: string | null
  link: string
  gambar: string
}

export const useCompareStore = defineStore('compare', () => {
  const selectedProducts = ref<Product[]>([])
  const showComparison = ref(false)

  function toggleCompare(product: Product) {
    const index = selectedProducts.value.findIndex(p => p.nama === product.nama)
    if (index === -1) {
      if (selectedProducts.value.length >= 2) {
        alert('Maksimal 3 produk bisa dibandingkan.')
        return
      }
      selectedProducts.value.push(product)
    } else {
      selectedProducts.value.splice(index, 1)
    }

    showComparison.value = selectedProducts.value.length > 0
  }

  function removeProduct(product: Product) {
    selectedProducts.value = selectedProducts.value.filter(p => p.nama !== product.nama)
    if (selectedProducts.value.length === 0) {
      showComparison.value = false
    }
  }

  function resetCompare() {
    selectedProducts.value = []
    showComparison.value = false
  }

  return {
    selectedProducts,
    showComparison,
    toggleCompare,
    removeProduct,
    resetCompare,
  }
})
