<template>
  <div class="admin-layout">
    <!-- 侧边栏 -->
    <aside class="sidebar">
      <div class="sidebar-logo">
        <span class="logo-icon">
          <svg viewBox="0 0 24 24" width="22" height="22" fill="none">
            <path d="M12 2a10 10 0 1 0 0 20c1.1 0 2-.9 2-2 0-.5-.2-1-.5-1.3-.3-.4-.5-.8-.5-1.2 0-1.1.9-2 2-2h2.3A4.7 4.7 0 0 0 22 10.8C21.9 5.9 17.4 2 12 2Z" fill="url(#lg-sidebar)"/>
            <circle cx="7.5" cy="10.5" r="1.4" fill="#fff"/>
            <circle cx="12" cy="7.5" r="1.4" fill="#fff"/>
            <circle cx="16.5" cy="10.5" r="1.4" fill="#fff"/>
            <defs>
              <linearGradient id="lg-sidebar" x1="0" y1="0" x2="24" y2="24">
                <stop stop-color="#4f9cf9"/><stop offset=".5" stop-color="#a06ee8"/><stop offset="1" stop-color="#f2709c"/>
              </linearGradient>
            </defs>
          </svg>
        </span>
        <div class="logo-text">
          <div class="logo-title">艺术测评系统</div>
          <div class="logo-sub">{{ roleMeta.title }}</div>
        </div>
      </div>

      <nav class="side-nav">
        <template v-for="group in menus" :key="group.title">
          <div class="nav-group-title">{{ group.title }}</div>
          <router-link
            v-for="item in group.items"
            :key="item.path"
            :to="item.path"
            class="nav-item"
            active-class="active"
          >
            <span class="nav-icon" v-html="item.icon"></span>
            <span>{{ item.label }}</span>
          </router-link>
        </template>
      </nav>

      <div class="sidebar-footer">
        <router-link to="/" class="back-home">
          <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 9.5 12 3l9 6.5"/><path d="M5 8v12h14V8"/>
          </svg>
          返回官网
        </router-link>
      </div>
    </aside>

    <!-- 主区 -->
    <div class="main-area">
      <header class="topbar">
        <div class="breadcrumbs">
          <span>{{ roleMeta.title }}</span>
          <span class="sep">/</span>
          <span class="current">{{ $route.meta.title || '首页' }}</span>
        </div>
        <div class="topbar-right">
          <span class="role-tag">{{ roleMeta.title }}</span>
          <div class="user-info">
            <div class="avatar">{{ userInfo.avatar }}</div>
            <div class="user-text">
              <div class="user-name">{{ userInfo.name }}</div>
              <div class="user-role">{{ userInfo.desc }}</div>
            </div>
          </div>
          <button class="logout-btn" @click="$router.push('/login')">退出</button>
        </div>
      </header>

      <main class="content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const roleMeta = computed(() => {
  const m = route.matched[0]?.meta || {}
  return { title: m.title || '管理端', role: m.role || 'unknown' }
})

// 当前登录角色对应的账号信息（预留接入 /api/login/ 的返回结果）
const userInfo = computed(() => {
  if (roleMeta.value.role === 'provincial') {
    return { avatar: '省', name: '赵省管', desc: '省教育厅 · 艺术测评管理' }
  }
  return { avatar: '题', name: '钱题库', desc: '省题库中心 · 试题维护' }
})

const icon = (svg) => svg
const ICON = {
  dashboard: icon('<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><rect x="3" y="3" width="7" height="9" rx="2"/><rect x="14" y="3" width="7" height="5" rx="2"/><rect x="14" y="12" width="7" height="9" rx="2"/><rect x="3" y="16" width="7" height="5" rx="2"/></svg>'),
  stats: icon('<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M3 3v16a2 2 0 0 0 2 2h16"/><path d="M7 14v-4M12 14V6M17 14V9"/></svg>'),
  paper: icon('<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z"/><path d="M14 2v6h6"/><path d="M8 13h8M8 17h6"/></svg>'),
  publish: icon('<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M22 2 11 13"/><path d="M22 2 15 22l-4-9-9-4Z"/></svg>'),
  user: icon('<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 3.6-6.5 8-6.5s8 2.5 8 6.5"/></svg>'),
  school: icon('<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M22 10 12 4 2 10"/><path d="M6 10v10h12V10"/><path d="M10 20v-6h4v6"/></svg>'),
  district: icon('<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M3 6h18v12H3z"/><path d="M3 10h18M9 6v12M15 6v12"/></svg>'),
  city: icon('<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><rect x="3" y="8" width="5" height="14"/><rect x="10" y="3" width="5" height="19"/><rect x="17" y="10" width="5" height="12"/></svg>'),
  export: icon('<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="M7 10l5 5 5-5"/><path d="M12 15V3"/></svg>'),
  log: icon('<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>'),
  question: icon('<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M9.1 9a3 3 0 0 1 5.8 1c0 2-3 2-3 4"/><path d="M12 17h.01"/></svg>'),
  audit: icon('<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="m20 6-11 11-5-5"/><path d="M14 6h6v6"/></svg>'),
  resource: icon('<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><rect x="3" y="3" width="18" height="18" rx="3"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="m21 15-5-5L5 21"/></svg>'),
  course: icon('<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M2 4h6a4 4 0 0 1 4 4v12a3 3 0 0 0-3-3H2Z"/><path d="M22 4h-6a4 4 0 0 0-4 4v12a3 3 0 0 1 3-3h7Z"/></svg>'),
  chapter: icon('<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M4 4h16v4H4z"/><path d="M4 10h16v4H4z"/><path d="M4 16h16v4H4z"/></svg>')
}

const provincialMenus = [
  { title: '数据概览', items: [
    { path: '/provincial/dashboard', label: '总览统计', icon: ICON.dashboard },
    { path: '/provincial/exam-stats', label: '测评数据统计', icon: ICON.stats },
    { path: '/provincial/export-rate', label: '测评率导出', icon: ICON.export }
  ]},
  { title: '组卷与发布', items: [
    { path: '/provincial/paper-manage', label: '省级组卷管理', icon: ICON.paper },
    { path: '/provincial/paper-publish', label: '省级测评发布', icon: ICON.publish }
  ]},
  { title: '账号管理', items: [
    { path: '/provincial/account-student', label: '学生账号', icon: ICON.user },
    { path: '/provincial/account-school', label: '学校账号', icon: ICON.school },
    { path: '/provincial/account-district', label: '区县账号', icon: ICON.district },
    { path: '/provincial/account-city', label: '市级账号', icon: ICON.city }
  ]},
  { title: '系统', items: [
    { path: '/provincial/log', label: '系统日志', icon: ICON.log }
  ]}
]

const qbMenus = [
  { title: '题库概览', items: [
    { path: '/questionbank/dashboard', label: '题库总览', icon: ICON.dashboard }
  ]},
  { title: '试题', items: [
    { path: '/questionbank/questions', label: '试题管理', icon: ICON.question },
    { path: '/questionbank/audit', label: '试题审核', icon: ICON.audit },
    { path: '/questionbank/resource', label: '试题资源', icon: ICON.resource }
  ]},
  { title: '课程体系', items: [
    { path: '/questionbank/course', label: '课程管理', icon: ICON.course },
    { path: '/questionbank/chapter', label: '章节管理', icon: ICON.chapter }
  ]},
  { title: '系统', items: [
    { path: '/questionbank/log', label: '题库日志', icon: ICON.log }
  ]}
]

const menus = computed(() => {
  const role = roleMeta.value.role
  return role === 'provincial' ? provincialMenus : qbMenus
})
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
  background: #f5f7fb;
  font-family: 'PingFang SC', 'Microsoft YaHei', 'Helvetica Neue', sans-serif;
  color: #2b3445;
}

/* ===== 侧边栏 ===== */
.sidebar {
  width: 232px;
  background: linear-gradient(180deg, #1e2a4a 0%, #2a3a66 100%);
  color: #cfd8ee;
  display: flex;
  flex-direction: column;
  position: sticky;
  top: 0;
  height: 100vh;
  flex-shrink: 0;
}
.sidebar-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 20px 20px 18px;
  border-bottom: 1px solid rgba(255,255,255,0.06);
}
.logo-icon { display: inline-flex; }
.logo-title { font-size: 15px; font-weight: 700; color: #fff; letter-spacing: 0.5px; }
.logo-sub { font-size: 11px; color: #8ea2cc; margin-top: 2px; letter-spacing: 0.5px; }

.side-nav {
  flex: 1;
  padding: 14px 12px;
  overflow-y: auto;
}
.nav-group-title {
  font-size: 11px;
  color: #6d7fa5;
  letter-spacing: 1.5px;
  padding: 14px 12px 6px;
  text-transform: uppercase;
}
.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 9px 12px;
  margin: 2px 0;
  border-radius: 8px;
  font-size: 13.5px;
  color: #bfcee8;
  text-decoration: none;
  transition: all 0.15s;
}
.nav-item:hover {
  background: rgba(255,255,255,0.06);
  color: #fff;
}
.nav-item.active {
  background: linear-gradient(90deg, rgba(79,156,249,0.35), rgba(79,156,249,0.05));
  color: #fff;
  font-weight: 500;
  box-shadow: inset 3px 0 0 #4f9cf9;
}
.nav-icon { display: inline-flex; width: 18px; justify-content: center; }

.sidebar-footer {
  padding: 12px 16px;
  border-top: 1px solid rgba(255,255,255,0.06);
}
.back-home {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #8ea2cc;
  text-decoration: none;
}
.back-home:hover { color: #fff; }

/* ===== 主区 ===== */
.main-area { flex: 1; display: flex; flex-direction: column; min-width: 0; }
.topbar {
  background: #fff;
  height: 58px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 28px;
  box-shadow: 0 1px 0 rgba(60,70,100,0.06);
  position: sticky;
  top: 0;
  z-index: 5;
}
.breadcrumbs {
  font-size: 13px;
  color: #8a93a5;
}
.breadcrumbs .sep { margin: 0 8px; color: #c9d1e0; }
.breadcrumbs .current { color: #2b3445; font-weight: 600; }

.topbar-right { display: flex; align-items: center; gap: 18px; }
.role-tag {
  font-size: 11px;
  padding: 3px 10px;
  border-radius: 10px;
  background: #eef4ff;
  color: #2f6fe4;
  letter-spacing: 0.5px;
}
.user-info { display: flex; align-items: center; gap: 10px; }
.avatar {
  width: 32px; height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, #4f9cf9, #a06ee8);
  color: #fff;
  display: flex; align-items: center; justify-content: center;
  font-size: 13px; font-weight: 700;
}
.user-name { font-size: 13px; font-weight: 600; color: #2b3445; }
.user-role { font-size: 11px; color: #8a93a5; }
.logout-btn {
  border: 1px solid #e0e5ef;
  background: #fff;
  color: #4a5568;
  padding: 6px 14px;
  border-radius: 6px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.15s;
}
.logout-btn:hover { border-color: #f2709c; color: #f2709c; }

.content {
  flex: 1;
  padding: 24px 28px 40px;
}
</style>
