<template>
  <div>
    <div class="stat-row">
      <StatCard label="试题总数" :value="stats.questionCount" trend="6" accent="#4f9cf9" />
      <StatCard label="已审核通过" :value="stats.auditPassed" trend="8" accent="#2fbfa5" />
      <StatCard label="待审核" :value="stats.pending" accent="#f2b23e" />
      <StatCard label="被使用次数" :value="stats.usedCount.toLocaleString()" trend="15" accent="#f2709c" />
    </div>

    <div class="grid-2">
      <DataCard title="按学科分布" accent="#2fbfa5">
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
              <span class="legend-val">{{ s.value }}题</span>
            </div>
          </div>
        </div>
      </DataCard>

      <DataCard title="按题型分布" accent="#a06ee8">
        <div class="bar-chart">
          <div v-for="t in typeData" :key="t.name" class="bar-row">
            <span class="bar-label">{{ t.name }}</span>
            <div class="bar-track"><div class="bar-fill" :style="{ width: t.pct + '%', background: t.color }"></div></div>
            <span class="bar-val">{{ t.count }}</span>
          </div>
        </div>
      </DataCard>
    </div>

    <div class="grid-2">
      <DataCard title="课程体系" accent="#4f9cf9">
        <div class="course-grid">
          <div v-for="c in courses" :key="c.name" class="course-item">
            <div class="course-icon" :style="{ background: c.color + '1f', color: c.color }">
              <svg v-if="c.icon === 'music'" viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/></svg>
              <svg v-else viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M12 3a9 9 0 1 0 0 18c1 0 1.8-.8 1.8-1.8 0-.5-.2-.9-.4-1.2-.3-.3-.4-.7-.4-1.1 0-1 .8-1.8 1.8-1.8h2A4.2 4.2 0 0 0 21 11c-.1-4.5-4-8-9-8Z"/></svg>
            </div>
            <div class="course-info">
              <div class="course-name">{{ c.name }}</div>
              <div class="course-meta">{{ c.chapters }} 章节 · {{ c.questions }} 题</div>
            </div>
          </div>
        </div>
      </DataCard>

      <DataCard title="最近上传/审核" accent="#f2709c">
        <div class="recent-list">
          <div v-for="(item, i) in recent" :key="i" class="recent-item">
            <div class="recent-tag" :class="item.type">{{ item.typeLabel }}</div>
            <div class="recent-info">
              <div class="recent-title">{{ item.title }}</div>
              <div class="recent-meta">{{ item.operator }} · {{ item.time }}</div>
            </div>
            <div class="recent-status" :class="item.status">{{ item.statusLabel }}</div>
          </div>
        </div>
      </DataCard>
    </div>
  </div>
</template>

<script setup>
import { reactive, computed } from 'vue'
import StatCard from '../../components/StatCard.vue'
import DataCard from '../../components/DataCard.vue'

const stats = reactive({ questionCount: 5862, auditPassed: 5420, pending: 186, usedCount: 12840 })

const subjects = computed(() => {
  const data = [
    { name: '音乐', value: 3240, color: '#a06ee8' },
    { name: '美术', value: 2622, color: '#2fbfa5' }
  ]
  let cumulative = 0
  const total = data.reduce((a, b) => a + b.value, 0)
  return data.map(s => {
    const circumference = 2 * Math.PI * 70
    const dasharray = (s.value / total) * circumference
    const dashoffset = -cumulative
    cumulative += dasharray
    return { ...s, dasharray, dashoffset: dashoffset + circumference * 0.25, transform: `rotate(-90 100 100)` }
  })
})

const typeData = [
  { name: '选择题', count: 2340, pct: 90, color: '#4f9cf9' },
  { name: '判断题', count: 1280, pct: 50, color: '#a06ee8' },
  { name: '填空题', count: 980, pct: 38, color: '#2fbfa5' },
  { name: '简答题', count: 720, pct: 28, color: '#f2709c' },
  { name: '创作题', count: 320, pct: 12, color: '#f2b23e' },
  { name: '其他', count: 222, pct: 9, color: '#8b7cf6' }
]

const courses = [
  { name: '初中音乐（人教版）', chapters: 36, questions: 1680, color: '#a06ee8', icon: 'music' },
  { name: '初中音乐（苏教版）', chapters: 32, questions: 1240, color: '#8b7cf6', icon: 'music' },
  { name: '初中美术（人教版）', chapters: 30, questions: 1420, color: '#2fbfa5', icon: 'art' },
  { name: '初中美术（岭南版）', chapters: 28, questions: 1202, color: '#4f9cf9', icon: 'art' },
  { name: '小学音乐（通用）', chapters: 48, questions: 720, color: '#a06ee8', icon: 'music' },
  { name: '小学美术（通用）', chapters: 42, questions: 600, color: '#2fbfa5', icon: 'art' }
]

const recent = [
  { type: 'audit', typeLabel: '审核', title: '音乐·七年级·听音识器·3道', operator: '题库管理员', time: '10-22 10:12', status: 'ok', statusLabel: '通过' },
  { type: 'upload', typeLabel: '上传', title: '美术·八年级·创作题·2道（含图片）', operator: '张老师', time: '10-22 09:55', status: 'wait', statusLabel: '待审核' },
  { type: 'audit', typeLabel: '审核', title: '音乐·九年级·简答·1道', operator: '题库管理员', time: '10-21 16:30', status: 'ok', statusLabel: '通过' },
  { type: 'upload', typeLabel: '上传', title: '音乐·七年级·音频资源·5个', operator: '李老师', time: '10-21 15:20', status: 'wait', statusLabel: '待审核' },
  { type: 'audit', typeLabel: '审核', title: '美术·七年级·判断题·10道', operator: '题库管理员', time: '10-21 11:08', status: 'reject', statusLabel: '驳回' }
]
</script>

<style scoped>
.stat-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 20px; }
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }
@media (max-width: 1100px) { .stat-row { grid-template-columns: repeat(2, 1fr); } .grid-2 { grid-template-columns: 1fr; } }

.pie-wrap { display: flex; align-items: center; gap: 24px; }
.pie { width: 180px; height: 180px; flex-shrink: 0; }
.pie-legend { display: flex; flex-direction: column; gap: 10px; flex: 1; }
.legend-item { display: flex; align-items: center; gap: 8px; font-size: 13px; color: #4a5568; }
.legend-item .legend-val { margin-left: auto; font-weight: 600; color: #2b3445; }
.legend-dot { width: 10px; height: 10px; border-radius: 3px; }

.bar-chart { display: flex; flex-direction: column; gap: 12px; }
.bar-row { display: flex; align-items: center; gap: 12px; font-size: 13px; }
.bar-label { width: 70px; color: #6b7688; }
.bar-track { flex: 1; height: 10px; background: #f0f2f7; border-radius: 5px; overflow: hidden; }
.bar-fill { height: 100%; border-radius: 5px; }
.bar-val { width: 40px; text-align: right; color: #2b3445; font-weight: 600; }

.course-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }
.course-item {
  display: flex; align-items: center; gap: 12px;
  padding: 12px; border-radius: 10px; background: #fafbfe;
}
.course-icon {
  width: 44px; height: 44px; border-radius: 10px;
  display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.course-name { font-size: 13px; font-weight: 600; color: #1f2a44; }
.course-meta { font-size: 11px; color: #8a93a5; margin-top: 3px; }

.recent-list { display: flex; flex-direction: column; gap: 10px; }
.recent-item {
  display: flex; align-items: center; gap: 12px;
  padding: 10px 12px; background: #fafbfe; border-radius: 8px;
}
.recent-tag { font-size: 11px; padding: 2px 9px; border-radius: 10px; font-weight: 600; }
.recent-tag.audit { background: #eef4ff; color: #2f6fe4; }
.recent-tag.upload { background: #fef3e2; color: #d97706; }
.recent-info { flex: 1; }
.recent-title { font-size: 13px; font-weight: 600; color: #2b3445; }
.recent-meta { font-size: 11px; color: #8a93a5; margin-top: 2px; }
.recent-status { font-size: 12px; font-weight: 600; }
.recent-status.ok { color: #16a34a; }
.recent-status.wait { color: #d97706; }
.recent-status.reject { color: #ef4444; }
</style>
