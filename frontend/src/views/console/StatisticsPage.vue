<template>
  <div class="c-page">
    <header class="c-page-head">
      <div>
        <h2>数据统计</h2>
        <p class="sub">{{ subtitle }}</p>
      </div>
      <div class="actions">
        <button class="c-btn outline" @click="exportAll">
          <AppIcon name="download" :size="16" />导出数据
        </button>
      </div>
    </header>

    <div v-if="focusInfo" class="focus-banner">
      <span class="focus-icon"><AppIcon name="target" :size="17" /></span>
      <div class="focus-main">
        <b>正在查看：{{ focusInfo.name }}</b>
        <span>{{ focusInfo.scopeText }} · {{ focusInfo.grade }}{{ focusInfo.subject }}</span>
      </div>
      <button class="c-btn ghost sm" @click="clearFocus">清除定位</button>
    </div>

    <section class="c-card">
      <div class="filter-row">
        <RegionCascade
          v-if="role !== 'school'"
          :role="role"
          v-model:district-id="form.districtId"
          v-model:school-id="form.schoolId"
        />
        <select v-model="form.grade" class="c-select">
          <option value="">全部年级</option>
          <option v-for="g in grades" :key="g">{{ g }}</option>
        </select>
        <select v-model="form.subject" class="c-select">
          <option value="">全部学科</option>
          <option>音乐</option>
          <option>美术</option>
        </select>
        <div class="spacer" />
        <button class="c-btn ghost" @click="resetFilters">
          <AppIcon name="refresh" :size="15" />重置
        </button>
        <button class="c-btn primary" @click="applyFilters">
          <AppIcon name="search" :size="15" />查询
        </button>
      </div>
    </section>

    <section class="c-kpi-grid">
      <article v-for="kpi in kpis" :key="kpi.label" class="c-kpi">
        <div>
          <p class="k-label">{{ kpi.label }}</p>
          <p class="k-value">{{ kpi.value }}<small>{{ kpi.unit }}</small></p>
          <p class="k-foot">{{ kpi.foot }}</p>
        </div>
        <span class="k-icon" :class="kpi.tone"><AppIcon :name="kpi.icon" :size="21" /></span>
      </article>
    </section>

    <section class="charts-row">
      <article class="c-card">
        <header class="c-card-head">
          <h3>{{ chartTitle }}</h3>
          <span class="hint">平均分对比</span>
        </header>
        <BarChart :labels="chartLabels" :values="chartValues" :colors="barColors" decimals />
      </article>
      <article class="c-card">
        <header class="c-card-head">
          <h3>参与率趋势</h3>
          <span class="hint">近 6 个月</span>
        </header>
        <LineChart :labels="trendLabels" :series="trendSeries" suffix="%" />
      </article>
    </section>

    <section class="c-card">
      <header class="c-card-head">
        <h3>统计明细</h3>
        <span class="hint">
          {{ scopeHint }} · {{ applied.grade || '全部年级' }} · {{ applied.subject || '全部学科' }}
        </span>
      </header>
      <div v-if="groups.length" class="c-table-wrap">
        <table class="c-table">
          <thead>
            <tr>
              <th>{{ dimensionLabel }}</th>
              <th>测评人数</th>
              <th>参与率</th>
              <th>平均分</th>
              <th>优秀率</th>
              <th>及格率</th>
              <th>趋势</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="g in groups" :key="g.key">
              <td>
                <div class="c-cell-name">{{ g.label }}</div>
                <div class="c-cell-sub">{{ g.sub }}</div>
              </td>
              <td class="c-num">
                {{ fmt(g.agg.participants) }}
                <span class="c-muted">/ {{ fmt(g.agg.eligible) }}</span>
              </td>
              <td>
                <span class="rate">{{ g.agg.participation.toFixed(1) }}%</span>
              </td>
              <td class="c-num">{{ g.agg.avgScore.toFixed(1) }}</td>
              <td class="c-num">{{ g.agg.excellentRate.toFixed(1) }}%</td>
              <td class="c-num">{{ g.agg.passRate.toFixed(1) }}%</td>
              <td>
                <SparkLine :values="g.spark" :color="g.agg.avgScore >= 85 ? '#13c2c2' : '#1677ff'" />
              </td>
              <td>
                <button class="c-link-btn" @click="exportRow(g)">导出</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="c-empty">
        <AppIcon name="chart" :size="38" />
        当前筛选条件下暂无统计数据
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref, watch } from 'vue'
import AppIcon from '../../components/AppIcon.vue'
import BarChart from '../../components/BarChart.vue'
import LineChart from '../../components/LineChart.vue'
import SparkLine from '../../components/SparkLine.vue'
import RegionCascade from '../../components/RegionCascade.vue'
import { toast } from '../../data/toast'
import {
  db,
  SCHOOL_ID,
  DISTRICT_ID,
  districts,
  grades,
  schools,
  schoolsOfDistrict,
  getSchool,
  getDistrict,
  aggregateRows,
  districtNameOfSchool,
  shortSchool,
  sparklineFor,
  downloadCsv
} from '../../data/consoleData'

const props = defineProps({ role: { type: String, default: 'school' } })
const role = computed(() => props.role)

const subtitle = computed(
  () =>
    ({
      school: '按年级查看本校艺术测评成绩、参与率与优秀率，支持一键导出',
      district: '按学校、年级查看区县测评数据，支持按学校或地区导出统计报表',
      city: '按区县、学校、年级多维度查看全市艺术测评数据，支持分级导出'
    })[props.role]
)

const form = reactive({ districtId: '', schoolId: '', grade: '', subject: '' })
const applied = reactive({ districtId: '', schoolId: '', grade: '', subject: '' })
const focusInfo = ref(null)

watch(
  () => props.role,
  () => {
    resetFilters()
    focusInfo.value = null
  }
)

onMounted(() => {
  if (db.focusPublish) {
    focusInfo.value = db.focusPublish
    form.grade = db.focusPublish.grade || ''
    form.subject = db.focusPublish.subject || ''
    Object.assign(applied, form)
    db.focusPublish = null
  }
})

const scopeSchools = computed(() => {
  if (props.role === 'school') return schools.filter(s => s.id === SCHOOL_ID)
  if (props.role === 'district') {
    return applied.schoolId ? schools.filter(s => s.id === applied.schoolId) : schoolsOfDistrict(DISTRICT_ID)
  }
  if (applied.schoolId) return schools.filter(s => s.id === applied.schoolId)
  if (applied.districtId) return schoolsOfDistrict(applied.districtId)
  return schools
})

const scopeSchoolIds = computed(() => new Set(scopeSchools.value.map(s => s.id)))

const rows = computed(() =>
  db.stats.filter(r => {
    if (!scopeSchoolIds.value.has(r.schoolId)) return false
    if (applied.grade && r.grade !== applied.grade) return false
    if (applied.subject && r.subject !== applied.subject) return false
    return true
  })
)

const total = computed(() => aggregateRows(rows.value))

const kpis = computed(() => [
  { label: '测评人数', value: fmt(total.value.participants), unit: '人', icon: 'users', tone: 'blue', foot: `应测 ${fmt(total.value.eligible)} 人` },
  { label: '测评参与率', value: total.value.participation.toFixed(1), unit: '%', icon: 'target', tone: 'green', foot: '较上期 +4.6%' },
  { label: '平均成绩', value: total.value.avgScore.toFixed(1), unit: '分', icon: 'award', tone: 'purple', foot: '较上期 +1.8 分' },
  { label: '优秀率', value: total.value.excellentRate.toFixed(1), unit: '%', icon: 'trend', tone: 'amber', foot: '及格率 ' + total.value.passRate.toFixed(1) + '%' }
])

const dimension = computed(() => {
  if (props.role === 'school') return 'grade'
  if (props.role === 'district') return applied.schoolId ? 'grade' : 'school'
  if (applied.schoolId) return 'grade'
  if (applied.districtId) return 'school'
  return 'district'
})

const dimensionLabel = computed(() =>
  dimension.value === 'grade' ? '年级' : dimension.value === 'school' ? '学校' : '区县'
)

const groups = computed(() => {
  if (dimension.value === 'grade') {
    return grades
      .map(g => {
        const list = rows.value.filter(r => r.grade === g)
        return {
          key: g,
          label: g,
          sub: applied.subject || '音乐 + 美术',
          rows: list,
          agg: aggregateRows(list),
          spark: sparklineFor(g, aggregateRows(list).avgScore || 80)
        }
      })
      .filter(g => g.rows.length)
  }
  if (dimension.value === 'school') {
    return scopeSchools.value
      .map(s => {
        const list = rows.value.filter(r => r.schoolId === s.id)
        return {
          key: s.id,
          label: s.name,
          sub: districtNameOfSchool(s),
          rows: list,
          agg: aggregateRows(list),
          spark: sparklineFor(s.name, aggregateRows(list).avgScore || 80)
        }
      })
      .filter(g => g.rows.length)
      .sort((a, b) => b.agg.avgScore - a.agg.avgScore)
  }
  const list = districts
    .filter(d => schoolsOfDistrict(d.id).length)
    .map(d => {
      const groupRows = rows.value.filter(r => r.districtId === d.id)
      return {
        key: d.id,
        label: d.name,
        sub: `${schoolsOfDistrict(d.id).length} 所学校`,
        rows: groupRows,
        agg: aggregateRows(groupRows),
        spark: sparklineFor(d.name, aggregateRows(groupRows).avgScore || 80)
      }
    })
  const directRows = rows.value.filter(r => r.districtId === 'direct')
  if (directRows.length) {
    list.push({
      key: 'direct',
      label: '市直属学校',
      sub: '云州市教育局直属',
      rows: directRows,
      agg: aggregateRows(directRows),
      spark: sparklineFor('市直属', aggregateRows(directRows).avgScore || 80)
    })
  }
  return list.filter(g => g.rows.length)
})

const chartTitle = computed(() =>
  dimensionLabel.value === '区县' ? '各区县平均分' : dimensionLabel.value === '学校' ? '各学校平均分' : '各年级平均分'
)
const chartLabels = computed(() =>
  groups.value.map(g => (dimension.value === 'school' ? shortSchool(g.label) : g.label))
)
const chartValues = computed(() => groups.value.map(g => Number(g.agg.avgScore.toFixed(1))))
const barColors = computed(() => chartValues.value.map(() => '#1677ff'))

const trendLabels = ['5月', '6月', '7月', '8月', '9月', '10月']
const trendSeries = computed(() => {
  const base = total.value.participation || 0
  const values = [-7, -5.2, -3.6, -2.1, -0.8, 0].map(d => Number(Math.max(0, Math.min(100, base + d)).toFixed(1)))
  return [{ name: '参与率', color: '#1677ff', data: values }]
})

const scopeHint = computed(() => {
  if (props.role === 'school') return '云州区第一中学'
  if (props.role === 'district') {
    return applied.schoolId ? getSchool(applied.schoolId)?.name : '云州区 · 全部学校'
  }
  if (applied.schoolId) return getSchool(applied.schoolId)?.name
  if (applied.districtId) return `${getDistrict(applied.districtId)?.name} · 全部学校`
  return '云州市 · 全部区县'
})

function applyFilters() {
  Object.assign(applied, form)
  toast('统计数据已刷新', 'info')
}

function resetFilters() {
  Object.assign(form, { districtId: '', schoolId: '', grade: '', subject: '' })
  Object.assign(applied, form)
}

function clearFocus() {
  focusInfo.value = null
  form.grade = ''
  form.subject = ''
  Object.assign(applied, form)
}

function fmt(n) {
  return Number(n).toLocaleString('zh-CN')
}

const headers = ['统计维度', '测评人数', '应测人数', '参与率', '平均分', '优秀率', '及格率']

function exportRow(group) {
  const row = [
    group.label,
    group.agg.participants,
    group.agg.eligible,
    group.agg.participation.toFixed(1) + '%',
    group.agg.avgScore.toFixed(1),
    group.agg.excellentRate.toFixed(1) + '%',
    group.agg.passRate.toFixed(1) + '%'
  ]
  downloadCsv(`艺术测评统计-${group.label}.csv`, headers, [row])
  toast(`「${group.label}」统计数据已导出`)
}

function exportAll() {
  if (!groups.value.length) return toast('当前没有可导出的数据', 'error')
  downloadCsv(
    `艺术测评统计-${scopeHint.value}.csv`,
    headers,
    groups.value.map(g => [
      g.label,
      g.agg.participants,
      g.agg.eligible,
      g.agg.participation.toFixed(1) + '%',
      g.agg.avgScore.toFixed(1),
      g.agg.excellentRate.toFixed(1) + '%',
      g.agg.passRate.toFixed(1) + '%'
    ])
  )
  toast('统计数据已导出为 CSV 文件')
}
</script>

<style scoped>
.filter-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 10px;
}
.filter-row .spacer {
  flex: 1;
}
.filter-row .c-select {
  width: auto;
  min-width: 118px;
}
.focus-banner {
  display: flex;
  align-items: center;
  gap: 11px;
  padding: 12px 16px;
  border: 1px solid #f0f0f0;
  border-radius: 8px;
  background: #f7f8fa;
}
.focus-icon {
  flex: none;
  width: 32px;
  height: 32px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #e8f3ff;
  color: #1677ff;
}
.focus-main {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 3px;
}
.focus-main b {
  font-size: 12.5px;
  color: #1f2329;
}
.focus-main span {
  font-size: 11.5px;
  color: #6b7280;
}
.charts-row {
  display: grid;
  grid-template-columns: 1.4fr 1fr;
  gap: 14px;
}
.rate {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-weight: 600;
  color: #1677ff;
}
@media (max-width: 1100px) {
  .charts-row {
    grid-template-columns: 1fr;
  }
}
</style>
