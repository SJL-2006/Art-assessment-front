<!-- 学生端成绩曲线：大 SVG 折线图 + 成长分析 -->
<template>
  <div class="page">
    <!-- 大图 -->
    <section class="card">
      <div class="card-head">
        <h2 class="title-splash">音乐 · 美术 成绩曲线</h2>
        <div class="legend">
          <span class="lg-item"><i style="background:linear-gradient(90deg,#3f8ef7,#7b6cf0)"></i>音乐</span>
          <span class="lg-item"><i style="background:linear-gradient(90deg,#f2a03d,#f2709c)"></i>美术</span>
        </div>
      </div>

      <svg :viewBox="`0 0 ${svgW} ${svgH}`" class="chart">
        <defs>
          <linearGradient id="gMusic" x1="0" y1="0" x2="1" y2="0">
            <stop stop-color="#3f8ef7"/><stop offset="1" stop-color="#7b6cf0"/>
          </linearGradient>
          <linearGradient id="gArt" x1="0" y1="0" x2="1" y2="0">
            <stop stop-color="#f2a03d"/><stop offset="1" stop-color="#f2709c"/>
          </linearGradient>
          <linearGradient id="fillMusic" x1="0" y1="0" x2="0" y2="1">
            <stop stop-color="#3f8ef7" stop-opacity="0.25"/><stop offset="1" stop-color="#3f8ef7" stop-opacity="0"/>
          </linearGradient>
          <linearGradient id="fillArt" x1="0" y1="0" x2="0" y2="1">
            <stop stop-color="#f2a03d" stop-opacity="0.25"/><stop offset="1" stop-color="#f2a03d" stop-opacity="0"/>
          </linearGradient>
        </defs>

        <!-- 网格 -->
        <line v-for="i in 5" :key="'gy'+i" :x1="padL" :x2="padL + plotW" :y1="padT + (plotH/4)*(i-1)" :y2="padT + (plotH/4)*(i-1)" stroke="#eef1f6" stroke-dasharray="4,4"/>
        <line :x1="padL" :x2="padL + plotW" :y1="padT + plotH" :y2="padT + plotH" stroke="#dfe4ee"/>

        <!-- 填充面积 音乐 -->
        <path :d="buildArea(musicPts)" fill="url(#fillMusic)"/>
        <path :d="buildArea(artPts)" fill="url(#fillArt)"/>

        <!-- 线 -->
        <path :d="buildLine(musicPts)" fill="none" stroke="url(#gMusic)" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
        <path :d="buildLine(artPts)" fill="none" stroke="url(#gArt)" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>

        <!-- 圆点 -->
        <g v-for="(p, i) in musicPts" :key="'mc'+i">
          <circle :cx="p.x" :cy="p.y" r="6" fill="#fff" stroke="#3f8ef7" stroke-width="2.5"/>
        </g>
        <g v-for="(p, i) in artPts" :key="'ac'+i">
          <circle :cx="p.x" :cy="p.y" r="6" fill="#fff" stroke="#f2a03d" stroke-width="2.5"/>
        </g>

        <!-- Y 轴标签 -->
        <text v-for="(v, i) in yTicks" :key="'yt'+i" :x="padL - 12" :y="padT + (plotH/4)*i + 5" fill="#8a93a5" font-size="13" text-anchor="end">{{ v }}</text>
        <!-- X 轴标签 -->
        <text v-for="(m, i) in months" :key="m" :x="padL + (plotW/(months.length-1))*i" :y="svgH - 12" fill="#8a93a5" font-size="13" text-anchor="middle">{{ m }}月</text>
      </svg>
    </section>

    <!-- 成长分析 -->
    <section class="analysis">
      <div class="card ana-card music">
        <h3>🎵 音乐成长</h3>
        <div class="ana-row"><span>起点</span><b>{{ music.start }}</b></div>
        <div class="ana-row"><span>终点</span><b>{{ music.end }}</b></div>
        <div class="ana-row highlight"><span>提升</span><b>+{{ music.delta }}</b></div>
      </div>
      <div class="card ana-card art">
        <h3>🎨 美术成长</h3>
        <div class="ana-row"><span>起点</span><b>{{ art.start }}</b></div>
        <div class="ana-row"><span>终点</span><b>{{ art.end }}</b></div>
        <div class="ana-row highlight"><span>提升</span><b>+{{ art.delta }}</b></div>
      </div>
      <div class="card ana-card summary">
        <h3>💡 成长分析</h3>
        <p>你的音乐和美术成绩都在稳步提升，表现出持续的艺术兴趣与良好的学习能力。继续保持练习，你在两个领域都有很好的潜力！</p>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive } from 'vue'
import { api } from '../../api'

const curve = reactive({ music: [], art: [], months: [] })

onMounted(async () => {
  try {
    const res = await api.student.workspace()
    Object.assign(curve, res.curve || {})
  } catch {
    Object.assign(curve, {
      music: [78, 80, 82, 81, 85, 88, 92],
      art:   [72, 75, 77, 80, 83, 84, 85],
      months: ['03','04','05','06','07','08','09','10']
    })
  }
})

const svgW = 900, svgH = 340
const padL = 56, padR = 30, padT = 20, padB = 36
const plotW = svgW - padL - padR
const plotH = svgH - padT - padB
const yMin = 70, yMax = 100
const yTicks = [100, 92.5, 85, 77.5, 70]

const months = computed(() => curve.months || [])

function pts(values) {
  const n = values.length
  return values.map((v, i) => ({
    x: padL + (plotW / Math.max(n - 1, 1)) * i,
    y: padT + plotH - ((v - yMin) / (yMax - yMin)) * plotH
  }))
}
const musicPts = computed(() => pts(curve.music || []))
const artPts   = computed(() => pts(curve.art   || []))

function buildLine(points) {
  if (!points.length) return ''
  return points.map((p, i) => (i === 0 ? 'M' : 'L') + p.x + ' ' + p.y).join(' ')
}
function buildArea(points) {
  if (!points.length) return ''
  const first = points[0], last = points[points.length - 1]
  const path = points.map((p, i) => (i === 0 ? 'M' : 'L') + p.x + ' ' + p.y).join(' ')
  return path + ` L ${last.x} ${padT + plotH} L ${first.x} ${padT + plotH} Z`
}

const music = computed(() => {
  const m = curve.music || []
  return { start: m[0] ?? 0, end: m[m.length - 1] ?? 0, delta: Math.max(0, (m[m.length - 1] ?? 0) - (m[0] ?? 0)) }
})
const art = computed(() => {
  const a = curve.art || []
  return { start: a[0] ?? 0, end: a[a.length - 1] ?? 0, delta: Math.max(0, (a[a.length - 1] ?? 0) - (a[0] ?? 0)) }
})
</script>

<style scoped>
.page { display: flex; flex-direction: column; gap: 22px; }
.card-head { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; }
.legend { display: flex; gap: 18px; font-size: 13px; color: #556074; }
.lg-item { display: inline-flex; align-items: center; gap: 6px; }
.lg-item i { width: 24px; height: 3px; border-radius: 2px; }
.chart { width: 100%; height: auto; }

/* 分析 */
.analysis { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; }
.ana-card h3 { margin: 0 0 14px; font-size: 16px; color: #2b3445; }
.ana-row {
  display: flex; justify-content: space-between;
  padding: 8px 0; font-size: 14px; color: #556074;
  border-bottom: 1px dashed #eef1f6;
}
.ana-row b { font-size: 18px; color: #2b3445; }
.ana-row.highlight b { color: #2fbfa5; font-size: 22px; }
.ana-card.music { border-left: 4px solid #3f8ef7; background: linear-gradient(135deg, #f8fbff, #fff); }
.ana-card.art { border-left: 4px solid #f2a03d; background: linear-gradient(135deg, #fff9f0, #fff); }
.ana-card.summary { border-left: 4px solid #7b6cf0; background: linear-gradient(135deg, #faf7ff, #fff); }
.summary p { margin: 0; font-size: 14px; line-height: 1.9; color: #556074; }
</style>
