<template>
  <div class="c-page">
    <section class="welcome">
      <div class="welcome-text">
        <p class="hello">{{ greeting }}，{{ adminName }}</p>
        <h2>{{ roleInfo.name }}数据概览</h2>
        <p class="desc">
          数据范围：{{ roleInfo.scope }}
          <span class="dot-sep">·</span>
          {{ dateText }}
        </p>
        <div class="todo">
          <span class="todo-chip"><i class="pulse" />{{ ongoingCount }} 项测评进行中</span>
          <span class="todo-chip">{{ pendingBackfill }} 条补录待审核</span>
          <span class="todo-chip">{{ draftCount }} 份试卷待完善</span>
        </div>
      </div>
      <div class="quick">
        <button
          v-for="action in quickActions"
          :key="action.key"
          class="quick-btn"
          @click="emit('navigate', action.key)"
        >
          <AppIcon :name="action.icon" :size="15" />
          <span>{{ action.label }}</span>
        </button>
      </div>
    </section>

    <section class="c-kpi-grid">
      <article v-for="kpi in kpis" :key="kpi.label" class="c-kpi">
        <div>
          <p class="k-label">{{ kpi.label }}</p>
          <p class="k-value">{{ kpi.value }}<small v-if="kpi.unit">{{ kpi.unit }}</small></p>
          <p class="k-foot"><span class="up">{{ kpi.delta }}</span>{{ kpi.foot }}</p>
        </div>
        <span class="k-icon" :class="kpi.tone"><AppIcon :name="kpi.icon" :size="21" /></span>
      </article>
    </section>

    <section class="charts-row">
      <article class="c-card">
        <header class="c-card-head">
          <h3>测评参与趋势</h3>
          <span class="hint">近 6 个月 · 参与人次</span>
        </header>
        <LineChart :labels="trendLabels" :series="trendSeries" suffix="" />
      </article>
      <article class="c-card">
        <header class="c-card-head">
          <h3>各年级平均分</h3>
          <span class="hint">音乐 + 美术</span>
        </header>
        <BarChart :labels="grades" :values="gradeAvg" :colors="['#1677ff']" decimals />
      </article>
    </section>

    <section class="bottom-row">
      <article class="c-card">
        <header class="c-card-head">
          <h3>{{ rankingTitle }}</h3>
          <span class="hint">按参与率</span>
        </header>
        <ul class="ranking">
          <li v-for="(item, i) in ranking" :key="item.label">
            <span class="rank-no" :class="{ top: i < 3 }">{{ i + 1 }}</span>
            <div class="rank-main">
              <div class="rank-line">
                <span>{{ item.label }}</span>
                <b class="c-num">{{ item.value.toFixed(1) }}%</b>
              </div>
              <div class="c-progress"><span :style="{ width: item.value + '%' }" /></div>
            </div>
          </li>
        </ul>
      </article>

      <article class="c-card">
        <header class="c-card-head">
          <h3>学科参与率</h3>
          <span class="hint">本期测评</span>
        </header>
        <div class="rings">
          <div v-for="ring in rings" :key="ring.name" class="ring-item">
            <div class="ring" :style="{ background: ring.style }">
              <div class="ring-inner">
                <b>{{ ring.value.toFixed(1) }}%</b>
                <span>{{ fmt(ring.count) }} 人</span>
              </div>
            </div>
            <p>{{ ring.name }}</p>
          </div>
        </div>
        <div class="ring-note">
          <AppIcon name="trend" :size="15" />
          整体参与率较上月提升 <b>4.6%</b>
        </div>
      </article>

      <article class="c-card">
        <header class="c-card-head">
          <h3>最近动态</h3>
          <button class="c-link-btn" @click="emit('navigate', 'statistics')">查看统计</button>
        </header>
        <ul class="activity">
          <li v-for="item in db.activities" :key="item.title">
            <span class="act-icon" :class="item.tone"><AppIcon :name="item.icon" :size="16" /></span>
            <div class="act-main">
              <p class="act-title">{{ item.title }}</p>
              <p class="act-desc">{{ item.desc }}</p>
            </div>
            <span class="act-time">{{ item.time }}</span>
          </li>
        </ul>
      </article>
    </section>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import AppIcon from '../../components/AppIcon.vue'
import LineChart from '../../components/LineChart.vue'
import BarChart from '../../components/BarChart.vue'
import {
  db,
  schoolsForRole,
  schoolsOfDistrict,
  districts,
  grades,
  subjects,
  aggregateRows,
  shortSchool,
  roleMeta
} from '../../data/consoleData'

const props = defineProps({ role: { type: String, default: 'school' } })
const emit = defineEmits(['navigate'])

const roleInfo = computed(() => roleMeta[props.role])

const scopeSchools = computed(() => schoolsForRole(props.role))
const scopeSchoolIds = computed(() => new Set(scopeSchools.value.map(s => s.id)))
const statsRows = computed(() => db.stats.filter(r => scopeSchoolIds.value.has(r.schoolId)))
const total = computed(() => aggregateRows(statsRows.value))

const adminName = computed(() => {
  if (props.role === 'school') return '王海燕'
  if (props.role === 'district') return '李建国'
  return '何文博'
})

const now = new Date()
const hour = now.getHours()
const greeting = hour < 6 ? '夜深了' : hour < 12 ? '上午好' : hour < 14 ? '中午好' : hour < 18 ? '下午好' : '晚上好'
const dateText = now.toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric', weekday: 'long' })

const ongoingCount = computed(
  () =>
    db.publishes.filter(p => p.level === props.role && p.start <= nowStampText() && p.end >= nowStampText()).length
)
function nowStampText() {
  const d = new Date()
  const pad = n => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`
}
const pendingBackfill = computed(() => {
  const ids = scopeSchoolIds.value
  return db.backfills.filter(b => ids.has(b.schoolId) && b.status === 'pending').length
})
const draftCount = computed(() => db.papers.filter(p => p.level === props.role && p.status === 'draft').length)

const classCount = computed(() => {
  const ids = scopeSchoolIds.value
  return new Set(db.students.filter(s => ids.has(s.schoolId)).map(s => `${s.schoolId}-${s.className}`)).size
})

const kpis = computed(() => {
  const first = {
    school: { label: '覆盖班级', value: classCount.value, unit: '个' },
    district: { label: '覆盖学校', value: scopeSchools.value.length, unit: '所' },
    city: { label: '覆盖区县', value: districts.filter(d => schoolsOfDistrict(d.id).length).length, unit: '个' }
  }[props.role]
  return [
    { ...first, icon: 'school', tone: 'blue', delta: '+2 ', foot: '较上学期' },
    { label: '参与学生', value: fmt(total.value.participants), unit: '人', icon: 'users', tone: 'green', delta: '+5.2% ', foot: '较上期' },
    { label: '平均成绩', value: total.value.avgScore.toFixed(1), unit: '分', icon: 'award', tone: 'purple', delta: '+1.8 ', foot: '较上期' },
    { label: '测评参与率', value: total.value.participation.toFixed(1), unit: '%', icon: 'target', tone: 'amber', delta: '+4.6% ', foot: '较上期' }
  ]
})

const quickActions = [
  { key: 'papers', label: '新建试卷', icon: 'paper' },
  { key: 'publish', label: '发布测评', icon: 'send' },
  { key: 'backfill', label: '成绩补录', icon: 'edit' },
  { key: 'accounts', label: '账号管理', icon: 'users' }
]

const trendLabels = ['5月', '6月', '7月', '8月', '9月', '10月']
const trendSeries = computed(() => {
  const factor = Math.max(0.6, scopeSchools.value.length / 12)
  const music = [1240, 1370, 960, 780, 1450, 1620].map(v => Math.round(v * factor))
  const art = [1080, 1260, 880, 720, 1320, 1480].map(v => Math.round(v * factor))
  return [
    { name: '音乐', color: '#1677ff', data: music },
    { name: '美术', color: '#13c2c2', data: art }
  ]
})

const gradeAvg = computed(() =>
  grades.map(g => {
    const rows = statsRows.value.filter(r => r.grade === g)
    return Number(aggregateRows(rows).avgScore.toFixed(1))
  })
)

const rankingTitle = computed(() =>
  props.role === 'school' ? '年级参与率排名' : props.role === 'district' ? '学校参与率排名' : '区县参与率排名'
)

const ranking = computed(() => {
  let list = []
  if (props.role === 'school') {
    list = grades.map(g => ({
      label: g,
      value: aggregateRows(statsRows.value.filter(r => r.grade === g)).participation
    }))
  } else if (props.role === 'district') {
    list = scopeSchools.value.map(s => ({
      label: shortSchool(s.name),
      value: aggregateRows(statsRows.value.filter(r => r.schoolId === s.id)).participation
    }))
  } else {
    list = districts
      .filter(d => schoolsOfDistrict(d.id).length)
      .map(d => ({
        label: d.name,
        value: aggregateRows(statsRows.value.filter(r => r.districtId === d.id)).participation
      }))
    const directRows = statsRows.value.filter(r => r.districtId === 'direct')
    if (directRows.length) list.push({ label: '市直属', value: aggregateRows(directRows).participation })
  }
  return list.sort((a, b) => b.value - a.value).slice(0, 5)
})

const rings = computed(() =>
  subjects.map((subject, i) => {
    const rows = statsRows.value.filter(r => r.subject === subject)
    const agg = aggregateRows(rows)
    const color = i === 0 ? '#1677ff' : '#13c2c2'
    return {
      name: subject,
      value: agg.participation,
      count: agg.participants,
      style: `conic-gradient(${color} 0 ${agg.participation * 3.6}deg, #f0f0f0 0)`
    }
  })
)

function fmt(n) {
  return Number(n).toLocaleString('zh-CN')
}
</script>

<style scoped>
.welcome {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  padding: 20px 22px;
  border: 1px solid #f0f0f0;
  border-radius: 8px;
  background: #fff;
}
.hello {
  margin: 0 0 4px;
  font-size: 12.5px;
  color: #86909c;
}
.welcome h2 {
  margin: 0 0 6px;
  font-size: 20px;
  font-weight: 600;
  color: #1f2329;
}
.desc {
  margin: 0;
  font-size: 12px;
  color: #86909c;
}
.dot-sep {
  margin: 0 6px;
  color: #c9cdd4;
}
.todo {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-top: 12px;
}
.todo-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 3px 9px;
  border: 1px solid #f0f0f0;
  border-radius: 4px;
  background: #f7f8fa;
  color: #4e5969;
  font-size: 12px;
}
.pulse {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #00b42a;
}
.quick {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  flex: none;
}
.quick-btn {
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 7px 12px;
  border: 1px solid #d9d9d9;
  border-radius: 6px;
  background: #fff;
  color: #1f2329;
  font-family: inherit;
  font-size: 12.5px;
  cursor: pointer;
  transition: all 0.16s;
}
.quick-btn:hover {
  border-color: #1677ff;
  color: #1677ff;
}
.quick-btn svg {
  color: #1677ff;
}
.charts-row {
  display: grid;
  grid-template-columns: 1.45fr 1fr;
  gap: 14px;
}
.bottom-row {
  display: grid;
  grid-template-columns: 1fr 0.85fr 1.15fr;
  gap: 14px;
}
.ranking {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.ranking li {
  display: flex;
  align-items: center;
  gap: 12px;
}
.rank-no {
  flex: none;
  width: 22px;
  height: 22px;
  border-radius: 4px;
  background: #f2f3f5;
  color: #6b7280;
  font-size: 11.5px;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
}
.rank-no.top {
  background: #e8f3ff;
  color: #1677ff;
  font-weight: 600;
}
.rank-main {
  flex: 1;
  min-width: 0;
}
.rank-line {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 6px;
  font-size: 12.5px;
  color: #4e5969;
}
.rank-line b {
  color: #1f2329;
  font-size: 12.5px;
}
.rings {
  display: flex;
  justify-content: space-around;
  gap: 10px;
  padding: 6px 0 14px;
}
.ring-item {
  text-align: center;
}
.ring {
  width: 108px;
  height: 108px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}
.ring-inner {
  width: 82px;
  height: 82px;
  border-radius: 50%;
  background: #fff;
  box-shadow: inset 0 0 0 1px #f0f0f0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2px;
}
.ring-inner b {
  font-size: 17px;
  color: #1f2329;
}
.ring-inner span {
  font-size: 10.5px;
  color: #86909c;
}
.ring-item p {
  margin: 8px 0 0;
  font-size: 12.5px;
  color: #4e5969;
}
.ring-note {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  padding: 8px;
  border-radius: 4px;
  background: #f7f8fa;
  font-size: 11.5px;
  color: #6b7280;
}
.ring-note b {
  color: #1a9c3f;
}
.activity {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 13px;
}
.activity li {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}
.act-icon {
  flex: none;
  width: 30px;
  height: 30px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.act-icon.blue {
  background: #e8f3ff;
  color: #1677ff;
}
.act-icon.green {
  background: #edfbf0;
  color: #1a9c3f;
}
.act-icon.amber {
  background: #fff7e8;
  color: #d48806;
}
.act-icon.purple {
  background: #f0f5ff;
  color: #2f54eb;
}
.act-icon.pink {
  background: #fff0f6;
  color: #c41d7f;
}
.act-main {
  flex: 1;
  min-width: 0;
}
.act-title {
  margin: 0 0 3px;
  font-size: 12.5px;
  color: #1f2329;
  line-height: 1.4;
}
.act-desc {
  margin: 0;
  font-size: 11.5px;
  color: #86909c;
}
.act-time {
  flex: none;
  font-size: 11px;
  color: #b0b8c6;
}
@media (max-width: 1200px) {
  .charts-row,
  .bottom-row {
    grid-template-columns: 1fr 1fr;
  }
  .bottom-row > .c-card:last-child {
    grid-column: 1 / -1;
  }
}
@media (max-width: 900px) {
  .welcome {
    flex-direction: column;
    align-items: flex-start;
    padding: 22px;
  }
  .quick {
    width: 100%;
  }
  .charts-row,
  .bottom-row {
    grid-template-columns: 1fr;
  }
  .bottom-row > .c-card:last-child {
    grid-column: auto;
  }
  .welcome h2 {
    font-size: 22px;
  }
}
</style>
