<template>
  <form @submit.prevent="handleLogin" class="space-y-4 w-full max-w-md mx-auto">
    <input
      v-model.trim="username"
      type="text"
      placeholder="Username"
      class="w-full px-3 py-2 border border-gray-700 rounded-md"
      required
    />
    <input
      v-model.trim="password"
      type="password"
      placeholder="Password"
      class="w-full px-3 py-2 border border-gray-700 rounded-md"
      required
    />
    <button
      type="submit"
      class="w-full bg-black text-white py-2 px-6 rounded-md hover:bg-gray-900 transition"
    >
      Login
    </button>
    <p v-if="message" class="text-red-500 text-center">{{ message }}</p>
  </form>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'

// Pastikan axios kirim cookie ke backend
axios.defaults.withCredentials = true

// Form fields
const username = ref('')
const password = ref('')
const message = ref('')

// Emit event ke parent
const emit = defineEmits(['login-success'])

const handleLogin = async () => {
  message.value = ''

  try {
    // Ambil CSRF cookie dari Sanctum
    await axios.get('http://127.0.0.1:8000/sanctum/csrf-cookie')

    // Kirim kredensial login
    const res = await axios.post(
      'http://127.0.0.1:8000/api/login',
      {
        username: username.value,
        password: password.value
      }
    )

    // Jika berhasil login
    if (res.status === 200 && res.data.user && res.data.token) {
  localStorage.setItem('user', JSON.stringify(res.data.user))
  localStorage.setItem('token', res.data.token) // ← simpan token asli!

  emit('login-success')
  window.dispatchEvent(new Event('user-logged-in'))
}

  } catch (err: any) {
    if (err.response) {
      message.value = err.response.data.message || 'Login gagal: username/password salah'
    } else if (err.request) {
      message.value = 'Tidak bisa terhubung ke server.'
    } else {
      message.value = 'Terjadi kesalahan: ' + err.message
    }
  }
}
</script>
