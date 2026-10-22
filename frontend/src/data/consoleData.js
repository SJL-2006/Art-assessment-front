import { reactive } from 'vue'

/* ==================== 基础地区数据（市州 → 区县 → 学校） ==================== */

export const SCHOOL_ID = 's-yzq1'
export const DISTRICT_ID = 'd-yzq'

export const cityInfo = { id: 'c-yz', name: '云州市', code: 'YZ' }

export const districts = [
  { id: 'd-yzq', name: '云州区', code: 'YZQ', manager: '李建国', account: 'yzq_admin', phone: '138-2210-6601', status: '正常', createdAt: '2024-09-01' },
  { id: 'd-qcx', name: '青川县', code: 'QCX', manager: '周文斌', account: 'qcx_admin', phone: '137-5521-3388', status: '正常', createdAt: '2024-09-01' },
  { id: 'd-mhx', name: '明湖县', code: 'MHX', manager: '陈晓芸', account: 'mhx_admin', phone: '136-8890-1122', status: '正常', createdAt: '2024-10-15' },
  { id: 'd-lhx', name: '临海县', code: 'LHX', manager: '赵天成', account: 'lhx_admin', phone: '135-6677-4409', status: '停用', createdAt: '2025-03-02' }
]

export const schools = [
  { id: 's-yzq1', districtId: 'd-yzq', name: '云州区第一中学', code: 'YZQ001', type: '公办', stage: '初中', direct: false, manager: '王海燕', account: 'yzq1_admin', phone: '139-8801-2233', status: '正常', createdAt: '2023-08-20' },
  { id: 's-yzq2', districtId: 'd-yzq', name: '云州区第二中学', code: 'YZQ002', type: '公办', stage: '初中', direct: false, manager: '刘海峰', account: 'yzq2_admin', phone: '139-8801-2244', status: '正常', createdAt: '2023-08-20' },
  { id: 's-yzq3', districtId: 'd-yzq', name: '云州区实验中学', code: 'YZQ003', type: '公办', stage: '初中', direct: false, manager: '孙莉', account: 'yzq3_admin', phone: '139-8801-2255', status: '正常', createdAt: '2023-09-12' },
  { id: 's-qcx1', districtId: 'd-qcx', name: '青川中学', code: 'QCX001', type: '公办', stage: '初中', direct: false, manager: '张明远', account: 'qcx1_admin', phone: '137-6601-3301', status: '正常', createdAt: '2023-08-25' },
  { id: 's-qcx2', districtId: 'd-qcx', name: '青川县第二中学', code: 'QCX002', type: '公办', stage: '初中', direct: false, manager: '黄丽华', account: 'qcx2_admin', phone: '137-6601-3302', status: '正常', createdAt: '2023-08-25' },
  { id: 's-qcx3', districtId: 'd-qcx', name: '川口初级中学', code: 'QCX003', type: '公办', stage: '初中', direct: false, manager: '吴永强', account: 'qcx3_admin', phone: '137-6601-3303', status: '停用', createdAt: '2024-02-18' },
  { id: 's-mhx1', districtId: 'd-mhx', name: '明湖县第一中学', code: 'MHX001', type: '公办', stage: '初中', direct: false, manager: '钱文静', account: 'mhx1_admin', phone: '136-9902-1101', status: '正常', createdAt: '2023-10-08' },
  { id: 's-mhx2', districtId: 'd-mhx', name: '明湖实验学校', code: 'MHX002', type: '公办', stage: '九年一贯制', direct: false, manager: '郑凯', account: 'mhx2_admin', phone: '136-9902-1102', status: '正常', createdAt: '2024-03-05' },
  { id: 's-mhx3', districtId: 'd-mhx', name: '湖畔中学', code: 'MHX003', type: '民办', stage: '初中', direct: false, manager: '柳青', account: 'mhx3_admin', phone: '136-9902-1103', status: '正常', createdAt: '2024-03-05' },
  { id: 's-lhx1', districtId: 'd-lhx', name: '临海中学', code: 'LHX001', type: '公办', stage: '初中', direct: false, manager: '徐海生', account: 'lhx1_admin', phone: '135-7712-9901', status: '正常', createdAt: '2023-11-20' },
  { id: 's-lhx2', districtId: 'd-lhx', name: '海城第二中学', code: 'LHX002', type: '公办', stage: '初中', direct: false, manager: '马晓琳', account: 'lhx2_admin', phone: '135-7712-9902', status: '正常', createdAt: '2023-11-20' },
  { id: 's-lhx3', districtId: 'd-lhx', name: '望海初级中学', code: 'LHX003', type: '公办', stage: '初中', direct: false, manager: '高峰', account: 'lhx3_admin', phone: '135-7712-9903', status: '正常', createdAt: '2024-06-01' },
  { id: 's-zs1', districtId: null, name: '云州市直属第一中学', code: 'ZS001', type: '公办', stage: '高中', direct: true, manager: '何文博', account: 'zs1_admin', phone: '138-0001-8801', status: '正常', createdAt: '2022-09-01' },
  { id: 's-zs2', districtId: null, name: '云州市艺术学校', code: 'ZS002', type: '公办', stage: '完全中学', direct: true, manager: '尚雅', account: 'zs2_admin', phone: '138-0001-8802', status: '正常', createdAt: '2022-09-01' }
]

export const roleMeta = {
  school: { key: 'school', name: '学校端', icon: 'school', scope: '云州区第一中学', scopeType: '学校' },
  district: { key: 'district', name: '区县端', icon: 'district', scope: '云州区', scopeType: '区县' },
  city: { key: 'city', name: '市州端', icon: 'city', scope: '云州市', scopeType: '市州' }
}

export const roleOptions = [roleMeta.school, roleMeta.district, roleMeta.city]

export const menus = [
  { key: 'dashboard', name: '数据概览', icon: 'dashboard' },
  { key: 'accounts', name: '账号管理', icon: 'users' },
  { key: 'papers', name: '组卷管理', icon: 'paper' },
  { key: 'publish', name: '测评发布', icon: 'send' },
  { key: 'statistics', name: '数据统计', icon: 'chart' },
  { key: 'backfill', name: '测评补录', icon: 'edit' }
]

export const subjects = ['音乐', '美术']
export const grades = ['七年级', '八年级', '九年级']

export function getSchool(id) {
  return schools.find(s => s.id === id)
}
export function getDistrict(id) {
  return districts.find(d => d.id === id)
}
export function schoolsOfDistrict(id) {
  return schools.filter(s => s.districtId === id)
}
export function schoolsForRole(role) {
  if (role === 'school') return schools.filter(s => s.id === SCHOOL_ID)
  if (role === 'district') return schoolsOfDistrict(DISTRICT_ID)
  return schools
}
export function districtNameOfSchool(school) {
  return school.direct ? '市直属' : (getDistrict(school.districtId)?.name || '—')
}

/* ==================== 模拟数据生成 ==================== */

let seed = 20261022
function rand() {
  seed = (seed * 9301 + 49297) % 233280
  return seed / 233280
}
function int(min, max) {
  return Math.floor(rand() * (max - min + 1)) + min
}
function pick(list) {
  return list[Math.floor(rand() * list.length)]
}
function pad(n) {
  return String(n).padStart(2, '0')
}
export function dateStr(offsetDays = 0) {
  const d = new Date()
  d.setDate(d.getDate() + offsetDays)
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`
}
export function dateTimeStr(offsetDays = 0, hour = 9, minute = 0) {
  return `${dateStr(offsetDays)} ${pad(hour)}:${pad(minute)}`
}
export function localInputValue(offsetDays = 0, hour = 9, minute = 0) {
  return `${dateStr(offsetDays)}T${pad(hour)}:${pad(minute)}`
}
export function nowStamp() {
  const d = new Date()
  return `${dateStr()} ${pad(d.getHours())}:${pad(d.getMinutes())}`
}

const surnames = ['张', '王', '李', '刘', '陈', '杨', '赵', '周', '吴', '徐', '孙', '马', '朱', '胡', '郭', '何', '高', '林', '罗', '郑']
const givenNames = ['伟', '娜', '芳', '洋', '静', '帆', '敏', '杰', '倩', '磊', '悦', '超', '欣', '婷', '浩', '晨', '雨', '佳', '铭', '雪']
const subjectsPool = ['音乐', '美术', '语文', '数学']

function personName() {
  return pick(surnames) + pick(givenNames)
}

// 教师账号
const teachers = []
schools.forEach((school, sIdx) => {
  const count = int(6, 9)
  for (let i = 0; i < count; i++) {
    const grade = pick(grades)
    teachers.push({
      id: `t-${sIdx}-${i}`,
      schoolId: school.id,
      name: personName(),
      account: `teacher${sIdx + 1}${pad(i + 1)}`,
      phone: `1${int(3, 9)}9-${int(1000, 9999)}-${int(1000, 9999)}`,
      subject: pick(subjectsPool),
      grade,
      role: i % 4 === 0 ? '班主任' : '科任教师',
      status: rand() > 0.08 ? '正常' : '停用',
      createdAt: dateStr(-int(30, 700))
    })
  }
})

// 学生账号
const students = []
schools.forEach((school, sIdx) => {
  const count = int(12, 18)
  for (let i = 0; i < count; i++) {
    const grade = pick(grades)
    const cls = int(1, 6)
    const no = `2026${pad(sIdx + 1)}${pad(i + 1)}`
    students.push({
      id: `stu-${sIdx}-${i}`,
      schoolId: school.id,
      name: personName(),
      studentNo: no,
      account: `stu${no}`,
      grade,
      className: `${grade}(${cls})班`,
      gender: rand() > 0.5 ? '女' : '男',
      status: rand() > 0.05 ? '正常' : '停用',
      createdAt: dateStr(-int(20, 500))
    })
  }
})

/* ==================== 试卷 ==================== */

const musicStems = [
  '聆听音频片段，判断该乐曲的演奏形式是（  ）',
  '聆听旋律片段，选出对应的民族乐器（  ）',
  '判断下列节奏型属于几拍子（  ）',
  '聆听歌曲片段，判断其所属的地区民歌类别（  ）',
  '判断该音乐作品的曲式结构（  ）'
]
const artStems = [
  '观察作品《春之韵》，判断其色彩风格属于（  ）',
  '欣赏画作，选出作品主要使用的构图方式（  ）',
  '判断该作品所属的美术门类（  ）',
  '观察作品细节，判断其采用的绘画技法（  ）',
  '分析画面，选出作品表达的主要情感（  ）'
]
const musicTypes = ['听辨题', '选择题', '判断题', '欣赏题', '判断题']
const artTypes = ['欣赏题', '选择题', '判断题', '分析题', '选择题']

export function makeQuestions(subject, count = 5) {
  const stems = subject === '音乐' ? musicStems : artStems
  const types = subject === '音乐' ? musicTypes : artTypes
  return stems.slice(0, Math.min(count, 5)).map((stem, i) => ({
    no: i + 1,
    type: types[i],
    difficulty: i < 2 ? '简单' : i < 4 ? '中等' : '较难',
    stem,
    options: ['A. 民族管弦乐', 'B. 交响乐', 'C. 室内乐', 'D. 电声乐'],
    answer: ['A', 'B', 'C', 'A', 'B'][i],
    analysis: subject === '音乐'
      ? '该题考查对音乐表现要素与作品风格的听辨能力，需结合音色、节奏与曲式综合判断。'
      : '该题考查美术作品欣赏能力，需从色彩、构图与技法等角度综合分析。'
  }))
}

function paper(id, level, name, subject, grade, mode, difficulty, count, status, creator, createdOffset) {
  return {
    id,
    level,
    name,
    subject,
    grade,
    mode,
    difficulty,
    questionCount: count,
    scoreEach: subject === '音乐' ? 2 : 4,
    totalScore: count * (subject === '音乐' ? 2 : 4),
    status,
    creator,
    createdAt: dateStr(createdOffset),
    questions: makeQuestions(subject)
  }
}

const papers = [
  paper('p-s1', 'school', '云州区第一中学 2026 年秋季音乐测评卷', '音乐', '八年级', '自动组卷', '中等', 30, 'published', '王海燕', -18),
  paper('p-s2', 'school', '云州区第一中学 2026 年秋季美术测评卷', '美术', '八年级', '自动组卷', '中等', 25, 'published', '王海燕', -18),
  paper('p-s3', 'school', '云州区第一中学艺术素养练习卷（音乐）', '音乐', '七年级', '手动组卷', '简单', 20, 'draft', '林雨晨', -6),
  paper('p-s4', 'school', '云州区第一中学艺术素养练习卷（美术）', '美术', '九年级', '自动组卷', '较难', 25, 'draft', '林雨晨', -3),
  paper('p-d1', 'district', '云州区 2026 年中小学生音乐素养测评卷', '音乐', '八年级', '自动组卷', '中等', 30, 'published', '李建国', -25),
  paper('p-d2', 'district', '云州区 2026 年中小学生美术素养测评卷', '美术', '八年级', '自动组卷', '中等', 25, 'published', '李建国', -25),
  paper('p-d3', 'district', '云州区 2026 年春季音乐练习卷', '音乐', '七年级', '手动组卷', '简单', 20, 'draft', '教研中心', -45),
  paper('p-d4', 'district', '云州区艺术素质测评样卷（美术）', '美术', '九年级', '自动组卷', '较难', 30, 'draft', '教研中心', -12),
  paper('p-c1', 'city', '云州市 2026 年艺术素质测评统一试卷（音乐）', '音乐', '八年级', '自动组卷', '中等', 40, 'published', '市教科院', -30),
  paper('p-c2', 'city', '云州市 2026 年艺术素质测评统一试卷（美术）', '美术', '八年级', '自动组卷', '中等', 40, 'published', '市教科院', -30),
  paper('p-c3', 'city', '云州市 2026 年秋季艺术素养抽测卷', '音乐', '九年级', '手动组卷', '较难', 35, 'draft', '市教科院', -8),
  paper('p-c4', 'city', '云州市艺术测评样卷（美术）', '美术', '七年级', '自动组卷', '简单', 30, 'draft', '市教科院', -5)
]

/* ==================== 测评发布 ==================== */

const publishes = [
  { id: 'pub-s1', level: 'school', paperId: 'p-s1', name: '2026 年秋季音乐测评（八年级）', subject: '音乐', grade: '八年级', scopeText: '云州区第一中学 · 八年级', start: dateTimeStr(-12, 8), end: dateTimeStr(3, 18), duration: 45, target: 286, submitted: 241, note: '请各班在信息课教室统一作答。', createdAt: dateStr(-14) },
  { id: 'pub-s2', level: 'school', paperId: 'p-s2', name: '2026 年秋季美术测评（八年级）', subject: '美术', grade: '八年级', scopeText: '云州区第一中学 · 八年级', start: dateTimeStr(5, 8), end: dateTimeStr(12, 18), duration: 45, target: 286, submitted: 0, note: '与音乐测评错峰进行。', createdAt: dateStr(-2) },
  { id: 'pub-s3', level: 'school', paperId: 'p-s3', name: '七年级音乐素养练习', subject: '音乐', grade: '七年级', scopeText: '云州区第一中学 · 七年级', start: dateTimeStr(-35, 8), end: dateTimeStr(-28, 18), duration: 30, target: 274, submitted: 268, note: '', createdAt: dateStr(-36) },
  { id: 'pub-d1', level: 'district', paperId: 'p-d1', name: '云州区中小学生音乐素养测评（八年级）', subject: '音乐', grade: '八年级', scopeText: '云州区 · 全部学校 · 八年级', start: dateTimeStr(-10, 8), end: dateTimeStr(4, 18), duration: 60, target: 1860, submitted: 1423, note: '区级统一测评，请各校按时组织。', createdAt: dateStr(-15) },
  { id: 'pub-d2', level: 'district', paperId: 'p-d2', name: '云州区中小学生美术素养测评（八年级）', subject: '美术', grade: '八年级', scopeText: '云州区 · 全部学校 · 八年级', start: dateTimeStr(6, 8), end: dateTimeStr(16, 18), duration: 60, target: 1860, submitted: 0, note: '', createdAt: dateStr(-3) },
  { id: 'pub-d3', level: 'district', paperId: 'p-d3', name: '云州区七年级音乐春季练习', subject: '音乐', grade: '七年级', scopeText: '云州区 · 云州区第二中学 · 七年级', start: dateTimeStr(-50, 8), end: dateTimeStr(-40, 18), duration: 30, target: 620, submitted: 604, note: '', createdAt: dateStr(-52) },
  { id: 'pub-c1', level: 'city', paperId: 'p-c1', name: '云州市艺术素质测评统一测评（音乐）', subject: '音乐', grade: '八年级', scopeText: '云州市 · 全部区县 · 八年级', start: dateTimeStr(-8, 8), end: dateTimeStr(6, 18), duration: 60, target: 6820, submitted: 5127, note: '全市统一测评，各区县按分配批次组织。', createdAt: dateStr(-20) },
  { id: 'pub-c2', level: 'city', paperId: 'p-c2', name: '云州市艺术素质测评统一测评（美术）', subject: '美术', grade: '八年级', scopeText: '云州市 · 全部区县 · 八年级', start: dateTimeStr(8, 8), end: dateTimeStr(18, 18), duration: 60, target: 6820, submitted: 0, note: '', createdAt: dateStr(-4) },
  { id: 'pub-c3', level: 'city', paperId: 'p-c3', name: '云州市秋季艺术素养抽测（九年级音乐）', subject: '音乐', grade: '九年级', scopeText: '云州市 · 青川县 · 九年级', start: dateTimeStr(-40, 8), end: dateTimeStr(-30, 18), duration: 60, target: 2100, submitted: 2035, note: '抽测结果计入年度艺术素养监测报告。', createdAt: dateStr(-42) }
]

/* ==================== 测评统计 ==================== */

const stats = []
schools.forEach(school => {
  grades.forEach(grade => {
    subjects.forEach(subject => {
      const eligible = int(120, 330)
      const rate = 0.76 + rand() * 0.22
      const avg = 72 + rand() * 22
      stats.push({
        id: `st-${school.id}-${grade}-${subject}`,
        schoolId: school.id,
        districtId: school.districtId || 'direct',
        grade,
        subject,
        eligible,
        participants: Math.round(eligible * rate),
        avgScore: Number(avg.toFixed(1)),
        excellentRate: Number((12 + rand() * 26).toFixed(1)),
        passRate: Number((82 + rand() * 16).toFixed(1))
      })
    })
  })
})

/* ==================== 测评补录 ==================== */

const backfillReasons = ['缺考未参加', '设备故障未提交', '成绩录入异常', '跨校转学补测']
const backfills = []
for (let i = 0; i < 14; i++) {
  const school = pick(schools)
  const schoolStudents = students.filter(s => s.schoolId === school.id)
  const stu = schoolStudents.length ? pick(schoolStudents) : null
  const subject = pick(subjects)
  backfills.push({
    id: `bf-${i + 1}`,
    schoolId: school.id,
    studentId: stu?.id || '',
    studentName: stu?.name || personName(),
    subject,
    paperName: `${school.name} ${subject}测评`,
    score: Number((65 + rand() * 33).toFixed(1)),
    examDate: dateStr(-int(3, 40)),
    reason: pick(backfillReasons),
    detail: '经核对纸质答卷与考场记录，申请补录。',
    status: i % 5 === 0 ? 'pending' : i % 7 === 0 ? 'rejected' : 'approved',
    operator: pick(['王海燕', '李建国', '市教科院']),
    createdAt: dateTimeStr(-int(0, 20), int(9, 17), int(0, 59))
  })
}

/* ==================== 最近动态 ==================== */

const activities = [
  { icon: 'send', tone: 'blue', title: '发布《2026 年秋季音乐测评》', desc: '覆盖八年级 · 286 名学生', time: '12 分钟前' },
  { icon: 'users', tone: 'green', title: '批量创建教师账号', desc: '新增 8 名艺术学科教师', time: '1 小时前' },
  { icon: 'edit', tone: 'amber', title: '提交成绩补录申请', desc: '八年级美术 · 3 名学生', time: '3 小时前' },
  { icon: 'paper', tone: 'purple', title: '完成自动组卷', desc: '《艺术素养练习卷（美术）》· 25 题', time: '昨天 16:42' },
  { icon: 'chart', tone: 'pink', title: '导出测评数据统计', desc: '云州区 · 八年级音乐 · Excel', time: '昨天 09:15' }
]

/* ==================== 共享状态 ==================== */

export const db = reactive({
  teachers,
  students,
  schoolAccounts: schools,
  districtAccounts: districts,
  papers,
  publishes,
  stats,
  backfills,
  activities,
  focusPublish: null
})

/* ==================== 工具函数 ==================== */

let idSeq = 1000
export function nextId(prefix = 'id') {
  idSeq += 1
  return `${prefix}-${Date.now().toString(36)}${idSeq}`
}

export function publishStatus(rec, now = new Date()) {
  const start = new Date(rec.start.replace(' ', 'T'))
  const end = new Date(rec.end.replace(' ', 'T'))
  if (now < start) return 'pending'
  if (now > end) return 'done'
  return 'ongoing'
}

export const publishStatusMeta = {
  ongoing: { label: '进行中', tag: 'green' },
  pending: { label: '待开始', tag: 'blue' },
  done: { label: '已结束', tag: 'gray' }
}

export function aggregateRows(rows) {
  const participants = rows.reduce((s, r) => s + r.participants, 0)
  const eligible = rows.reduce((s, r) => s + r.eligible, 0)
  const avgScore = participants
    ? rows.reduce((s, r) => s + r.avgScore * r.participants, 0) / participants
    : 0
  const excellentRate = participants
    ? rows.reduce((s, r) => s + r.excellentRate * r.participants, 0) / participants
    : 0
  const passRate = participants
    ? rows.reduce((s, r) => s + r.passRate * r.participants, 0) / participants
    : 0
  return {
    participants,
    eligible,
    participation: eligible ? (participants / eligible) * 100 : 0,
    avgScore,
    excellentRate,
    passRate
  }
}

export function shortSchool(name) {
  return name.replace('云州区', '').replace('云州市', '').replace('青川县', '').replace('明湖县', '').replace('临海县', '')
}

export function sparklineFor(label, base) {
  let h = 0
  for (let i = 0; i < label.length; i++) h = (h * 31 + label.charCodeAt(i)) % 997
  return Array.from({ length: 6 }, (_, i) => {
    const wave = Math.sin((h + i * 37) / 41) * 6
    return Number((base + wave + i * 0.6).toFixed(1))
  })
}

export function downloadText(filename, content, mime = 'text/plain;charset=utf-8') {
  const blob = new Blob(['﻿' + content], { type: mime })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  setTimeout(() => URL.revokeObjectURL(url), 1000)
}

export function downloadCsv(filename, headers, rows) {
  const escape = v => `"${String(v ?? '').replace(/"/g, '""')}"`
  const content = [headers, ...rows].map(row => row.map(escape).join(',')).join('\r\n')
  downloadText(filename, content, 'text/csv;charset=utf-8')
}
