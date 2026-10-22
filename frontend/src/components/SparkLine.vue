<template>
  <svg :width="width" :height="height" viewBox="0 0 80 28" preserveAspectRatio="none" class="spark">
    <polyline :points="points" fill="none" :stroke="color" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" />
    <circle :cx="last.x" :cy="last.y" r="2.2" :fill="color" />
  </svg>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  values: { type: Array, default: () => [] },
  color: { type: String, default: '#1677ff' },
  width: { type: [Number, String], default: 80 },
  height: { type: [Number, String], default: 28 }
})

const last = computed(() => {
  const pts = coords.value
  return pts.length ? pts[pts.length - 1] : { x: 0, y: 0 }
})
const coords = computed(() => {
  const values = props.values
  if (!values.length) return []
  const min = Math.min(...values)
  const max = Math.max(...values)
  const span = max - min || 1
  return values.map((v, i) => ({
    x: values.length === 1 ? 40 : 3 + (i * 74) / (values.length - 1),
    y: 24 - ((v - min) / span) * 20
  }))
})
const points = computed(() => coords.value.map(p => `${p.x},${p.y}`).join(' '))
</script>

<style scoped>
.spark {
  display: block;
  overflow: visible;
}
</style>
