<template>
  <div class="line-chart">
    <div v-if="series.length" class="legend">
      <span v-for="s in series" :key="s.name" class="legend-item">
        <i :style="{ background: s.color }" />{{ s.name }}
      </span>
    </div>
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
        >{{ formatValue(tick) }}</text>
      </g>
      <g v-for="s in series" :key="s.name">
        <path v-if="area" :d="areaPath(s.data)" :fill="s.color" opacity="0.06" />
        <polyline
          :points="linePoints(s.data)"
          fill="none"
          :stroke="s.color"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
        <circle
          v-for="(v, i) in s.data"
          :key="i"
          :cx="xOf(i, s.data.length)"
          :cy="yOf(v)"
          r="3.4"
          fill="#fff"
          :stroke="s.color"
          stroke-width="2"
        />
      </g>
      <g>
        <text
          v-for="(label, i) in labels"
          :key="label + i"
          :x="xOf(i, labels.length)"
          :y="height - 9"
          text-anchor="middle"
          class="axis-text"
        >{{ label }}</text>
      </g>
    </svg>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  labels: { type: Array, default: () => [] },
  series: { type: Array, default: () => [] },
  area: { type: Boolean, default: true },
  suffix: { type: String, default: '' }
})

const width = 600
const height = 240
const pad = { l: 42, r: 16, t: 12, b: 30 }

const allValues = computed(() => props.series.flatMap(s => s.data))
const hasData = computed(() => props.labels.length > 0 && allValues.value.length > 0)
const maxValue = computed(() => niceCeil(Math.max(...allValues.value, 1) * 1.02))
const ticks = computed(() => Array.from({ length: 5 }, (_, i) => Number(((maxValue.value / 4) * i).toFixed(1))))

function niceCeil(value) {
  const exp = Math.floor(Math.log10(value))
  const base = Math.pow(10, exp)
  const n = value / base
  const step =
    n <= 1 ? 1 : n <= 1.2 ? 1.2 : n <= 1.5 ? 1.5 : n <= 2 ? 2 : n <= 2.5 ? 2.5 : n <= 3 ? 3 : n <= 4 ? 4 : n <= 5 ? 5 : n <= 6 ? 6 : n <= 8 ? 8 : 10
  return step * base
}

function formatValue(v) {
  return `${Math.round(v)}${props.suffix}`
}
function xOf(i, count) {
  if (count <= 1) return (width - pad.l - pad.r) / 2 + pad.l
  return pad.l + (i * (width - pad.l - pad.r)) / (count - 1)
}
function yOf(v) {
  const h = height - pad.t - pad.b
  return pad.t + h - (v / maxValue.value) * h
}
function linePoints(data) {
  return data.map((v, i) => `${xOf(i, data.length)},${yOf(v)}`).join(' ')
}
function areaPath(data) {
  if (!data.length) return ''
  const bottom = height - pad.b
  const first = `${xOf(0, data.length)},${bottom}`
  const last = `${xOf(data.length - 1, data.length)},${bottom}`
  return `M${first} L${linePoints(data).split(' ').join(' L')} L${last} Z`
}
</script>

<style scoped>
.legend {
  display: flex;
  gap: 18px;
  margin-bottom: 6px;
}
.legend-item {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #4e5969;
}
.legend-item i {
  width: 8px;
  height: 8px;
  border-radius: 2px;
}
.chart-svg {
  display: block;
  width: 100%;
  height: auto;
}
.axis-text {
  font-size: 11px;
  fill: #86909c;
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
