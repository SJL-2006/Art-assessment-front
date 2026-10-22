const BASE = '/api'

async function req(url) {
  const res = await fetch(BASE + url)
  if (!res.ok) throw new Error(`请求失败: ${res.status}`)
  const data = await res.json()
  // 首页接口直接返回 data（无 code 包装）
  if (!('code' in data)) return data
  return data.data
}

export const api = {
  home: () => req('/home/'),
  login: (role) => req('/login/?role=' + role),

  student: {
    sidebar: () => req('/student/sidebar/'),
    workspace: () => req('/student/workspace/'),
    classDetail: () => req('/student/class/'),
    practicePaper: (subject) => req(`/student/practice/${subject}/`),
    officialPaper: (subject) => req(`/student/official/${subject}/`),
  },
  teacher: {
    sidebar: () => req('/teacher/sidebar/'),
    workspace: () => req('/teacher/workspace/'),
    classes: () => req('/teacher/classes/'),
    recentPapers: () => req('/teacher/papers/recent/'),
  },
  // ===== 省级管理员端 =====
  provincial: {
    stats: () => req('/provincial/stats/'),
    examStats: () => req('/provincial/exam-stats/'),
    papers: () => req('/provincial/papers/'),
    publish: () => req('/provincial/publish/'),
    accountsStudent: () => req('/provincial/accounts/student/'),
    accountsSchool: () => req('/provincial/accounts/school/'),
    accountsDistrict: () => req('/provincial/accounts/district/'),
    accountsCity: () => req('/provincial/accounts/city/'),
    exportRate: () => req('/provincial/export-rate/'),
    logs: () => req('/provincial/logs/'),
  },
  // ===== 题库管理端 =====
  questionbank: {
    stats: () => req('/qb/stats/'),
    questions: () => req('/qb/questions/'),
    audit: () => req('/qb/audit/'),
    resources: () => req('/qb/resources/'),
    courses: () => req('/qb/courses/'),
    chapters: () => req('/qb/chapters/'),
    logs: () => req('/qb/logs/'),
  },
}
