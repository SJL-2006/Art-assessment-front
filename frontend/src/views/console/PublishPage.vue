<template>
  <div class="c-page">
    <header class="c-page-head">
      <div>
        <h2>测评发布</h2>
        <p class="sub">{{ subtitle }}</p>
      </div>
      <div class="actions">
        <button class="c-btn outline" @click="emit('navigate', 'papers')">
          <AppIcon name="plus" :size="16" />新建试卷
        </button>
      </div>
    </header>

    <section class="c-kpi-grid">
      <article v-for="card in summary" :key="card.label" class="c-kpi">
        <div>
          <p class="k-label">{{ card.label }}</p>
          <p class="k-value">{{ card.value }}<small>{{ card.unit }}</small></p>
          <p class="k-foot">{{ card.foot }}</p>
        </div>
        <span class="k-icon" :class="card.tone"><AppIcon :name="card.icon" :size="21" /></span>
      </article>
    </section>

    <section class="publish-layout">
      <article class="c-card">
        <header class="c-card-head">
          <h3>发布新测评</h3>
          <span class="hint">{{ roleMeta[role].name }} · {{ roleMeta[role].scope }}</span>
        </header>
        <div class="c-form-grid">
          <div class="c-field full">
            <label>测评试卷<span class="req">*</span></label>
            <select v-model="form.paperId" class="c-select">
              <option value="">请选择要发布的试卷</option>
              <option v-for="p in rolePapers" :key="p.id" :value="p.id">
                {{ p.name }}（{{ p.subject }} · {{ p.grade }}）
              </option>
            </select>
          </div>
          <div class="c-field">
            <label>测评学科</label>
            <input class="c-input" :value="selectedPaper?.subject || '—'" disabled />
          </div>
          <div class="c-field">
            <label>测评年级</label>
            <select v-model="form.grade" class="c-select">
              <option v-for="g in grades" :key="g">{{ g }}</option>
            </select>
          </div>

          <div class="c-field full">
            <label>发布范围</label>
            <div v-if="role === 'school'" class="fixed-scope">
              <AppIcon name="school" :size="16" />
              {{ schoolName }} · {{ form.grade }}
            </div>
            <RegionCascade
              v-else
              :role="role"
              v-model:district-id="form.districtId"
              v-model:school-id="form.schoolId"
            />
            <span class="tip">
              {{ role === 'city' ? '不选择区县/学校时，将按全市范围发布' : role === 'district' ? '不选择学校时，将向全区县学校发布' : '测评将发布给本校指定年级的全部学生' }}
            </span>
          </div>

          <div class="c-field">
            <label>开始时间<span class="req">*</span></label>
            <input v-model="form.start" type="datetime-local" class="c-input" />
          </div>
          <div class="c-field">
            <label>截止时间<span class="req">*</span></label>
            <input v-model="form.end" type="datetime-local" class="c-input" />
          </div>
          <div class="c-field">
            <label>测评时长</label>
            <select v-model.number="form.duration" class="c-select">
              <option :value="30">30 分钟</option>
              <option :value="45">45 分钟</option>
              <option :value="60">60 分钟</option>
              <option :value="90">90 分钟</option>
            </select>
          </div>
          <div class="c-field">
            <label>预计覆盖</label>
            <div class="target-preview"><b>{{ targetCount }}</b> 人</div>
          </div>
          <div class="c-field full">
            <label>测评说明</label>
            <textarea v-model="form.note" class="c-textarea" rows="2" placeholder="选填，将展示给参与测评的学校与班级" />
          </div>
        </div>
        <div class="publish-actions">
          <button class="c-btn ghost" @click="resetForm">重置</button>
          <button class="c-btn primary" :disabled="!selectedPaper" @click="publish">
            <AppIcon name="send" :size="16" />立即发布
          </button>
        </div>
      </article>

      <article class="c-card preview">
        <header class="c-card-head">
          <h3>发布预览</h3>
          <span class="hint">发布前确认</span>
        </header>
        <template v-if="selectedPaper">
          <div class="preview-paper">
            <span class="preview-icon" :class="selectedPaper.subject === '音乐' ? 'blue' : 'pink'">
              <AppIcon :name="selectedPaper.subject === '音乐' ? 'music' : 'palette'" :size="22" />
            </span>
            <div>
              <p class="preview-name">{{ selectedPaper.name }}</p>
              <div class="preview-tags">
                <span class="c-tag blue">{{ selectedPaper.subject }}</span>
                <span class="c-tag purple">{{ selectedPaper.grade }}</span>
                <span class="c-tag amber">{{ selectedPaper.difficulty }}</span>
              </div>
            </div>
          </div>
          <ul class="preview-info">
            <li><span>组卷方式</span><b>{{ selectedPaper.mode }}</b></li>
            <li><span>题量 / 总分</span><b>{{ selectedPaper.questionCount }} 题 / {{ selectedPaper.totalScore }} 分</b></li>
            <li><span>发布范围</span><b>{{ scopeText }}</b></li>
            <li><span>测评时间</span><b>{{ displayTime(form.start) }} 至 {{ displayTime(form.end) }}</b></li>
            <li><span>测评时长</span><b>{{ form.duration }} 分钟</b></li>
            <li><span>预计覆盖</span><b>{{ targetCount }} 名学生</b></li>
          </ul>
        </template>
        <div v-else class="preview-empty">
          <AppIcon name="paper" :size="34" />
          选择一份试卷后查看发布预览
        </div>
        <div class="preview-tips">
          <p><AppIcon name="check-circle" :size="14" />发布后，学生可在规定时间内进入测评作答</p>
          <p><AppIcon name="check-circle" :size="14" />截止时间到达后系统自动收卷并生成统计</p>
          <p><AppIcon name="check-circle" :size="14" />未结束的测评可在下方列表中随时撤回</p>
        </div>
      </article>
    </section>

    <section class="c-card">
      <header class="c-card-head">
        <h3>已发布测评</h3>
        <div class="c-segmented">
          <button
            v-for="tab in statusTabs"
            :key="tab.key"
            class="item"
            :class="{ active: statusFilter === tab.key }"
            @click="statusFilter = tab.key"
          >{{ tab.name }} {{ tab.count }}</button>
        </div>
      </header>

      <div v-if="visibleRecords.length" class="c-table-wrap">
        <table class="c-table">
          <thead>
            <tr>
              <th>测评名称</th>
              <th>发布范围</th>
              <th>测评时间</th>
              <th>参与进度</th>
              <th>状态</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="rec in visibleRecords" :key="rec.id">
              <td>
                <div class="c-cell-main">
                  <span class="record-icon" :class="rec.subject === '音乐' ? 'blue' : 'pink'">
                    <AppIcon :name="rec.subject === '音乐' ? 'music' : 'palette'" :size="16" />
                  </span>
                  <div>
                    <div class="c-cell-name">{{ rec.name }}</div>
                    <div class="c-cell-sub">{{ rec.grade }} · {{ rec.duration }} 分钟 · {{ rec.subject }}</div>
                  </div>
                </div>
              </td>
              <td class="scope-cell">{{ rec.scopeText }}</td>
              <td class="time-cell">
                <div>{{ displayTime(rec.start) }}</div>
                <div class="c-cell-sub">至 {{ displayTime(rec.end) }}</div>
              </td>
              <td>
                <div class="progress-cell">
                  <div class="c-progress"><span :style="{ width: progressOf(rec) + '%' }" /></div>
                  <span class="c-num">{{ fmt(rec.submitted) }} / {{ fmt(rec.target) }}</span>
                </div>
              </td>
              <td>
                <span class="c-tag" :class="publishStatusMeta[publishStatus(rec)].tag">
                  <i class="c-dot" />{{ publishStatusMeta[publishStatus(rec)].label }}
                </span>
              </td>
              <td>
                <div class="c-row-actions">
                  <button class="c-link-btn" @click="viewStats(rec)">查看数据</button>
                  <button class="c-link-btn danger" @click="askRevoke(rec)">撤回</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="c-empty">
        <AppIcon name="send" :size="38" />
        暂无{{ statusFilter === 'all' ? '' : statusTabs.find(t => t.key === statusFilter)?.name }}测评
      </div>
    </section>

    <BaseModal v-model="confirmOpen" title="撤回测评" width="440px">
      <p class="confirm-text">
        确定要撤回「{{ revokeTarget?.name }}」吗？撤回后学生将无法继续作答，已提交的数据会保留。
      </p>
      <template #footer>
        <button class="c-btn ghost" @click="confirmOpen = false">取消</button>
        <button class="c-btn danger" @click="confirmRevoke">确认撤回</button>
      </template>
    </BaseModal>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref, watch } from 'vue'
import AppIcon from '../../components/AppIcon.vue'
import BaseModal from '../../components/BaseModal.vue'
import RegionCascade from '../../components/RegionCascade.vue'
import { toast } from '../../data/toast'
import {
  db,
  DISTRICT_ID,
  SCHOOL_ID,
  districts,
  getDistrict,
  getSchool,
  grades,
  localInputValue,
  nextId,
  dateStr,
  publishStatus,
  publishStatusMeta,
  roleMeta,
  schools,
  schoolsOfDistrict
} from '../../data/consoleData'

const props = defineProps({ role: { type: String, default: 'school' } })
const emit = defineEmits(['navigate'])

const role = computed(() => props.role)
const schoolName = getSchool(SCHOOL_ID)?.name || ''
const subtitle = computed(
  () =>
    ({
      school: '将学校测评试卷发布到指定年级，实时查看参与进度与数据统计',
      district: '将区县测评试卷按学校、年级逐级下发，统一跟踪各校参与情况',
      city: '将市州统考试卷按区县、学校分级发布，掌握全市测评进度'
    })[props.role]
)

const rolePapers = computed(() => db.papers.filter(p => p.level === props.role))

const form = reactive({
  paperId: '',
  grade: '八年级',
  districtId: '',
  schoolId: '',
  start: localInputValue(0, 9),
  end: localInputValue(7, 18),
  duration: 45,
  note: ''
})

const selectedPaper = computed(() => rolePapers.value.find(p => p.id === form.paperId) || null)

watch(
  () => props.role,
  () => {
    resetForm()
    statusFilter.value = 'all'
  }
)

watch(selectedPaper, paper => {
  if (paper) form.grade = paper.grade
})

onMounted(() => {
  if (db.focusPaperId) {
    const paper = rolePapers.value.find(p => p.id === db.focusPaperId)
    if (paper) {
      form.paperId = paper.id
      form.grade = paper.grade
    }
    db.focusPaperId = null
  }
  if (db.focusPublish) db.focusPublish = null
})

const scopeText = computed(() => {
  if (props.role === 'school') return `${schoolName} · ${form.grade}`
  if (props.role === 'district') {
    const school = form.schoolId ? getSchool(form.schoolId)?.name : '全部学校'
    return `云州区 · ${school} · ${form.grade}`
  }
  const district = form.districtId ? getDistrict(form.districtId)?.name : '全部区县'
  const school = form.schoolId ? getSchool(form.schoolId)?.name : '全部学校'
  return `云州市 · ${district} · ${school} · ${form.grade}`
})

const targetSchoolIds = computed(() => {
  if (props.role === 'school') return [SCHOOL_ID]
  if (props.role === 'district') {
    return form.schoolId ? [form.schoolId] : schoolsOfDistrict(DISTRICT_ID).map(s => s.id)
  }
  if (form.schoolId) return [form.schoolId]
  if (form.districtId) return schoolsOfDistrict(form.districtId).map(s => s.id)
  return schools.map(s => s.id)
})

const targetCount = computed(() => {
  if (!selectedPaper.value) return 0
  const ids = new Set(targetSchoolIds.value)
  return db.stats
    .filter(r => ids.has(r.schoolId) && r.grade === form.grade && r.subject === selectedPaper.value.subject)
    .reduce((sum, r) => sum + r.eligible, 0)
})

function displayTime(value) {
  return (value || '').replace('T', ' ')
}

const records = computed(() =>
  db.publishes
    .filter(p => p.level === props.role)
    .slice()
    .sort((a, b) => b.start.localeCompare(a.start))
)

const statusFilter = ref('all')
const statusTabs = computed(() => {
  const counts = { ongoing: 0, pending: 0, done: 0 }
  records.value.forEach(r => counts[publishStatus(r)]++)
  return [
    { key: 'all', name: '全部', count: records.value.length },
    { key: 'ongoing', name: '进行中', count: counts.ongoing },
    { key: 'pending', name: '待开始', count: counts.pending },
    { key: 'done', name: '已结束', count: counts.done }
  ]
})
const visibleRecords = computed(() =>
  statusFilter.value === 'all'
    ? records.value
    : records.value.filter(r => publishStatus(r) === statusFilter.value)
)

const summary = computed(() => {
  const counts = { ongoing: 0, pending: 0, done: 0 }
  records.value.forEach(r => counts[publishStatus(r)]++)
  return [
    { label: '进行中测评', value: counts.ongoing, icon: 'activity', tone: 'green', foot: '学生可正常作答', unit: '场' },
    { label: '待开始测评', value: counts.pending, icon: 'calendar', tone: 'blue', foot: '已排期待发布', unit: '场' },
    { label: '已结束测评', value: counts.done, icon: 'check-circle', tone: 'purple', foot: '数据已归档', unit: '场' },
    { label: '累计参与人次', value: fmt(records.value.reduce((s, r) => s + r.submitted, 0)), icon: 'users', tone: 'amber', foot: '含全部已发布测评', unit: '人次' }
  ]
})

function progressOf(rec) {
  if (!rec.target) return 0
  return Math.min(100, Math.round((rec.submitted / rec.target) * 100))
}
function fmt(n) {
  return Number(n).toLocaleString('zh-CN')
}

function publish() {
  if (!selectedPaper.value) return toast('请先选择测评试卷', 'error')
  if (!form.start || !form.end) return toast('请设置测评开始与截止时间', 'error')
  if (new Date(form.end) <= new Date(form.start)) return toast('截止时间需晚于开始时间', 'error')

  db.publishes.push({
    id: nextId('pub'),
    level: props.role,
    paperId: selectedPaper.value.id,
    name: selectedPaper.value.name,
    subject: selectedPaper.value.subject,
    grade: form.grade,
    scopeText: scopeText.value,
    start: displayTime(form.start),
    end: displayTime(form.end),
    duration: form.duration,
    target: targetCount.value,
    submitted: 0,
    note: form.note,
    createdAt: dateStr()
  })
  toast('测评发布成功，已通知相关学校')
  db.activities.unshift({
    icon: 'send',
    tone: 'blue',
    title: `发布《${selectedPaper.value.name}》`,
    desc: `${scopeText.value} · 预计 ${targetCount.value} 人`,
    time: '刚刚'
  })
  form.paperId = ''
  form.note = ''
}

function resetForm() {
  form.paperId = ''
  form.grade = '八年级'
  form.districtId = ''
  form.schoolId = ''
  form.start = localInputValue(0, 9)
  form.end = localInputValue(7, 18)
  form.duration = 45
  form.note = ''
}

const confirmOpen = ref(false)
const revokeTarget = ref(null)

function askRevoke(rec) {
  revokeTarget.value = rec
  confirmOpen.value = true
}

function confirmRevoke() {
  const index = db.publishes.findIndex(p => p.id === revokeTarget.value?.id)
  if (index > -1) db.publishes.splice(index, 1)
  confirmOpen.value = false
  toast('测评已撤回')
}

function viewStats(rec) {
  db.focusPublish = {
    id: rec.id,
    name: rec.name,
    subject: rec.subject,
    grade: rec.grade,
    scopeText: rec.scopeText
  }
  emit('navigate', 'statistics')
}
</script>

<style scoped>
.publish-layout {
  display: grid;
  grid-template-columns: minmax(0, 1.5fr) minmax(300px, 0.9fr);
  gap: 14px;
  align-items: start;
}
.publish-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 18px;
  padding-top: 16px;
  border-top: 1px solid #f0f3f9;
}
.fixed-scope {
  display: flex;
  align-items: center;
  gap: 7px;
  height: 32px;
  padding: 0 11px;
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  background: #f7f8fa;
  color: #4e5969;
  font-size: 13px;
}
.target-preview {
  display: flex;
  align-items: baseline;
  gap: 4px;
  height: 32px;
  padding: 0 11px;
  border-radius: 6px;
  background: #f7f8fa;
  color: #6b7280;
  font-size: 12px;
}
.target-preview b {
  font-size: 18px;
  color: #1677ff;
}
.preview {
  position: sticky;
  top: 78px;
}
.preview-paper {
  display: flex;
  gap: 12px;
  padding: 14px;
  border-radius: 8px;
  background: #f7f8fa;
}
.preview-icon {
  flex: none;
  width: 44px;
  height: 44px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.preview-icon.blue {
  background: #eaf2ff;
  color: #1677ff;
}
.preview-icon.pink {
  background: #fff0f6;
  color: #c41d7f;
}
.preview-name {
  margin: 0 0 7px;
  font-size: 13px;
  font-weight: 600;
  line-height: 1.5;
  color: #1f2329;
}
.preview-tags {
  display: flex;
  gap: 5px;
  flex-wrap: wrap;
}
.preview-info {
  list-style: none;
  margin: 14px 0 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.preview-info li {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 14px;
  font-size: 12px;
}
.preview-info span {
  flex: none;
  color: #86909c;
}
.preview-info b {
  text-align: right;
  font-weight: 500;
  color: #1f2329;
  line-height: 1.5;
}
.preview-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 44px 16px;
  color: #86909c;
  font-size: 12.5px;
  text-align: center;
}
.preview-empty svg {
  color: #c5cddb;
}
.preview-tips {
  margin-top: 16px;
  padding-top: 13px;
  border-top: 1px dashed #eef1f7;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.preview-tips p {
  display: flex;
  align-items: flex-start;
  gap: 7px;
  margin: 0;
  font-size: 11.5px;
  line-height: 1.6;
  color: #6b7280;
}
.preview-tips svg {
  flex: none;
  margin-top: 1px;
  color: #1a9c3f;
}
.record-icon {
  flex: none;
  width: 30px;
  height: 30px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.record-icon.blue {
  background: #eaf2ff;
  color: #1677ff;
}
.record-icon.pink {
  background: #fff0f6;
  color: #c41d7f;
}
.scope-cell {
  max-width: 230px;
  font-size: 12.5px;
  line-height: 1.5;
}
.time-cell {
  font-size: 12px;
  white-space: nowrap;
}
.progress-cell {
  min-width: 130px;
}
.progress-cell .c-progress {
  margin-bottom: 5px;
}
.progress-cell .c-num {
  font-size: 11.5px;
  color: #6b7280;
}
.confirm-text {
  margin: 0;
  font-size: 13.5px;
  line-height: 1.75;
  color: #4e5969;
}
@media (max-width: 1100px) {
  .publish-layout {
    grid-template-columns: 1fr;
  }
  .preview {
    position: static;
  }
}
</style>
