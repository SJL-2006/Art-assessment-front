<template>
  <div class="c-page">
    <header class="c-page-head">
      <div>
        <h2>组卷管理</h2>
        <p class="sub">{{ subtitle }}</p>
      </div>
      <div class="actions">
        <button class="c-btn outline" @click="openCreate('manual')">
          <AppIcon name="edit" :size="16" />手动组卷
        </button>
        <button class="c-btn primary" @click="openCreate('auto')">
          <AppIcon name="spark" :size="16" />智能组卷
        </button>
      </div>
    </header>

    <section class="c-card">
      <div class="c-tabs">
        <button
          v-for="tab in tabOptions"
          :key="tab.key"
          class="c-tab"
          :class="{ active: activeTab === tab.key }"
          @click="activeTab = tab.key"
        >
          {{ tab.name }}<span class="count">{{ tab.count }}</span>
        </button>
      </div>

      <div class="c-toolbar">
        <label class="c-search">
          <AppIcon name="search" :size="15" />
          <input v-model="keyword" class="c-input" placeholder="搜索试卷名称或创建人" />
        </label>
        <select v-model="subjectFilter" class="c-select">
          <option value="">全部学科</option>
          <option>音乐</option>
          <option>美术</option>
        </select>
        <select v-model="gradeFilter" class="c-select">
          <option value="">全部年级</option>
          <option v-for="g in grades" :key="g">{{ g }}</option>
        </select>
        <div class="spacer" />
        <span class="c-muted">共 {{ filtered.length }} 份试卷</span>
      </div>

      <div v-if="filtered.length" class="c-table-wrap">
        <table class="c-table">
          <thead>
            <tr>
              <th>试卷名称</th>
              <th>年级</th>
              <th>组卷方式</th>
              <th>难度</th>
              <th>题量</th>
              <th>总分</th>
              <th>状态</th>
              <th>创建时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in filtered" :key="p.id">
              <td>
                <div class="c-cell-main">
                  <span class="paper-icon" :class="p.subject === '音乐' ? 'blue' : 'pink'">
                    <AppIcon :name="p.subject === '音乐' ? 'music' : 'palette'" :size="17" />
                  </span>
                  <div>
                    <div class="c-cell-name">{{ p.name }}</div>
                    <div class="c-cell-sub">{{ p.creator }} · {{ p.subject }}测评</div>
                  </div>
                </div>
              </td>
              <td>{{ p.grade }}</td>
              <td>{{ p.mode }}</td>
              <td>
                <span class="c-tag" :class="difficultyTag(p.difficulty)">{{ p.difficulty }}</span>
              </td>
              <td class="c-num">{{ p.questionCount }} 题</td>
              <td class="c-num">{{ p.totalScore }} 分</td>
              <td>
                <span class="c-tag" :class="p.status === 'published' ? 'green' : 'amber'">
                  <i class="c-dot" />{{ p.status === 'published' ? '已发布' : '草稿' }}
                </span>
              </td>
              <td class="c-muted c-num">{{ p.createdAt }}</td>
              <td>
                <div class="c-row-actions">
                  <button class="c-link-btn" @click="openView(p)">查看</button>
                  <button class="c-link-btn muted" @click="openEdit(p)">编辑</button>
                  <button class="c-link-btn muted" @click="downloadAnswers(p)">下载答案</button>
                  <button class="c-link-btn danger" @click="askDelete(p)">删除</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="c-empty">
        <AppIcon name="paper" :size="38" />
        暂无符合条件的试卷，试试新建一份吧
      </div>
    </section>

    <BaseModal v-model="formOpen" :title="editingId ? '编辑试卷' : '创建测评试卷'" :subtitle="formSubtitle" width="680px">
      <div class="c-form-grid">
        <div class="c-field full">
          <label>试卷名称<span class="req">*</span></label>
          <input v-model="form.name" class="c-input" placeholder="如：2026 年秋季八年级音乐测评卷" />
        </div>
        <div class="c-field full">
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
          <label>适用年级</label>
          <select v-model="form.grade" class="c-select">
            <option v-for="g in grades" :key="g">{{ g }}</option>
          </select>
        </div>
        <div class="c-field">
          <label>难度水平</label>
          <select v-model="form.difficulty" class="c-select">
            <option>简单</option>
            <option>中等</option>
            <option>较难</option>
          </select>
        </div>
        <div class="c-field full">
          <label>组卷方式</label>
          <div class="c-segmented">
            <button class="item" :class="{ active: form.mode === '自动组卷' }" @click="form.mode = '自动组卷'">自动组卷</button>
            <button class="item" :class="{ active: form.mode === '手动组卷' }" @click="form.mode = '手动组卷'">手动组卷</button>
          </div>
        </div>
        <div class="c-field">
          <label>题目数量</label>
          <input v-model.number="form.questionCount" type="number" min="5" max="60" class="c-input" />
        </div>
        <div class="c-field">
          <label>预计总分</label>
          <div class="score-preview">{{ previewScore }} <span>分</span></div>
        </div>
        <div class="c-field full">
          <div class="mode-hint">
            <AppIcon :name="form.mode === '自动组卷' ? 'spark' : 'list'" :size="16" />
            <span v-if="form.mode === '自动组卷'">
              系统将按「简单 40% · 中等 40% · 较难 20%」的比例，从{{ roleName }}题库中自动抽取 {{ form.questionCount || 0 }} 道题。
            </span>
            <span v-else>
              保存后进入手动组卷，可逐题从题库挑选，当前先按 {{ form.questionCount || 0 }} 题预估分值。
            </span>
          </div>
        </div>
      </div>
      <template #footer>
        <button class="c-btn ghost" @click="formOpen = false">取消</button>
        <button class="c-btn primary" @click="saveForm">保存草稿</button>
      </template>
    </BaseModal>

    <BaseModal v-model="viewOpen" :title="current?.name || '试卷详情'" subtitle="试卷信息与试题预览" width="780px">
      <template v-if="current">
        <div class="paper-meta">
          <div v-for="item in paperMeta" :key="item.label" class="meta-item">
            <span>{{ item.label }}</span>
            <b>{{ item.value }}</b>
          </div>
        </div>

        <div class="question-head">
          <h4>试题预览</h4>
          <span class="c-muted">展示前 {{ current.questions.length }} 题 · 共 {{ current.questionCount }} 题</span>
        </div>
        <ul class="question-list">
          <li v-for="q in current.questions" :key="q.no">
            <div class="q-top">
              <span class="q-no">{{ q.no }}</span>
              <span class="c-tag blue">{{ q.type }}</span>
              <span class="c-tag" :class="difficultyTag(q.difficulty)">{{ q.difficulty }}</span>
            </div>
            <p class="q-stem">{{ q.stem }}</p>
            <div class="q-options">
              <span v-for="opt in q.options" :key="opt">{{ opt }}</span>
            </div>
            <p class="q-answer">答案：{{ q.answer }}　·　解析：{{ q.analysis }}</p>
          </li>
        </ul>
      </template>
      <template #footer>
        <button class="c-btn ghost" @click="downloadMaterials(current)">下载材料</button>
        <button class="c-btn outline" @click="downloadAnswers(current)">下载答案</button>
        <button v-if="current?.status === 'draft'" class="c-btn primary" @click="goPublish">
          发布该测评
        </button>
        <button v-else class="c-btn soft" @click="goPublish">再发布一次</button>
      </template>
    </BaseModal>

    <BaseModal v-model="confirmOpen" title="删除试卷" width="420px">
      <p class="confirm-text">
        确定要删除「{{ deleteTarget?.name }}」吗？删除后该试卷不可恢复，已发布的测评记录不受影响。
      </p>
      <template #footer>
        <button class="c-btn ghost" @click="confirmOpen = false">取消</button>
        <button class="c-btn danger" @click="confirmDelete">确认删除</button>
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
  grades,
  makeQuestions,
  nextId,
  dateStr,
  downloadText
} from '../../data/consoleData'

const props = defineProps({ role: { type: String, default: 'school' } })
const emit = defineEmits(['navigate'])

const roleName = computed(() => (props.role === 'school' ? '学校' : props.role === 'district' ? '区县' : '市州'))

const subtitle = computed(
  () =>
    ({
      school:
        '维护学校级测评试卷，支持自动/手动组卷、试题解析查看与音视频材料下载',
      district: '统筹区县级测评试卷，可复用同一套组卷模板向辖区内学校下发',
      city: '管理市州级统考试卷，支持按区县、学校逐级发布与复用'
    })[props.role]
)

const activeTab = ref('all')
const keyword = ref('')
const subjectFilter = ref('')
const gradeFilter = ref('')
const formOpen = ref(false)
const viewOpen = ref(false)
const confirmOpen = ref(false)
const editingId = ref(null)
const current = ref(null)
const deleteTarget = ref(null)
const form = reactive({})

watch(
  () => props.role,
  () => {
    activeTab.value = 'all'
    keyword.value = ''
    subjectFilter.value = ''
    gradeFilter.value = ''
  }
)

const rolePapers = computed(() => db.papers.filter(p => p.level === props.role))

const tabOptions = computed(() => [
  { key: 'all', name: '全部试卷', count: rolePapers.value.length },
  { key: 'draft', name: '草稿', count: rolePapers.value.filter(p => p.status === 'draft').length },
  { key: 'published', name: '已发布', count: rolePapers.value.filter(p => p.status === 'published').length }
])

const filtered = computed(() => {
  const kw = keyword.value.trim().toLowerCase()
  return rolePapers.value
    .filter(p => {
      if (activeTab.value !== 'all' && p.status !== activeTab.value) return false
      if (subjectFilter.value && p.subject !== subjectFilter.value) return false
      if (gradeFilter.value && p.grade !== gradeFilter.value) return false
      if (kw && !`${p.name} ${p.creator}`.toLowerCase().includes(kw)) return false
      return true
    })
    .slice()
    .sort((a, b) => b.createdAt.localeCompare(a.createdAt))
})

const paperMeta = computed(() => {
  if (!current.value) return []
  const p = current.value
  return [
    { label: '学科', value: p.subject },
    { label: '年级', value: p.grade },
    { label: '组卷方式', value: p.mode },
    { label: '难度', value: p.difficulty },
    { label: '题量 / 总分', value: `${p.questionCount} 题 / ${p.totalScore} 分` },
    { label: '创建人', value: p.creator },
    { label: '状态', value: p.status === 'published' ? '已发布' : '草稿' },
    { label: '创建时间', value: p.createdAt }
  ]
})

const formSubtitle = computed(() =>
  editingId.value ? '修改试卷信息不会影响已发布的测评记录' : `当前身份：${roleName.value}端 · 试卷将保存在${roleName.value}级题库`
)

const previewScore = computed(() => {
  const count = Number(form.questionCount) || 0
  const each = form.subject === '音乐' ? 2 : 4
  return count * each
})

function difficultyTag(level) {
  if (level === '简单') return 'green'
  if (level === '较难') return 'red'
  return 'amber'
}

function openCreate(mode) {
  editingId.value = null
  Object.keys(form).forEach(k => delete form[k])
  Object.assign(form, {
    name: '',
    subject: '音乐',
    grade: '八年级',
    mode: mode === 'manual' ? '手动组卷' : '自动组卷',
    difficulty: '中等',
    questionCount: 30
  })
  formOpen.value = true
}

function openEdit(paper) {
  editingId.value = paper.id
  Object.keys(form).forEach(k => delete form[k])
  Object.assign(form, {
    name: paper.name,
    subject: paper.subject,
    grade: paper.grade,
    mode: paper.mode,
    difficulty: paper.difficulty,
    questionCount: paper.questionCount
  })
  formOpen.value = true
}

function saveForm() {
  if (!form.name?.trim()) return toast('请填写试卷名称', 'error')
  const count = Number(form.questionCount)
  if (!count || count < 5 || count > 60) return toast('题目数量需在 5 - 60 之间', 'error')

  if (editingId.value) {
    const paper = db.papers.find(p => p.id === editingId.value)
    if (paper) {
      const subjectChanged = paper.subject !== form.subject
      Object.assign(paper, {
        name: form.name,
        subject: form.subject,
        grade: form.grade,
        mode: form.mode,
        difficulty: form.difficulty,
        questionCount: count,
        totalScore: previewScore.value
      })
      if (subjectChanged || !paper.questions?.length) paper.questions = makeQuestions(form.subject)
    }
    toast('试卷信息已更新')
  } else {
    const creator = props.role === 'school' ? '王海燕' : props.role === 'district' ? '李建国' : '市教科院'
    db.papers.push({
      id: nextId('paper'),
      level: props.role,
      name: form.name,
      subject: form.subject,
      grade: form.grade,
      mode: form.mode,
      difficulty: form.difficulty,
      questionCount: count,
      scoreEach: form.subject === '音乐' ? 2 : 4,
      totalScore: previewScore.value,
      status: 'draft',
      creator,
      createdAt: dateStr(),
      questions: makeQuestions(form.subject)
    })
    toast('试卷已保存为草稿')
  }
  formOpen.value = false
}

function openView(paper) {
  current.value = paper
  viewOpen.value = true
}

function downloadAnswers(paper) {
  if (!paper) return
  const lines = [
    `${paper.name} · 参考答案`,
    `学科：${paper.subject}　年级：${paper.grade}　题量：${paper.questionCount}　总分：${paper.totalScore}`,
    ''
  ]
  paper.questions.forEach(q => {
    lines.push(`${q.no}. [${q.type} / ${q.difficulty}] ${q.stem}`)
    lines.push(`答案：${q.answer}`)
    lines.push(`解析：${q.analysis}`)
    lines.push('')
  })
  downloadText(`${paper.name}-参考答案.txt`, lines.join('\n'))
  toast('参考答案已开始下载')
}

function downloadMaterials(paper) {
  if (!paper) return
  const lines = [
    `${paper.name} · 测评材料清单`,
    `学科：${paper.subject}　年级：${paper.grade}`,
    ''
  ]
  if (paper.subject === '音乐') {
    lines.push('音频材料：', '01_乐曲片段一.mp3', '02_乐曲片段二.mp3', '03_节奏示范.mp3')
  } else {
    lines.push('图片材料：', '01_作品《春之韵》.jpg', '02_作品《秋色》.jpg', '03_构图示例.jpg')
  }
  lines.push('', `共配套 ${paper.questions.length} 组材料，请在测评前完成设备调试。`)
  downloadText(`${paper.name}-测评材料清单.txt`, lines.join('\n'))
  toast('测评材料清单已开始下载')
}

function askDelete(paper) {
  deleteTarget.value = paper
  confirmOpen.value = true
}

function confirmDelete() {
  const index = db.papers.findIndex(p => p.id === deleteTarget.value?.id)
  if (index > -1) db.papers.splice(index, 1)
  confirmOpen.value = false
  if (current.value?.id === deleteTarget.value?.id) viewOpen.value = false
  toast('试卷已删除')
}

function goPublish() {
  if (!current.value) return
  db.focusPaperId = current.value.id
  viewOpen.value = false
  emit('navigate', 'publish')
}
</script>

<style scoped>
.paper-icon {
  flex: none;
  width: 34px;
  height: 34px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.paper-icon.blue {
  background: #e8f3ff;
  color: #1677ff;
}
.paper-icon.pink {
  background: #fff0f6;
  color: #c41d7f;
}
.score-preview {
  display: flex;
  align-items: baseline;
  gap: 4px;
  height: 32px;
  padding: 0 11px;
  border-radius: 6px;
  background: #f7f8fa;
  color: #1677ff;
  font-size: 18px;
  font-weight: 600;
}
.score-preview span {
  font-size: 12px;
  font-weight: 400;
  color: #86909c;
}
.mode-hint {
  display: flex;
  gap: 9px;
  padding: 11px 13px;
  border-radius: 6px;
  background: #f7f8fa;
  color: #6b7a95;
  font-size: 12px;
  line-height: 1.7;
}
.mode-hint svg {
  flex: none;
  margin-top: 2px;
  color: #1677ff;
}
.paper-meta {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px 16px;
  padding: 15px 16px;
  border-radius: 8px;
  background: #f7f8fa;
  margin-bottom: 18px;
}
.meta-item span {
  display: block;
  margin-bottom: 4px;
  font-size: 11.5px;
  color: #86909c;
}
.meta-item b {
  font-size: 13px;
  color: #1f2329;
}
.question-head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 10px;
}
.question-head h4 {
  margin: 0;
  font-size: 14px;
  color: #1f2329;
}
.question-head span {
  font-size: 11.5px;
}
.question-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.question-list li {
  padding: 13px 15px;
  border: 1px solid #eef1f7;
  border-radius: 8px;
  background: #fff;
}
.q-top {
  display: flex;
  align-items: center;
  gap: 7px;
  margin-bottom: 8px;
}
.q-no {
  width: 22px;
  height: 22px;
  border-radius: 4px;
  background: #e8f3ff;
  color: #1677ff;
  font-size: 11.5px;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
}
.q-stem {
  margin: 0 0 8px;
  font-size: 13px;
  line-height: 1.65;
  color: #1f2329;
}
.q-options {
  display: flex;
  flex-wrap: wrap;
  gap: 6px 18px;
  margin-bottom: 8px;
  font-size: 12.5px;
  color: #6b7688;
}
.q-answer {
  margin: 0;
  padding-top: 8px;
  border-top: 1px dashed #eef1f7;
  font-size: 12px;
  line-height: 1.7;
  color: #6b7280;
}
.confirm-text {
  margin: 0;
  font-size: 13.5px;
  line-height: 1.75;
  color: #4e5969;
}
@media (max-width: 760px) {
  .paper-meta {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
