import { ref } from 'vue'

const toast = ref(null)

export function useToast() {
  const showToast = (message, type = 'info') => {
    toast.value = { message, type }
    setTimeout(() => {
      toast.value = null
    }, 3000)
  }

  return {
    toast,
    showToast,
  }
}
