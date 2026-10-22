<template>
  <div class="c-page">
    <header class="c-page-head">
      <div>
        <h2>测评补录</h2>
        <p class="sub">{{ subtitle }}</p>
      </div>
      <div class="actions">
        <button class="c-btn outline" @click="exportRecords">
          <AppIcon name="download" :size="16" />导出补录记录
        </button>
      </div>
    </header>

    <section class="c-kpi-grid three">
      <article class="c-kpi">
        <div>
          <p class="k-label">本月补录</p>
          <p class="k-value">{{ monthCount }}<small>条</small></p>
          <p class="k-foot">含补录申请与审核记录</p>
        </div>
        <span class="k-icon blue"><AppIcon name="edit" :size="21" /></span>
      </article>
      <article class="c-kpi">
        <div>
          <p class="k-label">待审核</p>
          <p class="k-value">{{ pendingCount }}<small>条</small></p>
          <p class="k-foot">请及时完成审核</p>
        </div>
        <span class="k-icon amber"><AppIcon name="clock" :size="21" /></span>
      </article>
      <article class="c-kpi">
        <div>
          <p class="k-label">补录通过率</p>
          <p class="k-value">{{ approvalRate }}<small>%</small></p>
          <p class="k-foot">已通过 / 已审核</p>
        </div>
        <span class="k-icon green"><AppIcon name="check-circle" :size="21" /></span>
      </article>
    </section>

    <section class="backfill-layout">
      <article class="c-card form-card">
        <header class="c-card-head">
          <h3>补录申请</h3>
          <span class="hint">{{ roleMeta[role].scope }}</span>
        </header>
        <div class="form-stack">
          <div class="c-field">
            <label>选择学生<span class="req">*</span></label>
            <select v-model="form.studentId" class="c-select">
              <option value="">请选择需要补录的学生</option>
              <option v-for="s in studentOptions" :key="s.id" :value="s.id">
                {{ s.name }} · {{ getSchool(s.schoolId)?.name }} · {{ s.className }}
              </option>
            </select>
          </div>
          <div class="c-field">
            <label>测评学科</label>
            <div class="c-segmented">
              <button
                v-for="s in ['音乐', '美术']"
                :key="s"
                class="item"
                :class="{ active: form.subject === s }"
                @click="form.subject = s"
              >{{ s }}</button>
            </div>
          </div>
          <div class="c-field">
            <label>测评名称<span class="req">*</span></label>
            <input v-model="form.paperName" class="c-input" placeholder="如：2026 年秋季音乐测评" />
          </div>
          <div class="two-col">
            <div class="c-field">
              <label>补录成绩<span class="req">*</span></label>
              <input v-model.number="form.score" type="number" min="0" max="100" step="0.5" class="c-input" placeholder="0 - 100" />
            </div>
            <div class="c-field">
              <label>测评日期<span class="req">*</span></label>
              <input v-model="form.examDate" type="date" class="c-input" />
            </div>
          </div>
          <div class="c-field">
            <label>补录原因<span class="req">*</span></label>
            <select v-model="form.reason" class="c-select">
              <option v-for="r in reasons" :key="r">{{ r }}</option>
            </select>
          </div>
          <div class="c-field">
            <label>情况说明</label>
            <textarea v-model="form.detail" class="c-textarea" rows="3" placeholder="请简要说明补录依据，如考场记录、纸质答卷编号等" />
          </div>
          <button class="c-btn primary submit" @click="submit">
            <AppIcon name="check" :size="16" />提交补录申请
          </button>
          <p class="form-note">
            <AppIcon name="info" :size="14" />
            {{ role === 'school' ? '申请提交后由区县管理员审核，通过后计入测评统计。' : '提交后将直接计入对应学校的测评统计。' }}
          </p>
        </div>
      </article>

      <article class="c-card">
        <header class="c-card-head record-head">
          <div>
            <h3>补录记录</h3>
            <p class="hint">共 {{ filteredRecords.length }} 条记录</p>
          </div>
          <div class="record-tools">
            <label class="c-search">
              <AppIcon name="search" :size="15" />
              <input v-model="keyword" class="c-input" placeholder="搜索学生、学校或测评名称" />
            </label>
          </div>
        </header>

        <div class="c-tabs">
          <button
            v-for="tab in statusTabs"
            :key="tab.key"
            class="c-tab"
            :class="{ active: statusFilter === tab.key }"
            @click="switchStatus(tab.key)"
          >{{ tab.name }}<span class="count">{{ tab.count }}</span></button>
        </div>

        <div v-if="paged.length" class="c-table-wrap">
          <table class="c-table">
            <thead>
              <tr>
                <th>学生</th>
                <th>学校</th>
                <th>学科 / 测评</th>
                <th>补录成绩</th>
                <th>补录原因</th>
                <th>补录时间</th>
                <th>状态</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="rec in paged" :key="rec.id">
                <td>
                  <div class="c-cell-name">{{ rec.studentName }}</div>
                  <div class="c-cell-sub">{{ rec.operator }} 提交</div>
                </td>
                <td class="school-cell">{{ getSchool(rec.schoolId)?.name || '—' }}</td>
                <td>
                  <div>{{ rec.paperName }}</div>
                  <div class="c-cell-sub">{{ rec.subject }} · {{ rec.examDate }}</div>
                </td>
                <td><span class="score">{{ rec.score.toFixed(1) }}</span></td>
                <td>{{ rec.reason }}</td>
                <td class="c-muted c-num time-cell">{{ rec.createdAt }}</td>
                <td>
                  <span class="c-tag" :class="statusMeta(rec.status).tag">
                    <i class="c-dot" />{{ statusMeta(rec.status).label }}
                  </span>
                </td>
                <td>
                  <div class="c-row-actions">
                    <template v-if="rec.status === 'pending'">
                      <button class="c-link-btn" @click="approve(rec)">通过</button>
                      <button class="c-link-btn danger" @click="reject(rec)">驳回</button>
                    </template>
                    <button v-else class="c-link-btn muted" @click="openDetail(rec)">查看</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-else class="c-empty">
          <AppIcon name="edit" :size="38" />
          暂无{{ statusFilter === 'all' ? '' : statusTabs.find(t => t.key === statusFilter)?.name }}补录记录
        </div>

        <div v-if="filteredRecords.length" class="c-pagination">
          <span class="total">第 {{ currentPage }} / {{ totalPages }} 页</span>
          <button class="c-page-btn" :disabled="currentPage === 1" @click="page = currentPage - 1">
            <AppIcon name="chevron-left" :size="14" />
          </button>
          <button
            v-for="n in pageNumbers"
            :key="n"
            class="c-page-btn"
            :class="{ active: n === currentPage }"
            @click="page = n"
          >{{ n }}</button>
          <button class="c-page-btn" :disabled="currentPage === totalPages" @click="page = currentPage + 1">
            <AppIcon name="chevron-right" :size="14" />
          </button>
        </div>
      </article>
    </section>

    <BaseModal v-model="detailOpen" title="补录详情" width="520px">
      <template v-if="detailRecord">
        <ul class="detail-list">
          <li><span>学生</span><b>{{ detailRecord.studentName }}</b></li>
          <li><span>学校</span><b>{{ getSchool(detailRecord.schoolId)?.name }}</b></li>
          <li><span>学科</span><b>{{ detailRecord.subject }}</b></li>
          <li><span>测评名称</span><b>{{ detailRecord.paperName }}</b></li>
          <li><span>补录成绩</span><b>{{ detailRecord.score.toFixed(1) }} 分</b></li>
          <li><span>测评日期</span><b>{{ detailRecord.examDate }}</b></li>
          <li><span>补录原因</span><b>{{ detailRecord.reason }}</b></li>
          <li><span>情况说明</span><b>{{ detailRecord.detail || '—' }}</b></li>
          <li><span>提交人</span><b>{{ detailRecord.operator }}</b></li>
          <li><span>提交时间</span><b>{{ detailRecord.createdAt }}</b></li>
          <li>
            <span>审核状态</span>
            <b><span class="c-tag" :class="statusMeta(detailRecord.status).tag">{{ statusMeta(detailRecord.status).label }}</span></b>
          </li>
        </ul>
      </template>
      <template #footer>
        <button class="c-btn primary" @click="detailOpen = false">知道了</button>
      </template>
    </BaseModal>
  </div>
</template>

<script setup>
import { computed, reactive, ref, watch } from 'vue'
import AppIcon from '../../components/AppIcon.vue'
import BaseModal from '../../components/BaseModal.vue'
import { toast } from '../../data/toast'
import {
  db,
  SCHOOL_ID,
  DISTRICT_ID,
  dateStr,
  downloadCsv,
  getSchool,
  nextId,
  nowStamp,
  roleMeta,
  schoolsForRole
} from '../../data/consoleData'

const props = defineProps({ role: { type: String, default: 'school' } })
const role = computed(() => props.role)

const subtitle = computed(
  () =>
    ({
      school: '为本校缺考、设备故障等原因未提交的学生补录测评成绩',
      district: '审核辖区内学校提交的补录申请，并支持区县统一补录',
      city: '查看全市补录记录，审核并汇总各区县补录数据'
    })[props.role]
)

const reasons = ['缺考未参加', '设备故障未提交', '成绩录入异常', '跨校转学补测']

const form = reactive({
  studentId: '',
  subject: '音乐',
  paperName: '',
  score: null,
  examDate: dateStr(-1),
  reason: '缺考未参加',
  detail: ''
})

const scopeSchoolIds = computed(() => new Set(schoolsForRole(props.role).map(s => s.id)))

const studentOptions = computed(() => {
  const ids = scopeSchoolIds.value
  return db.students.filter(s => ids.has(s.schoolId))
})

watch(
  () => props.role,
  () => {
    resetForm()
    keyword.value = ''
    statusFilter.value = 'all'
    page.value = 1
  }
)

const scopedRecords = computed(() =>
  db.backfills
    .filter(b => scopeSchoolIds.value.has(b.schoolId))
    .slice()
    .sort((a, b) => b.createdAt.localeCompare(a.createdAt))
)

const latestMonth = new Date().toISOString().slice(0, 7)
const monthCount = computed(() => scopedRecords.value.filter(r => r.createdAt.startsWith(latestMonth)).length)
const pendingCount = computed(() => scopedRecords.value.filter(r => r.status === 'pending').length)
const approvalRate = computed(() => {
  const reviewed = scopedRecords.value.filter(r => r.status !== 'pending')
  if (!reviewed.length) return '0.0'
  return ((reviewed.filter(r => r.status === 'approved').length / reviewed.length) * 100).toFixed(1)
})

const statusFilter = ref('all')
const keyword = ref('')
const page = ref(1)
const pageSize = 6

const statusTabs = computed(() => {
  const count = status => scopedRecords.value.filter(r => r.status === status).length
  return [
    { key: 'all', name: '全部', count: scopedRecords.value.length },
    { key: 'pending', name: '待审核', count: count('pending') },
    { key: 'approved', name: '已通过', count: count('approved') },
    { key: 'rejected', name: '已驳回', count: count('rejected') }
  ]
})

const filteredRecords = computed(() => {
  const kw = keyword.value.trim().toLowerCase()
  return scopedRecords.value.filter(r => {
    if (statusFilter.value !== 'all' && r.status !== statusFilter.value) return false
    if (kw) {
      const hay = `${r.studentName} ${getSchool(r.schoolId)?.name || ''} ${r.paperName} ${r.subject}`.toLowerCase()
      if (!hay.includes(kw)) return false
    }
    return true
  })
})

const totalPages = computed(() => Math.max(1, Math.ceil(filteredRecords.value.length / pageSize)))
const currentPage = computed(() => Math.min(page.value, totalPages.value))
const paged = computed(() =>
  filteredRecords.value.slice((currentPage.value - 1) * pageSize, currentPage.value * pageSize)
)
const pageNumbers = computed(() => Array.from({ length: totalPages.value }, (_, i) => i + 1))

watch([keyword, statusFilter], () => {
  page.value = 1
})

function switchStatus(key) {
  statusFilter.value = key
  page.value = 1
}

function statusMeta(status) {
  return {
    pending: { label: '待审核', tag: 'amber' },
    approved: { label: '已通过', tag: 'green' },
    rejected: { label: '已驳回', tag: 'red' }
  }[status] || { label: '未知', tag: 'gray' }
}

function submit() {
  const student = db.students.find(s => s.id === form.studentId)
  if (!student) return toast('请选择需要补录的学生', 'error')
  if (!form.paperName.trim()) return toast('请填写测评名称', 'error')
  if (form.score === null || form.score === '' || Number.isNaN(Number(form.score))) return toast('请填写补录成绩', 'error')
  const score = Number(form.score)
  if (score < 0 || score > 100) return toast('补录成绩需在 0 - 100 之间', 'error')
  if (!form.examDate) return toast('请选择测评日期', 'error')

  db.backfills.unshift({
    id: nextId('bf'),
    schoolId: student.schoolId,
    studentId: student.id,
    studentName: student.name,
    subject: form.subject,
    paperName: form.paperName,
    score,
    examDate: form.examDate,
    reason: form.reason,
    detail: form.detail,
    status: 'pending',
    operator: props.role === 'school' ? '王海燕' : props.role === 'district' ? '李建国' : '何文博',
    createdAt: nowStamp()
  })
  toast('补录申请已提交')
  resetForm()
  statusFilter.value = 'all'
  page.value = 1
}

function resetForm() {
  form.studentId = ''
  form.subject = '音乐'
  form.paperName = ''
  form.score = null
  form.examDate = dateStr(-1)
  form.reason = '缺考未参加'
  form.detail = ''
}

function approve(rec) {
  rec.status = 'approved'
  toast(`已通过 ${rec.studentName} 的补录申请`)
}

function reject(rec) {
  rec.status = 'rejected'
  toast(`已驳回 ${rec.studentName} 的补录申请`, 'warning')
}

const detailOpen = ref(false)
const detailRecord = ref(null)
function openDetail(rec) {
  detailRecord.value = rec
  detailOpen.value = true
}

function exportRecords() {
  if (!filteredRecords.value.length) return toast('当前没有可导出的补录记录', 'error')
  downloadCsv(
    '艺术测评补录记录.csv',
    ['学生', '学校', '学科', '测评名称', '补录成绩', '测评日期', '补录原因', '提交人', '提交时间', '状态'],
    filteredRecords.value.map(r => [
      r.studentName,
      getSchool(r.schoolId)?.name || '',
      r.subject,
      r.paperName,
      r.score.toFixed(1),
      r.examDate,
      r.reason,
      r.operator,
      r.createdAt,
      statusMeta(r.status).label
    ])
  )
  toast('补录记录已导出')
}
</script>

<style scoped>
.c-kpi-grid.three {
  grid-template-columns: repeat(3, 1fr);
}
.backfill-layout {
  display: grid;
  grid-template-columns: 350px minmax(0, 1fr);
  gap: 14px;
  align-items: start;
}
.form-card {
  position: sticky;
  top: 78px;
}
.form-stack {
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.two-col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}
.submit {
  margin-top: 2px;
}
.form-note {
  display: flex;
  align-items: flex-start;
  gap: 6px;
  margin: 0;
  font-size: 11.5px;
  line-height: 1.6;
  color: #86909c;
}
.form-note svg {
  flex: none;
  margin-top: 1px;
  color: #1677ff;
}
.record-head {
  align-items: flex-start;
}
.record-tools {
  display: flex;
  gap: 8px;
}
.record-tools .c-input {
  width: 210px;
}
.school-cell {
  max-width: 170px;
  font-size: 12.5px;
  line-height: 1.5;
}
.score {
  font-size: 14px;
  font-weight: 700;
  color: #1677ff;
  font-variant-numeric: tabular-nums;
}
.time-cell {
  font-size: 11.5px;
  white-space: nowrap;
}
.detail-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 11px;
}
.detail-list li {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 20px;
  font-size: 12.5px;
}
.detail-list span {
  flex: none;
  color: #86909c;
}
.detail-list b {
  text-align: right;
  font-weight: 500;
  color: #1f2329;
  line-height: 1.6;
}
@media (max-width: 1180px) {
  .backfill-layout {
    grid-template-columns: 1fr;
  }
  .form-card {
    position: static;
  }
  .record-tools .c-input {
    width: 180px;
  }
}
@media (max-width: 760px) {
  .c-kpi-grid.three {
    grid-template-columns: 1fr;
  }
  .record-head {
    flex-direction: column;
  }
  .record-tools,
  .record-tools .c-search,
  .record-tools .c-input {
    width: 100%;
  }
}
</style>
