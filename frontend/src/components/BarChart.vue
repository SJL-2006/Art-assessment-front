<template>
  <div class="bar-chart">
    <div v-if="!hasData" class="chart-empty">暂无数据</div>
    <svg v-else viewBox="0 0 600 240" class="chart-svg" preserveAspectRatio="xMidYMid meet">
      <g>
        <line
          v-for="(tick, i) in ticks"
          :key="'g' + i"
          :x1="pad.l"
          :x2="width - pad.r"
          :y1="yOf(tick)"
          :y2="yOf(tick)"
          stroke="#f0f0f0"
          stroke-width="1"
        />
        <text
          v-for="(tick, i) in ticks"
          :key="'t' + i"
          :x="pad.l - 8"
          :y="yOf(tick) + 4"
          text-anchor="end"
          class="axis-text"
        >{{ Math.round(tick) }}{{ suffix }}</text>
      </g>
      <g v-for="(value, i) in values" :key="i">
        <rect
          :x="barX(i) - barWidth / 2"
          :y="yOf(value)"
          :width="barWidth"
          :height="Math.max(2, height - pad.b - yOf(value))"
          rx="3"
          :fill="colorOf(i)"
          class="bar"
        />
        <text
          :x="barX(i)"
          :y="yOf(value) - 7"
          text-anchor="middle"
          class="value-text"
        >{{ format(value) }}</text>
        <text :x="barX(i)" :y="height - 9" text-anchor="middle" class="axis-text">{{ labels[i] }}</text>
      </g>
    </svg>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  labels: { type: Array, default: () => [] },
  values: { type: Array, default: () => [] },
  colors: { type: Array, default: () => ['#1677ff', '#91caff', '#13c2c2', '#52c41a', '#faad14'] },
  suffix: { type: String, default: '' },
  decimals: { type: Boolean, default: false }
})

const width = 600
const height = 240
const pad = { l: 42, r: 16, t: 22, b: 32 }

const hasData = computed(() => props.values.length > 0)
const maxValue = computed(() => niceCeil(Math.max(...props.values, 1) * 1.02))
const ticks = computed(() => Array.from({ length: 5 }, (_, i) => Number(((maxValue.value / 4) * i).toFixed(1))))

function niceCeil(value) {
  const exp = Math.floor(Math.log10(value))
  const base = Math.pow(10, exp)
  const n = value / base
  const step =
    n <= 1 ? 1 : n <= 1.2 ? 1.2 : n <= 1.5 ? 1.5 : n <= 2 ? 2 : n <= 2.5 ? 2.5 : n <= 3 ? 3 : n <= 4 ? 4 : n <= 5 ? 5 : n <= 6 ? 6 : n <= 8 ? 8 : 10
  return step * base
}
const slot = computed(() => (width - pad.l - pad.r) / Math.max(props.values.length, 1))
const barWidth = computed(() => Math.min(44, slot.value * 0.44))

function barX(i) {
  return pad.l + slot.value * i + slot.value / 2
}
function yOf(v) {
  const h = height - pad.t - pad.b
  return pad.t + h - (v / maxValue.value) * h
}
function colorOf(i) {
  return props.colors[i % props.colors.length]
}
function format(v) {
  return props.decimals ? v.toFixed(1) : Math.round(v)
}
</script>

<style scoped>
.chart-svg {
  display: block;
  width: 100%;
  height: auto;
}
.axis-text {
  font-size: 11px;
  fill: #86909c;
}
.value-text {
  font-size: 11.5px;
  font-weight: 500;
  fill: #4e5969;
}
.bar {
  transition: opacity 0.15s;
}
.bar:hover {
  opacity: 0.82;
}
.chart-empty {
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #9aa3b2;
  font-size: 13px;
}
</style>
