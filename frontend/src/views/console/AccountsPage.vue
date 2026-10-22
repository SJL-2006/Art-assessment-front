<template>
  <div class="c-page">
    <header class="c-page-head">
      <div>
        <h2>账号管理</h2>
        <p class="sub">{{ subtitle }}</p>
      </div>
      <div class="actions">
        <button v-if="active === 'teacher'" class="c-btn outline" @click="openBatch">
          <AppIcon name="upload" :size="16" />批量创建
        </button>
        <button class="c-btn primary" @click="openCreate">
          <AppIcon name="plus" :size="16" />新增{{ entityName }}
        </button>
      </div>
    </header>

    <section class="c-card">
      <div class="c-tabs">
        <button
          v-for="tab in tabs"
          :key="tab.key"
          class="c-tab"
          :class="{ active: active === tab.key }"
          @click="switchTab(tab.key)"
        >
          {{ tab.name }}<span class="count">{{ countOf(tab.key) }}</span>
        </button>
      </div>

      <div class="c-toolbar">
        <label class="c-search">
          <AppIcon name="search" :size="15" />
          <input v-model="keyword" class="c-input" :placeholder="searchPlaceholder" />
        </label>
        <select v-if="active === 'teacher'" v-model="subjectFilter" class="c-select">
          <option value="">全部学科</option>
          <option v-for="s in subjectsPool" :key="s">{{ s }}</option>
        </select>
        <select v-if="active === 'teacher' || active === 'student'" v-model="gradeFilter" class="c-select">
          <option value="">全部年级</option>
          <option v-for="g in grades" :key="g">{{ g }}</option>
        </select>
        <select v-model="statusFilter" class="c-select">
          <option value="">全部状态</option>
          <option>正常</option>
          <option>停用</option>
        </select>
        <div class="spacer" />
        <span class="c-muted">共 {{ filtered.length }} 条</span>
        <button class="c-btn ghost sm" @click="resetFilters">
          <AppIcon name="refresh" :size="14" />重置
        </button>
      </div>

      <div v-if="paged.length" class="c-table-wrap">
        <table class="c-table">
          <thead>
            <tr>
              <th v-for="col in columns" :key="col.label">{{ col.label }}</th>
              <th>状态</th>
              <th>创建时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in paged" :key="row.id">
              <td v-for="(col, idx) in columns" :key="col.label">
                <div v-if="idx === 0" class="c-cell-main">
                  <span class="c-avatar" :class="toneOf(row)">{{ row.name?.charAt(0) || '艺' }}</span>
                  <div>
                    <div class="c-cell-name">{{ col.get(row) }}</div>
                    <div class="c-cell-sub">{{ subLine(row) }}</div>
                  </div>
                </div>
                <span v-else class="c-num">{{ col.get(row) }}</span>
              </td>
              <td>
                <span class="c-tag" :class="row.status === '正常' ? 'green' : 'gray'">
                  <i class="c-dot" />{{ row.status }}
                </span>
              </td>
              <td class="c-muted c-num">{{ row.createdAt }}</td>
              <td>
                <div class="c-row-actions">
                  <button class="c-link-btn" @click="openEdit(row)">编辑</button>
                  <button class="c-link-btn muted" @click="askReset(row)">重置密码</button>
                  <button class="c-link-btn danger" @click="askDelete(row)">删除</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="c-empty">
        <AppIcon name="users" :size="38" />
        没有找到匹配的账号
      </div>

      <div v-if="filtered.length" class="c-pagination">
        <span class="total">共 {{ filtered.length }} 条 · 第 {{ currentPage }} / {{ totalPages }} 页</span>
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
    </section>

    <BaseModal
      v-model="formOpen"
      :title="editingId ? `编辑${entityName}` : `新增${entityName}`"
      :subtitle="formSubtitle"
      width="620px"
    >
      <div class="c-form-grid">
        <div class="c-field">
          <label>{{ active === 'school' ? '学校名称' : active === 'district' ? '区县名称' : '姓名' }}<span class="req">*</span></label>
          <input v-model="form.name" class="c-input" :placeholder="active === 'school' ? '请输入学校全称' : active === 'district' ? '请输入区县名称' : '请输入姓名'" />
        </div>
        <div v-if="active === 'student'" class="c-field">
          <label>学籍号<span class="req">*</span></label>
          <input v-model="form.studentNo" class="c-input" placeholder="请输入学籍号" />
        </div>
        <div v-else-if="active === 'school' || active === 'district'" class="c-field">
          <label>{{ active === 'school' ? '学校编码' : '区县编码' }}<span class="req">*</span></label>
          <input v-model="form.code" class="c-input" placeholder="如 YZQ004" />
        </div>
        <div v-else class="c-field">
          <label>手机号</label>
          <input v-model="form.phone" class="c-input" placeholder="请输入手机号" />
        </div>

        <div v-if="active === 'teacher' || active === 'student'" class="c-field">
          <label>登录账号<span class="req">*</span></label>
          <input v-model="form.account" class="c-input" placeholder="用于登录系统" />
        </div>
        <div v-else class="c-field">
          <label>负责人<span class="req">*</span></label>
          <input v-model="form.manager" class="c-input" placeholder="请输入负责人姓名" />
        </div>

        <template v-if="active === 'teacher'">
          <div class="c-field">
            <label>任教学科</label>
            <select v-model="form.subject" class="c-select">
              <option v-for="s in subjectsPool" :key="s">{{ s }}</option>
            </select>
          </div>
          <div class="c-field">
            <label>任教年级</label>
            <select v-model="form.grade" class="c-select">
              <option v-for="g in grades" :key="g">{{ g }}</option>
            </select>
          </div>
          <div class="c-field">
            <label>教师角色</label>
            <select v-model="form.role" class="c-select">
              <option>班主任</option>
              <option>科任教师</option>
            </select>
          </div>
        </template>

        <template v-if="active === 'student'">
          <div class="c-field">
            <label>年级</label>
            <select v-model="form.grade" class="c-select">
              <option v-for="g in grades" :key="g">{{ g }}</option>
            </select>
          </div>
          <div class="c-field">
            <label>班级</label>
            <input v-model="form.className" class="c-input" placeholder="如 八年级(2)班" />
          </div>
          <div class="c-field">
            <label>性别</label>
            <select v-model="form.gender" class="c-select">
              <option>女</option>
              <option>男</option>
            </select>
          </div>
        </template>

        <template v-if="active === 'school'">
          <div class="c-field">
            <label>所属区县</label>
            <select v-model="form.districtId" class="c-select" :disabled="role === 'district'">
              <option value="">市直属</option>
              <option v-for="d in districts" :key="d.id" :value="d.id">{{ d.name }}</option>
            </select>
          </div>
          <div class="c-field">
            <label>登录账号<span class="req">*</span></label>
            <input v-model="form.account" class="c-input" placeholder="学校管理员登录账号" />
          </div>
          <div class="c-field">
            <label>手机号</label>
            <input v-model="form.phone" class="c-input" placeholder="请输入手机号" />
          </div>
        </template>

        <template v-if="active === 'district'">
          <div class="c-field">
            <label>登录账号<span class="req">*</span></label>
            <input v-model="form.account" class="c-input" placeholder="区县管理员登录账号" />
          </div>
          <div class="c-field">
            <label>手机号</label>
            <input v-model="form.phone" class="c-input" placeholder="请输入手机号" />
          </div>
        </template>

        <div class="c-field">
          <label>账号状态</label>
          <select v-model="form.status" class="c-select">
            <option>正常</option>
            <option>停用</option>
          </select>
        </div>
        <div v-if="!editingId" class="c-field">
          <label>初始密码</label>
          <input v-model="form.password" class="c-input" placeholder="默认 Art@2026" />
          <span class="tip">首次登录后需修改密码</span>
        </div>
      </div>
      <template #footer>
        <button class="c-btn ghost" @click="formOpen = false">取消</button>
        <button class="c-btn primary" @click="saveForm">保存</button>
      </template>
    </BaseModal>

    <BaseModal v-model="batchOpen" title="批量创建教师账号" subtitle="每行一个账号，格式：姓名,手机号,学科" width="560px">
      <div class="c-field">
        <label>账号列表<span class="req">*</span></label>
        <textarea
          v-model="batchText"
          class="c-textarea"
          rows="7"
          placeholder="张老师,13800001111,音乐&#10;李老师,13800002222,美术&#10;王老师,13800003333,音乐"
        />
        <span class="tip">系统将自动生成登录账号，初始密码为 Art@2026</span>
      </div>
      <template #footer>
        <button class="c-btn ghost" @click="batchOpen = false">取消</button>
        <button class="c-btn primary" @click="submitBatch">批量创建</button>
      </template>
    </BaseModal>

    <BaseModal v-model="confirmOpen" :title="confirmTitle" width="420px">
      <p class="confirm-text">{{ confirmText }}</p>
      <template #footer>
        <button class="c-btn ghost" @click="confirmOpen = false">取消</button>
        <button class="c-btn" :class="confirmAction?.type === 'delete' ? 'danger' : 'primary'" @click="runConfirm">
          {{ confirmAction?.type === 'delete' ? '确认删除' : '确认重置' }}
        </button>
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
  DISTRICT_ID,
  SCHOOL_ID,
  districts,
  grades,
  schoolsOfDistrict,
  nextId,
  dateStr
} from '../../data/consoleData'

const props = defineProps({ role: { type: String, default: 'school' } })

const subjectsPool = ['音乐', '美术', '语文', '数学']

const tabs = computed(() => {
  if (props.role === 'school') return [
    { key: 'teacher', name: '教师账号' },
    { key: 'student', name: '学生账号' }
  ]
  if (props.role === 'district') return [{ key: 'school', name: '学校账号' }]
  return [
    { key: 'district', name: '区县账号' },
    { key: 'school', name: '市直属学校' }
  ]
})

const role = computed(() => props.role)
const active = ref('teacher')
const keyword = ref('')
const subjectFilter = ref('')
const gradeFilter = ref('')
const statusFilter = ref('')
const page = ref(1)
const pageSize = 8

watch(
  () => props.role,
  () => {
    active.value = tabs.value[0].key
    resetFilters()
  },
  { immediate: true }
)

function switchTab(key) {
  active.value = key
  resetFilters()
}

const entityName = computed(() => {
  if (active.value === 'teacher') return '教师账号'
  if (active.value === 'student') return '学生账号'
  if (active.value === 'district') return '区县账号'
  return role.value === 'city' ? '市直属学校' : '学校账号'
})

const subtitle = computed(() => {
  if (props.role === 'school') return '管理本校教师与学生账号，支持批量创建、密码重置与状态维护'
  if (props.role === 'district') return '管理云州区各学校管理员账号，按学校维度统一维护'
  return '管理区县账号与市直属学校账号，支持三级地区架构下的统一账号体系'
})

const searchPlaceholder = computed(() =>
  active.value === 'teacher' || active.value === 'student' ? '搜索姓名、账号或手机号' : '搜索名称、编码或负责人'
)

const sourceList = computed(() => {
  if (active.value === 'teacher') return db.teachers.filter(t => t.schoolId === SCHOOL_ID)
  if (active.value === 'student') return db.students.filter(s => s.schoolId === SCHOOL_ID)
  if (active.value === 'district') return db.districtAccounts
  if (props.role === 'district') return db.schoolAccounts.filter(s => s.districtId === DISTRICT_ID)
  return db.schoolAccounts.filter(s => s.direct)
})

const filtered = computed(() => {
  const kw = keyword.value.trim().toLowerCase()
  return sourceList.value.filter(row => {
    if (kw) {
      const hay = [row.name, row.account, row.phone, row.manager, row.code, row.studentNo].join(' ').toLowerCase()
      if (!hay.includes(kw)) return false
    }
    if (statusFilter.value && row.status !== statusFilter.value) return false
    if (subjectFilter.value && row.subject !== subjectFilter.value) return false
    if (gradeFilter.value && row.grade !== gradeFilter.value) return false
    return true
  })
})

const totalPages = computed(() => Math.max(1, Math.ceil(filtered.value.length / pageSize)))
const currentPage = computed(() => Math.min(page.value, totalPages.value))
const paged = computed(() => filtered.value.slice((currentPage.value - 1) * pageSize, currentPage.value * pageSize))
const pageNumbers = computed(() => Array.from({ length: totalPages.value }, (_, i) => i + 1))

function countOf(key) {
  if (key === 'teacher') return db.teachers.filter(t => t.schoolId === SCHOOL_ID).length
  if (key === 'student') return db.students.filter(s => s.schoolId === SCHOOL_ID).length
  if (key === 'district') return db.districtAccounts.length
  if (props.role === 'district') return db.schoolAccounts.filter(s => s.districtId === DISTRICT_ID).length
  return db.schoolAccounts.filter(s => s.direct).length
}

const columns = computed(() => {
  if (active.value === 'teacher') return [
    { label: '姓名', get: r => r.name },
    { label: '登录账号', get: r => r.account },
    { label: '任教学科', get: r => r.subject },
    { label: '任教年级', get: r => r.grade },
    { label: '教师角色', get: r => r.role },
    { label: '手机号', get: r => r.phone }
  ]
  if (active.value === 'student') return [
    { label: '姓名', get: r => r.name },
    { label: '学籍号', get: r => r.studentNo },
    { label: '登录账号', get: r => r.account },
    { label: '年级班级', get: r => r.className },
    { label: '性别', get: r => r.gender }
  ]
  if (active.value === 'district') return [
    { label: '区县名称', get: r => r.name },
    { label: '区县编码', get: r => r.code },
    { label: '负责人', get: r => r.manager },
    { label: '登录账号', get: r => r.account },
    { label: '学校数', get: r => `${schoolsOfDistrict(r.id).length} 所` },
    { label: '手机号', get: r => r.phone }
  ]
  return [
    { label: '学校名称', get: r => r.name },
    { label: '学校编码', get: r => r.code },
    { label: '所属区县', get: r => (r.districtId ? districts.find(d => d.id === r.districtId)?.name : '市直属') },
    { label: '负责人', get: r => r.manager },
    { label: '登录账号', get: r => r.account },
    { label: '手机号', get: r => r.phone }
  ]
})

function subLine(row) {
  if (active.value === 'teacher') return `${row.subject}学科 · ${row.role}`
  if (active.value === 'student') return row.studentNo
  if (active.value === 'district') return `${schoolsOfDistrict(row.id).length} 所学校`
  return row.code
}

function toneOf(row) {
  const tones = ['', 'green', 'amber', 'pink']
  const code = (row.name || '').charCodeAt(0) || 0
  return tones[code % tones.length]
}

function resetFilters() {
  keyword.value = ''
  subjectFilter.value = ''
  gradeFilter.value = ''
  statusFilter.value = ''
  page.value = 1
}

watch([keyword, subjectFilter, gradeFilter, statusFilter], () => {
  page.value = 1
})

/* ==================== 表单 ==================== */
const formOpen = ref(false)
const editingId = ref(null)
const form = reactive({})

const formSubtitle = computed(() => {
  if (editingId.value) return '修改账号基础信息，保存后立即生效'
  if (active.value === 'teacher' || active.value === 'student') return '账号创建后可通过手机号找回密码'
  return '账号将纳入三级地区架构统一管理'
})

function defaults() {
  if (active.value === 'teacher') {
    return { name: '', account: '', phone: '', subject: '音乐', grade: '七年级', role: '科任教师', status: '正常', password: '' }
  }
  if (active.value === 'student') {
    return { name: '', studentNo: '', account: '', grade: '七年级', className: '七年级(1)班', gender: '女', status: '正常', password: '' }
  }
  if (active.value === 'district') {
    return { name: '', code: '', manager: '', account: '', phone: '', status: '正常', password: '' }
  }
  return { name: '', code: '', districtId: props.role === 'district' ? DISTRICT_ID : '', manager: '', account: '', phone: '', status: '正常', password: '' }
}

function openCreate() {
  editingId.value = null
  Object.keys(form).forEach(k => delete form[k])
  Object.assign(form, defaults())
  formOpen.value = true
}

function openEdit(row) {
  editingId.value = row.id
  Object.keys(form).forEach(k => delete form[k])
  Object.assign(form, {
    ...row,
    password: '',
    districtId: row.districtId ?? ''
  })
  formOpen.value = true
}

function storeOf() {
  if (active.value === 'teacher') return db.teachers
  if (active.value === 'student') return db.students
  if (active.value === 'district') return db.districtAccounts
  return db.schoolAccounts
}

function saveForm() {
  if (!form.name?.trim()) return toast('请填写名称或姓名', 'error')
  if (active.value !== 'school' && active.value !== 'district' && !form.account?.trim()) return toast('请填写登录账号', 'error')
  if (active.value === 'school' && !form.account?.trim()) return toast('请填写学校登录账号', 'error')
  if (active.value === 'district' && !form.account?.trim()) return toast('请填写区县登录账号', 'error')

  const store = storeOf()
  if (editingId.value) {
    const target = store.find(r => r.id === editingId.value)
    if (target) {
      const { password, ...rest } = form
      Object.assign(target, rest)
      if (active.value === 'school' && props.role === 'city') {
        target.direct = !target.districtId
      }
    }
    toast(`${entityName.value}已更新`)
  } else {
    const record = {
      ...form,
      id: nextId(active.value),
      status: form.status || '正常',
      createdAt: dateStr()
    }
    delete record.password
    if (active.value === 'teacher' || active.value === 'student') record.schoolId = SCHOOL_ID
    if (active.value === 'school') {
      record.direct = !record.districtId
      if (props.role === 'district') record.districtId = DISTRICT_ID
    }
    store.push(record)
    toast(`${entityName.value}创建成功，初始密码 Art@2026`)
  }
  formOpen.value = false
}

/* ==================== 批量创建 ==================== */
const batchOpen = ref(false)
const batchText = ref('')

function openBatch() {
  batchText.value = ''
  batchOpen.value = true
}

function submitBatch() {
  const lines = batchText.value.split('\n').map(l => l.trim()).filter(Boolean)
  if (!lines.length) return toast('请至少输入一行账号信息', 'error')
  let added = 0
  lines.forEach((line, i) => {
    const parts = line.split(/[,，\s]+/).filter(Boolean)
    const name = parts[0]
    if (!name) return
    db.teachers.push({
      id: nextId('teacher'),
      schoolId: SCHOOL_ID,
      name,
      account: `newteacher${Date.now().toString(36).slice(-4)}${i}`,
      phone: parts[1] || '',
      subject: parts[2] || '音乐',
      grade: '七年级',
      role: '科任教师',
      status: '正常',
      createdAt: dateStr()
    })
    added++
  })
  batchOpen.value = false
  toast(`成功创建 ${added} 个教师账号`)
}

/* ==================== 确认操作 ==================== */
const confirmOpen = ref(false)
const confirmAction = ref(null)
const confirmTitle = computed(() =>
  confirmAction.value?.type === 'delete' ? `删除${entityName.value}` : '重置登录密码'
)
const confirmText = computed(() => {
  if (!confirmAction.value) return ''
  const name = confirmAction.value.row.name
  return confirmAction.value.type === 'delete'
    ? `确定要删除「${name}」的账号吗？删除后该账号将无法登录，且相关测评数据仍会保留。`
    : `确定要将「${name}」的登录密码重置为初始密码吗？`
})

function askDelete(row) {
  confirmAction.value = { type: 'delete', row }
  confirmOpen.value = true
}
function askReset(row) {
  confirmAction.value = { type: 'reset', row }
  confirmOpen.value = true
}
function runConfirm() {
  const action = confirmAction.value
  if (!action) return
  if (action.type === 'delete') {
    const store = storeOf()
    const index = store.findIndex(r => r.id === action.row.id)
    if (index > -1) store.splice(index, 1)
    toast('账号已删除')
  } else {
    toast('密码已重置，初始密码：Art@2026')
  }
  confirmOpen.value = false
}
</script>

<style scoped>
.confirm-text {
  margin: 0;
  font-size: 13.5px;
  line-height: 1.75;
  color: #4e5969;
}
</style>
