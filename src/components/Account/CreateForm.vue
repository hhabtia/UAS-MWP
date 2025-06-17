<template>
  <form @submit.prevent="handleSubmit" class="flex flex-col gap-4">
    <input
      v-model="form.name"
      type="text"
      placeholder="Full Name"
      class="border rounded px-4 py-3 text-base text-gray-800 focus:outline-none focus:ring-2 focus:ring-k-main"
      required
    />
    <input
      v-model="form.username"
      type="text"
      placeholder="Username"
      class="border rounded px-4 py-3 text-base text-gray-800 focus:outline-none focus:ring-2 focus:ring-k-main"
      required
    />
    <input
  v-model="form.password"
  type="password"
  placeholder="Password"
  minlength="6"
  class="border rounded px-4 py-3 ..."
  required
/>


    <button
      type="submit"
      class="bg-k-main text-white py-3 rounded font-semibold text-base hover:opacity-90"
    >
      Sign up
    </button>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()

const form = ref({
  name: '',
  username: '',
  password: '',
})

const handleSubmit = async () => {
  try {
    const res = await axios.post('/api/register', form.value);


    if (res.status === 201) {
      router.push('/login');
    }
  } catch (error) {
    console.error('Signup error:', error);

    if (error.response) {
      // Error dari server Laravel (validasi, DB error, dll)
      console.log('Respon error:', error.response.data);
      alert('Signup failed: ' + (error.response.data.message || 'Validasi gagal.'));
    } else if (error.request) {
      // Gagal konek ke backend
      console.error('Tidak ada respon dari server:', error.request);
      alert('Signup gagal: tidak dapat terhubung ke server.');
    } else {
      // Error lain (sebelum request terkirim)
      console.error('Error saat setup request:', error.message);
      alert('Signup gagal: ' + error.message);
    }
  }
};

</script>
