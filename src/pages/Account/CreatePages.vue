<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-white">
    <div class="border p-10 w-[30rem] rounded shadow-md">
      <img src="/icons/logo3.png" class="mx-auto w-40 mb-6" />
      <p class="text-center text-base text-black mb-6">
        Sign up to see the products comparison
      </p>
      <CreateForm />
    </div>

    <div class="border w-[28rem] mt-6 py-5 text-center text-base font-medium rounded shadow">
  Already have an account?
  <RouterLink to="/login" class="text-k-main font-bold hover:underline">Log in</RouterLink>
</div>
  </div>
</template>

<script setup>
import CreateForm from '../../components/Account/CreateForm.vue'
</script>
