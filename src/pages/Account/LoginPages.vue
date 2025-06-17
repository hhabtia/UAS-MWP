<template>
  <div class="bg-white text-gray-900 min-h-screen flex items-center justify-center">
    <div class="container mx-auto flex flex-col lg:flex-row w-full max-w-6xl">
      <!-- Left Side -->
      <div class="lg:w-1/2 flex items-center justify-center p-8">
        <img src="/icons/logo3.png" alt="X Logo" class="w-180 h-auto" />
      </div>

      <!-- Right Side -->
      <div class="lg:w-1/2 flex flex-col justify-center p-8 lg:p-16 max-w-xl mx-auto">
        <h2 class="text-5xl font-bold mb-2 text-black">Find the Best Prices</h2>
        <h2 class="text-3xl mb-8 text-black">Join to unlock the best deals</h2>

        <!-- Login Form -->
        <form class="space-y-4" @submit.prevent="handleSubmit">
          <div>
            <input 
              type="text" 
              v-model="username"
              placeholder="Username"
              class="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#5fc25f] focus:border-transparent"
              required
            >
          </div>
          <div>
            <input 
              type="password" 
              v-model="password"
              placeholder="Password"
              class="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#5fc25f] focus:border-transparent"
              required
            >
          </div>

          <!-- tambahkan ini untuk cek klik tombol login -->
<button 
  type="submit"
  class="w-full py-3 bg-k-main text-black font-bold rounded-full hover:bg-[#4db04d] transition"
>
  Login
</button>

          <p v-if="message" class="text-red-500 text-sm font-semibold">{{ message }}</p>
        </form>

        <!-- OR separator -->
        <div class="relative my-6">
  <div class="absolute inset-0 flex items-center pointer-events-none">
    <div class="w-full border-t border-[#5fc25f]"></div>
  </div>
  <div class="relative flex justify-center">
    <span class="px-2 bg-white text-[#5fc25f] font-bold">or</span>
  </div>
</div>


        <!-- Register Button -->
        <router-link
          to="/register"
          class="w-full py-3 bg-white text-[#5fc25f] font-bold rounded-full text-center border-2 border-[#5fc25f] hover:bg-gray-50 transition"
        >
          Create account
        </router-link>
        

        <!-- Terms -->
        <p class="text-xs text-black font-bold mt-8">
          By signing up, you agree to the
          <a href="#" class="text-[#5fc25f] hover:underline font-bold">Terms of Service</a> and
          <a href="#" class="text-[#5fc25f] hover:underline font-bold">Privacy Policy</a>, including
          <a href="#" class="text-[#5fc25f] hover:underline font-bold">Cookie Use</a>.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const username = ref('')
const password = ref('')
const message = ref('')

const handleSubmit = async () => {
  console.log('Submitting form...')

  try {
    console.log('Getting CSRF cookie...')
    await axios.get('http://127.0.0.1:8000/sanctum/csrf-cookie', {
      withCredentials: true
    })

    console.log('Sending login request...')
    const response = await axios.post('http://127.0.0.1:8000/api/login', {
      username: username.value.trim(),
      password: password.value.trim()
    }, {
      withCredentials: true
    })

    console.log('Login success:', response.data)

    if (response.status === 200 && response.data.user) {
      // 🔐 Simpan data login
      localStorage.setItem('user', JSON.stringify(response.data.user))
      localStorage.setItem('token', response.data.token)

      // 🔔 Trigger update navbar
      window.dispatchEvent(new Event('user-logged-in'))

      // ⏩ Arahkan ke halaman utama
      await router.push('/').catch(err => {
        console.error('Router push error:', err)
      })
    }

  } catch (error) {
    console.error('Login error:', error)
    if (error.response) {
      message.value = error.response.data.message || 'Login gagal: username/password salah'
    } else if (error.request) {
      message.value = 'Tidak bisa terhubung ke server.'
    } else {
      message.value = 'Terjadi kesalahan: ' + error.message
    }
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

body {
  font-family: 'Inter', sans-serif;
}
</style>
