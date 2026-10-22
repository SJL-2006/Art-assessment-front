<template>
  <div class="provincial-dashboard">
    <!-- 顶部统计 -->
    <div class="stat-row">
      <StatCard label="覆盖市州" :value="stats.cities" trend="5" accent="#4f9cf9" />
      <StatCard label="覆盖区县" :value="stats.districts" trend="8" accent="#a06ee8" />
      <StatCard label="参与学生" :value="stats.students.toLocaleString()" trend="12" accent="#2fbfa5" />
      <StatCard label="已发布测评" :value="stats.exams" trend="-3" accent="#f2709c" />
    </div>

    <div class="grid-2">
      <!-- 测评参与率 -->
      <DataCard title="各市州测评参与率" accent="#4f9cf9">
        <div class="bar-chart">
          <div v-for="item in cityRate" :key="item.name" class="bar-row">
            <span class="bar-label">{{ item.name }}</span>
            <div class="bar-track">
              <div class="bar-fill" :style="{ width: item.rate + '%', background: item.color }"></div>
            </div>
            <span class="bar-val">{{ item.rate }}%</span>
          </div>
        </div>
      </DataCard>

      <!-- 学科分布 -->
      <DataCard title="已发布测评学科分布" accent="#f2709c">
        <div class="pie-wrap">
          <svg viewBox="0 0 200 200" class="pie">
            <circle v-for="(s, i) in subjects" :key="i" cx="100" cy="100" r="70"
              :style="{ stroke: s.color, strokeDasharray: s.dasharray, strokeDashoffset: s.dashoffset, transform: s.transform }"
              fill="none" stroke-width="28" />
          </svg>
          <div class="pie-legend">
            <div v-for="s in subjects" :key="s.name" class="legend-item">
              <span class="legend-dot" :style="{ background: s.color }"></span>
              <span>{{ s.name }}</span>
              <span class="legend-val">{{ s.value }}</span>
            </div>
          </div>
        </div>
      </DataCard>
    </div>

    <!-- 最近动态 -->
    <DataCard title="最近发布的省级测评" accent="#a06ee8">
      <div class="recent-list">
        <div v-for="(item, i) in recentExams" :key="i" class="recent-item">
          <div class="recent-tag" :style="{ background: item.color + '1f', color: item.color }">{{ item.subject }}</div>
          <div class="recent-info">
            <div class="recent-title">{{ item.name }}</div>
            <div class="recent-meta">发布到 {{ item.scope }} · {{ item.time }}</div>
          </div>
          <div class="recent-status" :class="item.status === '已完成' ? 'ok' : 'run'">{{ item.status }}</div>
        </div>
      </div>
    </DataCard>
  </div>
</template>

<script setup>
import { reactive, computed } from 'vue'
import StatCard from '../../components/StatCard.vue'
import DataCard from '../../components/DataCard.vue'

const stats = reactive({
  cities: 14,
  districts: 125,
  students: 312480,
  exams: 48
})

const cityRate = [
  { name: '成都市', rate: 96, color: '#4f9cf9' },
  { name: '绵阳市', rate: 88, color: '#a06ee8' },
  { name: '德阳市', rate: 82, color: '#2fbfa5' },
  { name: '乐山市', rate: 78, color: '#f2709c' },
  { name: '宜宾市', rate: 74, color: '#f2b23e' },
  { name: '自贡市', rate: 69, color: '#8b7cf6' },
  { name: '广元市', rate: 62, color: '#2fbfa5' },
  { name: '其他市州', rate: 58, color: '#4f9cf9' }
]

const subjects = computed(() => {
  const data = [
    { name: '音乐', value: 22, color: '#a06ee8' },
    { name: '美术', value: 20, color: '#2fbfa5' },
    { name: '综合艺术', value: 6, color: '#f2709c' }
  ]
  let cumulative = 0
  const total = data.reduce((a, b) => a + b.value, 0)
  return data.map((s, i) => {
    const circumference = 2 * Math.PI * 70
    const dasharray = (s.value / total) * circumference
    const dashoffset = -cumulative
    const transform = `rotate(-90 100 100)`
    cumulative += dasharray
    return { ...s, dasharray, dashoffset: dashoffset + circumference * 0.25, transform }
  })
})

const recentExams = [
  { name: '2026秋季省级音乐统一测评（七年级）', subject: '音乐', scope: '14 市州 · 328 所学校', time: '10-20 14:32', status: '进行中', color: '#a06ee8' },
  { name: '2026秋季省级美术统一测评（八年级）', subject: '美术', scope: '14 市州 · 321 所学校', time: '10-18 09:15', status: '进行中', color: '#2fbfa5' },
  { name: '2026春季省级音乐测评（九年级）', subject: '音乐', scope: '14 市州 · 315 所学校', time: '04-22 10:00', status: '已完成', color: '#a06ee8' },
  { name: '2026春季省级美术测评（七年级）', subject: '美术', scope: '14 市州 · 310 所学校', time: '04-20 08:30', status: '已完成', color: '#2fbfa5' },
  { name: '2025秋季省级音乐与美术综合测评', subject: '综合', scope: '14 市州 · 302 所学校', time: '11-12 09:00', status: '已完成', color: '#f2709c' }
]
</script>

<style scoped>
.provincial-dashboard { display: flex; flex-direction: column; gap: 20px; }
.stat-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}
.grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}
@media (max-width: 1100px) {
  .stat-row { grid-template-columns: repeat(2, 1fr); }
  .grid-2 { grid-template-columns: 1fr; }
}

/* 条形图 */
.bar-chart { display: flex; flex-direction: column; gap: 14px; }
.bar-row { display: flex; align-items: center; gap: 12px; font-size: 13px; }
.bar-label { width: 80px; color: #6b7688; flex-shrink: 0; }
.bar-track { flex: 1; height: 10px; background: #f0f2f7; border-radius: 5px; overflow: hidden; }
.bar-fill { height: 100%; border-radius: 5px; transition: width 0.8s ease; }
.bar-val { width: 46px; text-align: right; color: #2b3445; font-weight: 600; }

/* 饼图 */
.pie-wrap { display: flex; align-items: center; gap: 24px; }
.pie { width: 180px; height: 180px; flex-shrink: 0; }
.pie-legend { display: flex; flex-direction: column; gap: 10px; flex: 1; }
.legend-item { display: flex; align-items: center; gap: 8px; font-size: 13px; color: #4a5568; }
.legend-item .legend-val { margin-left: auto; font-weight: 600; color: #2b3445; }
.legend-dot { width: 10px; height: 10px; border-radius: 3px; }

/* 动态列表 */
.recent-list { display: flex; flex-direction: column; gap: 14px; }
.recent-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 12px 14px;
  background: #fafbfe;
  border-radius: 10px;
}
.recent-tag {
  font-size: 11px;
  padding: 3px 10px;
  border-radius: 10px;
  font-weight: 600;
}
.recent-info { flex: 1; }
.recent-title { font-size: 13px; font-weight: 600; color: #2b3445; }
.recent-meta { font-size: 11px; color: #8a93a5; margin-top: 3px; }
.recent-status { font-size: 12px; font-weight: 600; }
.recent-status.ok { color: #16a34a; }
.recent-status.run { color: #2f6fe4; }
</style>
