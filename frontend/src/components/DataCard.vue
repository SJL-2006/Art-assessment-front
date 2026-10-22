<template>
  <div class="data-card">
    <div class="card-head">
      <h3 class="card-title">
        <span class="title-dot" :style="{ background: accent }"></span>
        {{ title }}
      </h3>
      <slot name="actions"></slot>
    </div>
    <div class="card-body">
      <slot />
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  accent: { type: String, default: '#4f9cf9' }
})
</script>

<style scoped>
.data-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 14px rgba(70,90,130,0.06);
  overflow: hidden;
}
.card-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid #f0f2f7;
}
.card-title {
  font-size: 15px;
  font-weight: 600;
  color: #1f2a44;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}
.title-dot {
  width: 4px; height: 16px;
  border-radius: 2px;
}
.card-body { padding: 20px; }
</style>
