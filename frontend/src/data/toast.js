import { reactive } from 'vue'

export const toasts = reactive([])
let seq = 0

export function toast(message, type = 'success') {
  const id = ++seq
  toasts.push({ id, message, type })
  setTimeout(() => {
    const index = toasts.findIndex(t => t.id === id)
    if (index > -1) toasts.splice(index, 1)
  }, 2800)
}
