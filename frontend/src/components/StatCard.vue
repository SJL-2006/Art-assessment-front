<template>
  <div class="stat-card" :style="{ borderTopColor: accent }">
    <div class="stat-head">
      <div class="stat-icon" :style="{ background: accent + '1f', color: accent }">
        <component :is="icon" />
      </div>
      <div v-if="trend" class="stat-trend" :class="trend > 0 ? 'up' : 'down'">
        <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
          <path v-if="trend > 0" d="M6 15l6-6 6 6"/>
          <path v-else d="M6 9l6 6 6-6"/>
        </svg>
        {{ Math.abs(trend) }}%
      </div>
    </div>
    <div class="stat-value">{{ value }}</div>
    <div class="stat-label">{{ label }}</div>
    <div v-if="subLabel" class="stat-sub">{{ subLabel }}</div>
  </div>
</template>

<script setup>
import { computed, h } from 'vue'

const props = defineProps({
  label: String,
  value: [Number, String],
  trend: { type: Number, default: 0 },
  subLabel: String,
  accent: { type: String, default: '#4f9cf9' },
  icon: { type: [Object, Function], default: null }
})
</script>

<style scoped>
.stat-card {
  background: #fff;
  border-radius: 14px;
  padding: 20px 22px;
  border-top: 3px solid #4f9cf9;
  box-shadow: 0 2px 14px rgba(70,90,130,0.06);
  transition: transform 0.2s, box-shadow 0.2s;
}
.stat-card:hover { transform: translateY(-2px); box-shadow: 0 8px 22px rgba(70,90,130,0.1); }
.stat-head { display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px; }
.stat-icon {
  width: 40px; height: 40px;
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
}
.stat-trend {
  font-size: 12px;
  font-weight: 600;
  padding: 2px 7px;
  border-radius: 10px;
  display: inline-flex; align-items: center; gap: 2px;
}
.stat-trend.up { background: #e6f8ed; color: #16a34a; }
.stat-trend.down { background: #fdecee; color: #ef4444; }
.stat-value { font-size: 28px; font-weight: 700; color: #1f2a44; letter-spacing: 0.5px; }
.stat-label { font-size: 13px; color: #7a8494; margin-top: 4px; }
.stat-sub { font-size: 11px; color: #a8b0c0; margin-top: 2px; }
</style>
