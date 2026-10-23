import { createRouter, createWebHashHistory } from 'vue-router'
import MainLayout from '../layouts/MainLayout.vue'
import StudentLayout from '../layouts/StudentLayout.vue'
import TeacherLayout from '../layouts/TeacherLayout.vue'
import AdminLayout from '../layouts/AdminLayout.vue'

const routes = [
  { path: '/', component: MainLayout, children: [
    { path: '', name: 'home', component: () => import('../views/HomeView.vue') },
    { path: 'login', name: 'login', component: () => import('../views/LoginView.vue') },
    { path: 'register', name: 'register', component: () => import('../views/RegisterView.vue') },
    { path: 'help', name: 'help', component: () => import('../views/PlaceholderView.vue'), meta: { title: '系统帮助' } },
  ]},
  { path: '/practice', redirect: '/student/practice/music' },
  { path: '/analysis', redirect: '/student/curve' },
  { path: '/profile', redirect: '/student/profile' },
  {
    path: '/student',
    component: StudentLayout,
    redirect: '/student/dashboard',
    children: [
      { path: 'dashboard', name: 'student-dashboard', component: () => import('../views/student/Dashboard.vue'), meta: { title: '工作台' } },
      { path: 'class', name: 'student-class', component: () => import('../views/PlaceholderView.vue'), meta: { title: '我的班级' } },
      { path: 'practice/music', component: () => import('../views/PlaceholderView.vue'), meta: { title: '音乐测评练习' } },
      { path: 'practice/art', component: () => import('../views/PlaceholderView.vue'), meta: { title: '美术测评练习' } },
      { path: 'practice/dance', component: () => import('../views/PlaceholderView.vue'), meta: { title: '舞蹈测评练习' } },
      { path: 'practice/general', component: () => import('../views/PlaceholderView.vue'), meta: { title: '综合测评' } },
      { path: 'official/music', component: () => import('../views/PlaceholderView.vue'), meta: { title: '音乐正式测评' } },
      { path: 'official/art', component: () => import('../views/PlaceholderView.vue'), meta: { title: '美术正式测评' } },
      { path: 'results', component: () => import('../views/PlaceholderView.vue'), meta: { title: '测评记录' } },
      { path: 'curve', component: () => import('../views/student/GrowthCurve.vue'), meta: { title: '成绩曲线' } },
      { path: 'class-report', component: () => import('../views/PlaceholderView.vue'), meta: { title: '班级测评信息' } },
      { path: 'certificate', component: () => import('../views/student/Certificate.vue'), meta: { title: '我的证书' } },
      { path: 'profile', component: () => import('../views/PlaceholderView.vue'), meta: { title: '个人信息' } },
      { path: 'autonomy', component: () => import('../views/PlaceholderView.vue'), meta: { title: '课外自主学习' } },
    ],
  },
  {
    path: '/teacher',
    component: TeacherLayout,
    redirect: '/teacher/dashboard',
    children: [
      { path: 'dashboard', name: 'teacher-dashboard', component: () => import('../views/teacher/Dashboard.vue'), meta: { title: '工作台' } },
      { path: 'class', component: () => import('../views/PlaceholderView.vue'), meta: { title: '班级列表' } },
      { path: 'class/create', component: () => import('../views/PlaceholderView.vue'), meta: { title: '创建班级' } },
      { path: 'students', component: () => import('../views/PlaceholderView.vue'), meta: { title: '学生列表' } },
      { path: 'students/import', component: () => import('../views/PlaceholderView.vue'), meta: { title: '批量导入学生' } },
      { path: 'questions', component: () => import('../views/PlaceholderView.vue'), meta: { title: '试题库' } },
      { path: 'papers', component: () => import('../views/PlaceholderView.vue'), meta: { title: '试卷列表' } },
      { path: 'papers/create', component: () => import('../views/PlaceholderView.vue'), meta: { title: '手动组卷' } },
      { path: 'papers/auto', component: () => import('../views/PlaceholderView.vue'), meta: { title: '自动组卷' } },
      { path: 'publish/music', component: () => import('../views/PlaceholderView.vue'), meta: { title: '发布音乐测评' } },
      { path: 'publish/art', component: () => import('../views/PlaceholderView.vue'), meta: { title: '发布美术测评' } },
      { path: 'score', component: () => import('../views/PlaceholderView.vue'), meta: { title: '学生评分' } },
      { path: 'certificate', component: () => import('../views/PlaceholderView.vue'), meta: { title: '学生证书' } },
      { path: 'profile', component: () => import('../views/PlaceholderView.vue'), meta: { title: '个人信息' } },
    ],
  },
  // ===== 省级管理员端 =====
  {
    path: '/provincial',
    component: AdminLayout,
    redirect: '/provincial/dashboard',
    meta: { role: 'provincial', title: '省级管理员端' },
    children: [
      { path: 'dashboard', name: 'provincial-dashboard', component: () => import('../views/provincial/Dashboard.vue'), meta: { title: '总览统计' } },
      { path: 'exam-stats', name: 'provincial-exam-stats', component: () => import('../views/provincial/ExamStats.vue'), meta: { title: '测评数据统计' } },
      { path: 'paper-manage', name: 'provincial-paper-manage', component: () => import('../views/provincial/PaperManage.vue'), meta: { title: '省级组卷管理' } },
      { path: 'paper-publish', name: 'provincial-paper-publish', component: () => import('../views/provincial/PaperPublish.vue'), meta: { title: '省级测评发布' } },
      { path: 'account-student', name: 'provincial-account-student', component: () => import('../views/provincial/AccountStudent.vue'), meta: { title: '学生账号管理' } },
      { path: 'account-school', name: 'provincial-account-school', component: () => import('../views/provincial/AccountSchool.vue'), meta: { title: '学校账号管理' } },
      { path: 'account-district', name: 'provincial-account-district', component: () => import('../views/provincial/AccountDistrict.vue'), meta: { title: '区县账号管理' } },
      { path: 'account-city', name: 'provincial-account-city', component: () => import('../views/provincial/AccountCity.vue'), meta: { title: '市级账号管理' } },
      { path: 'export-rate', name: 'provincial-export-rate', component: () => import('../views/provincial/ExportRate.vue'), meta: { title: '测评率导出' } },
      { path: 'log', name: 'provincial-log', component: () => import('../views/provincial/LogView.vue'), meta: { title: '系统日志' } },
    ],
  },
  // ===== 题库管理端 =====
  {
    path: '/questionbank',
    component: AdminLayout,
    redirect: '/questionbank/dashboard',
    meta: { role: 'questionbank', title: '题库管理端' },
    children: [
      { path: 'dashboard', name: 'qb-dashboard', component: () => import('../views/questionbank/Dashboard.vue'), meta: { title: '题库总览' } },
      { path: 'questions', name: 'qb-questions', component: () => import('../views/questionbank/QuestionList.vue'), meta: { title: '试题管理' } },
      { path: 'audit', name: 'qb-audit', component: () => import('../views/questionbank/QuestionAudit.vue'), meta: { title: '试题审核' } },
      { path: 'resource', name: 'qb-resource', component: () => import('../views/questionbank/ResourceManage.vue'), meta: { title: '试题资源管理' } },
      { path: 'course', name: 'qb-course', component: () => import('../views/questionbank/CourseList.vue'), meta: { title: '课程管理' } },
      { path: 'chapter', name: 'qb-chapter', component: () => import('../views/questionbank/ChapterList.vue'), meta: { title: '章节管理' } },
      { path: 'log', name: 'qb-log', component: () => import('../views/questionbank/QbLogView.vue'), meta: { title: '题库日志' } },
    ],
  },
  // ===== 学校端 / 区县端 / 市州端（同一控制台，侧栏内切换管理身份） =====
  { path: '/admin', redirect: '/admin/dashboard' },
  {
    path: '/admin/:page',
    name: 'admin-console',
    component: () => import('../views/ConsoleView.vue'),
    meta: { title: '管理中心' },
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
})

export default router
