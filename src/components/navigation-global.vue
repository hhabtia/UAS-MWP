<script setup lang="ts">
import bookmarkIcon from '/icons/bookmark.png'
import { computed, ref, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

interface Product {
  nama: string
  gambar: string
  link: string
  harga?: string
  harga_diskon?: string
}

interface Props {
  color?: 'black' | 'transparent' | 'k-black'
}
const props = withDefaults(defineProps<Props>(), {
  color: 'transparent',
})
const style = computed(() => 'bg-' + props.color)

const hamburgerState = ref('hide')
function showHamburger() { hamburgerState.value = 'show' }
function hideHamburger() { hamburgerState.value = 'hide' }

const showSearchInput = ref(false)
const searchQuery = ref('')
function handleSearch() {
  console.log('Searching:', searchQuery.value)
}

const userName = ref('Guest')
const userId = ref<number | null>(null)
const isLoggedIn = computed(() => userName.value !== 'Guest')
const router = useRouter()

function updateUserName() {
  const storedUser = localStorage.getItem('user')
  if (storedUser) {
    try {
      const user = JSON.parse(storedUser)
      userName.value = user.name || 'Guest'
      userId.value = user.id || null
    } catch {
      userName.value = 'Guest'
      userId.value = null
    }
  } else {
    userName.value = 'Guest'
    userId.value = null
  }
}

// Bookmark
const showBookmarkPopup = ref(false)
const allProducts = ref<Product[]>([])
const bookmarkedProducts = ref<Product[]>([])

function loadBookmarks() {
  const data = localStorage.getItem('bookmarks')
  const user = userId.value

  if (data && user !== null) {
    const parsed = JSON.parse(data)
    const bookmarkedNames = parsed[user] || []
    bookmarkedProducts.value = allProducts.value.filter(p => bookmarkedNames.includes(p.nama))
  } else {
    bookmarkedProducts.value = []
  }
}

function toggleBookmarkPopup() {
  if (!isLoggedIn.value) return
  showBookmarkPopup.value = !showBookmarkPopup.value
  if (showBookmarkPopup.value) loadBookmarks()
}

function removeBookmark(product: Product) {
  const user = userId.value
  if (!user) return

  const allBookmarks = JSON.parse(localStorage.getItem('bookmarks') || '{}')
  const updated = (allBookmarks[user] || []).filter((nama: string) => nama !== product.nama)
  allBookmarks[user] = updated
  localStorage.setItem('bookmarks', JSON.stringify(allBookmarks))
  loadBookmarks()
  window.dispatchEvent(new StorageEvent('storage'))
}

// Compare
const compareList = ref<Product[]>(JSON.parse(localStorage.getItem('compareList') || '[]'))

function isInCompare(product: Product) {
  return compareList.value.some(p => p.link === product.link)
}

function toggleCompare(product: Product) {
  const exists = isInCompare(product)
  if (exists) {
    compareList.value = compareList.value.filter(p => p.link !== product.link)
  } else {
    compareList.value.push(product)
    localStorage.setItem('temp_compare', JSON.stringify(product))
    window.dispatchEvent(new Event('bookmark-add-to-compare'))
  }
  localStorage.setItem('compareList', JSON.stringify(compareList.value))
}

// ✅ Handler tunggal untuk event storage dan user login
function handleUserChange() {
  updateUserName()
  loadBookmarks()
}

onMounted(async () => {
  updateUserName()

  const cached = localStorage.getItem('cached_products')
  if (cached) {
    allProducts.value = JSON.parse(cached)
  } else {
    try {
      const res = await axios.get('http://localhost:5000/api/products/nike') // sesuaikan endpoint kalau perlu
      allProducts.value = res.data
      localStorage.setItem('cached_products', JSON.stringify(res.data))
    } catch (err) {
      console.error('Gagal load produk:', err)
    }
  }

  loadBookmarks()

  window.addEventListener('storage', handleUserChange)
  window.addEventListener('user-logged-in', handleUserChange)
  window.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  window.removeEventListener('storage', handleUserChange)
  window.removeEventListener('user-logged-in', handleUserChange)
  window.removeEventListener('click', handleClickOutside)
})

// Dropdown logic
const showCategoryDropdown = ref(false)
const showProfileDropdown = ref(false)

function toggleCategoryDropdown() {
  showCategoryDropdown.value = !showCategoryDropdown.value
  if (showCategoryDropdown.value) showProfileDropdown.value = false
}
function toggleProfileDropdown() {
  showProfileDropdown.value = !showProfileDropdown.value
  if (showProfileDropdown.value) showCategoryDropdown.value = false
}
function logout() {
  localStorage.removeItem('user')
  localStorage.removeItem('token')
  userName.value = 'Guest'
  userId.value = null
  showProfileDropdown.value = false
  router.push('/login')
}
function handleClickOutside(event: MouseEvent) {
  const target = event.target as HTMLElement
  if (!target.closest('.category-dropdown')) showCategoryDropdown.value = false
  if (!target.closest('.profile-dropdown')) showProfileDropdown.value = false
  if (!target.closest('.bookmark-popup') && !target.closest('.bookmark-button')) showBookmarkPopup.value = false
}
</script>

<template>
  <header id="navi" class="main-container flex flex-col w-screen items-center" :class="style">
    <div class="relative flex w-full max-w-6xl justify-between items-center border-b border-zinc-500 py-6 px-4 md:px-8 lg:px-12">
      <!-- HAMBURGER -->
      <button class="select-none lg:hidden" @click="showHamburger">
        <svg class="h-8 w-8 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
        </svg>
      </button>

      <!-- LOGO -->
      <router-link to="/" class="text-3xl font-extrabold text-k-main hover:scale-110 transition">PricePeek</router-link>

      <!-- NAVIGATION -->
      <nav class="hidden lg:flex gap-8 items-center text-white uppercase">
        <router-link to="/" class="hover:text-k-main">Home</router-link>
        <div class="relative category-dropdown" @click.stop="toggleCategoryDropdown">
          <span class="cursor-pointer hover:text-k-main">Categories</span>
          <div v-if="showCategoryDropdown" class="absolute top-full left-0 mt-2 bg-black border border-gray-700 rounded-md shadow-lg w-40 z-50">
            <router-link to="/scraped-products" class="block px-4 py-2 hover:bg-zinc-800">Nike</router-link>
            <router-link to="/adidas" class="block px-4 py-2 hover:bg-zinc-800">Adidas</router-link>
            <router-link to="/converse" class="block px-4 py-2 hover:bg-zinc-800">Converse</router-link>
          </div>
        </div>
        <router-link to="/about" class="hover:text-k-main">About Us</router-link>
        <router-link to="/contact" class="hover:text-k-main">Contact</router-link>
      </nav>

      <!-- RIGHT ICONS -->
      <div class="flex items-center gap-4">
        <!-- Search -->
        <div class="relative">
          <template v-if="showSearchInput">
            <input
              v-model="searchQuery"
              @blur="showSearchInput = false"
              @keyup.enter="handleSearch"
              type="text"
              placeholder="Search..."
              class="w-40 md:w-60 rounded-md border border-gray-500 bg-black px-2 py-1 text-white focus:outline-none focus:ring-2 focus:ring-k-main transition"
            />
          </template>
        </div>

        <!-- Bookmark -->
        <div class="relative bookmark-button">
          <img :src="bookmarkIcon" alt="Bookmark" class="w-11 h-11 cursor-pointer" @click="toggleBookmarkPopup" />
          <div
            v-if="showBookmarkPopup"
            class="bookmark-popup absolute right-0 top-14 bg-white text-black w-[380px] rounded-xl shadow-2xl border border-gray-300 z-50"
          >
            <div class="px-4 py-3 border-b font-semibold bg-k-main text-white rounded-t-xl">Bookmarks</div>
            <div class="max-h-64 overflow-y-auto p-4 space-y-3">
              <template v-if="bookmarkedProducts.length">
                <div v-for="(item, idx) in bookmarkedProducts" :key="idx" class="flex gap-3 items-center justify-between">
                  <div class="flex gap-3 items-center overflow-hidden w-full">
                    <img :src="item.gambar" class="w-12 h-12 rounded border object-cover" />
                    <div class="flex flex-col truncate w-[160px]">
                      <span class="font-semibold text-sm truncate">{{ item.nama }}</span>
                      <a :href="item.link" target="_blank" class="text-blue-500 text-xs underline">Lihat Produk</a>
                    </div>
                  </div>
                  <div class="flex items-center gap-2">
                    <button
                      class="bg-k-main hover:bg-k-dark text-white w-6 h-6 rounded-full flex items-center justify-center text-sm"
                      @click="toggleCompare(item)"
                      :title="isInCompare(item) ? 'Hapus dari compare' : 'Tambah ke compare'"
                    >
                      {{ isInCompare(item) ? '✓' : '+' }}
                    </button>
                    <button
                      class="text-red-500 text-sm"
                      @click="removeBookmark(item)"
                      title="Hapus bookmark"
                    >
                      🗑
                    </button>
                  </div>
                </div>
              </template>
              <p v-else class="text-gray-500 text-sm text-center">Belum ada bookmark.</p>
            </div>
          </div>
        </div>

        <!-- Profile -->
        <div class="relative profile-dropdown flex items-center gap-2 cursor-pointer" @click.stop="toggleProfileDropdown">
          <img src="/icons/next.png" alt="Profile" class="w-10 h-10 rounded-full border object-cover" />
          <span class="hidden md:inline text-white">{{ userName }}</span>
          <div v-if="showProfileDropdown" class="absolute top-12 right-0 bg-black border border-gray-700 rounded-md py-2 w-28 text-sm z-50">
            <button @click="logout" class="hover:bg-zinc-800 px-4 py-2 w-full text-left text-white">Logout</button>
          </div>
        </div>
      </div>
    </div>

    <!-- MOBILE NAV -->
    <transition>
      <nav v-if="hamburgerState === 'show'" class="absolute flex flex-col w-full bg-black p-6 text-sm font-semibold z-50 gap-2">
        <button @click="hideHamburger" class="text-white hover:text-k-main self-end mb-2">Close</button>
        <router-link to="/" class="text-white hover:text-k-main" @click="hideHamburger">Home</router-link>
        <span class="text-white">Categories</span>
        <router-link to="/scraped-products" class="ml-4 text-white hover:text-k-main" @click="hideHamburger">Nike</router-link>
        <router-link to="/adidas" class="ml-4 text-white hover:text-k-main" @click="hideHamburger">Adidas</router-link>
        <router-link to="/converse" class="ml-4 text-white hover:text-k-main" @click="hideHamburger">Converse</router-link>
        <router-link to="/about" class="text-white hover:text-k-main" @click="hideHamburger">About Us</router-link>
        <router-link to="/contact" class="text-white hover:text-k-main" @click="hideHamburger">Contact</router-link>
      </nav>
    </transition>
  </header>
</template>
