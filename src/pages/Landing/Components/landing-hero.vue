<script lang="ts" setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const query = ref('')
const router = useRouter()

const onSearch = () => {
  if (!query.value.trim()) return
  router.push({ path: '/search', query: { q: query.value } })
}
const ArrowIcon = '/icons/next.png' // panah dari public/icons
</script>

<template>
  <section class="flex w-full flex-col items-center overflow-hidden rounded-b-md bg-k-black">
    <div
      class="relative mt-20 flex max-w-6xl flex-col text-center transition-transform duration-200 sm:w-4/5 md:grid md:w-11/12 md:grid-cols-2 md:text-start lg:w-4/5"
    >
      <div
        class="relative z-10 flex flex-col items-center justify-center pb-6 sm:ml-0 md:ml-10 md:items-start lg:ml-0"
      >
        <h1 class="relative mt-4 mb-6 text-5xl font-semibold text-white md:text-6xl">
          Easily Search, Easily Compare!<br />
        </h1>
        <p class="text-2xl mb-8 text-white">
          Compare prices of millions of products from thousands of shops quickly<br />
          and find the best deals on PricePeek.
        </p>

        <!-- Search bar -->
        <div class="w-full md:w-auto mb-20">
          <div
            class="flex items-center bg-white rounded-full px-6 h-14 shadow-md w-full max-w-2xl"
          >
            <!-- Magnifying glass icon -->
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="w-6 h-6 text-gray-400 mr-4"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M21 21l-4.35-4.35M10 18a8 8 0 100-16 8 8 0 000 16z"
              />
            </svg>

            <!-- Input -->
            <input
              v-model="query"
              @keyup.enter="onSearch"
              type="text"
              placeholder="What are you looking for today?"
              class="flex-1 bg-transparent focus:outline-none text-black text-lg"
            />

            <!-- Arrow Button -->
            <button
              @click="onSearch"
              class="ml-12 bg-k-main text-white rounded-full w-10 h-10 flex items-center justify-center"
            >
              <img :src="ArrowIcon" alt="Go" class="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>

      <div class="absolute bottom-0 z-0 aspect-auto w-full opacity-30 md:relative md:z-10 md:opacity-100">
        <img
          class="relative top-12 scale-[175%] md:top-20 md:scale-[175%] lg:top-12 lg:scale-150"
        />
      </div>
    </div>
  </section>
</template>
