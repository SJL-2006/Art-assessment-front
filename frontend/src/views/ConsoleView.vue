<template>
  <div class="console">
    <div v-if="mobileOpen" class="sidebar-mask" @click="mobileOpen = false" />

    <aside class="sidebar" :class="{ 'mobile-open': mobileOpen }">
      <a class="brand" href="#/" @click="mobileOpen = false">
        <span class="brand-icon"><AppIcon name="palette" :size="20" /></span>
        <span class="brand-text">
          <b>艺术测评系统</b>
          <i>ART ASSESSMENT</i>
        </span>
      </a>

      <div class="role-card">
        <p class="role-label">当前管理身份</p>
        <div class="role-switch">
          <button
            v-for="r in roleOptions"
            :key="r.key"
            class="role-btn"
            :class="{ active: role === r.key }"
            :title="r.name"
            @click="switchRole(r.key)"
          >
            <span>{{ r.name }}</span>
          </button>
        </div>
        <div class="scope-line">
          <AppIcon :name="roleInfo.icon" :size="14" />
          {{ roleInfo.scope }}
        </div>
      </div>

      <nav class="nav">
        <router-link
          v-for="m in menus"
          :key="m.key"
          :to="{ path: '/admin/' + m.key, query: { role } }"
          class="nav-item"
          :class="{ active: currentKey === m.key }"
          @click="mobileOpen = false"
        >
          <span class="nav-icon"><AppIcon :name="m.icon" :size="18" /></span>
          <span class="nav-label">{{ m.name }}</span>
          <span v-if="badgeOf(m.key)" class="nav-badge">{{ badgeOf(m.key) }}</span>
        </router-link>
      </nav>

      <div class="sidebar-foot">
        <p class="sidebar-note">
          <AppIcon name="shield" :size="13" />数据加密保护 · 每日 02:00 汇总
        </p>
        <a class="back-home" href="#/" @click="mobileOpen = false">
          <AppIcon name="home" :size="15" />返回官网首页
        </a>
      </div>
    </aside>

    <div class="main">
      <header class="topbar">
        <div class="top-left">
          <button class="menu-btn" title="菜单" @click="mobileOpen = true">
            <AppIcon name="menu" :size="19" />
          </button>
          <div class="crumb">
            <span class="crumb-muted">管理中心</span>
            <AppIcon name="chevron-right" :size="13" />
            <span class="crumb-current">{{ currentMenu.name }}</span>
          </div>
        </div>
        <div class="top-right">
          <span class="scope-chip">
            <AppIcon :name="roleInfo.icon" :size="14" />
            {{ roleInfo.scope }}
          </span>
          <button class="icon-btn" title="通知" @click="notify">
            <AppIcon name="bell" :size="18" />
            <i v-if="hasNotice" class="dot" />
          </button>
          <div class="user">
            <span class="c-avatar">{{ adminName.charAt(0) }}</span>
            <div class="user-text">
              <b>{{ adminName }}</b>
              <span>{{ roleInfo.name }}管理员</span>
            </div>
          </div>
        </div>
      </header>

      <main class="content">
        <component
          :is="currentPage"
          :key="currentKey + '-' + role"
          :role="role"
          @navigate="navigate"
        />
      </main>
    </div>

    <ToastHost />
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AppIcon from '../components/AppIcon.vue'
import ToastHost from '../components/ToastHost.vue'
import { toast } from '../data/toast'
import {
  db,
  menus,
  roleOptions,
  roleMeta,
  publishStatus,
  schoolsForRole
} from '../data/consoleData'
import DashboardPage from './console/DashboardPage.vue'
import AccountsPage from './console/AccountsPage.vue'
import PapersPage from './console/PapersPage.vue'
import PublishPage from './console/PublishPage.vue'
import StatisticsPage from './console/StatisticsPage.vue'
import BackfillPage from './console/BackfillPage.vue'

const pageMap = {
  dashboard: DashboardPage,
  accounts: AccountsPage,
  papers: PapersPage,
  publish: PublishPage,
  statistics: StatisticsPage,
  backfill: BackfillPage
}

const pageKeys = Object.keys(pageMap)

const route = useRoute()
const router = useRouter()

// 子页面从路由参数读取：/admin/:page
const currentKey = computed(() => {
  const k = Array.isArray(route.params.page) ? route.params.page[0] : route.params.page
  return pageKeys.includes(k) ? k : 'dashboard'
})

const mobileOpen = ref(false)

// 管理身份：学校端 / 区县端 / 市州端，支持登录时 ?role= 指定，也支持侧栏内切换
const validRoles = roleOptions.map(r => r.key)
const queryRole = route.query.role
const savedRole = localStorage.getItem('art-console-role')
const role = ref(
  validRoles.includes(queryRole) ? queryRole : validRoles.includes(savedRole) ? savedRole : 'school'
)

const roleInfo = computed(() => roleMeta[role.value])
const currentMenu = computed(() => menus.find(m => m.key === currentKey.value) || menus[0])
const currentPage = computed(() => pageMap[currentKey.value])
const adminName = computed(() =>
  ({ school: '王海燕', district: '李建国', city: '何文博' })[role.value]
)

// 切换身份时同步到地址栏，刷新后仍保持当前端
watch(role, value => {
  localStorage.setItem('art-console-role', value)
  router.replace({ query: { ...route.query, role: value } })
})

const scopeIds = computed(() => new Set(schoolsForRole(role.value).map(s => s.id)))
const pendingCount = computed(
  () => db.backfills.filter(b => scopeIds.value.has(b.schoolId) && b.status === 'pending').length
)
const draftCount = computed(() => db.papers.filter(p => p.level === role.value && p.status === 'draft').length)
const ongoingCount = computed(
  () => db.publishes.filter(p => p.level === role.value && publishStatus(p) === 'ongoing').length
)
const hasNotice = computed(() => pendingCount.value > 0)

function badgeOf(key) {
  if (key === 'backfill') return pendingCount.value || ''
  if (key === 'papers') return draftCount.value || ''
  if (key === 'publish') return ongoingCount.value || ''
  return ''
}

function switchRole(key) {
  if (role.value === key) return
  role.value = key
  mobileOpen.value = false
  toast(`已切换至${roleMeta[key].name}`, 'info')
}

function navigate(key) {
  if (!pageMap[key]) return
  router.push({ path: '/admin/' + key, query: { role: role.value } })
}

function notify() {
  toast(pendingCount.value ? `有 ${pendingCount.value} 条补录申请待审核` : '暂无新的系统通知', 'info')
}

onMounted(() => {
  document.title = `${currentMenu.value.name} · 艺术测评系统`
})

watch(currentKey, key => {
  document.title = `${currentMenu.value.name} · 艺术测评系统`
  if (key) window.scrollTo({ top: 0 })
})
</script>

<style scoped>
.console {
  display: flex;
  min-height: 100vh;
  background: #f2f4f7;
}
.sidebar {
  position: sticky;
  top: 0;
  z-index: 40;
  width: 232px;
  height: 100vh;
  flex: none;
  display: flex;
  flex-direction: column;
  padding: 16px 12px 14px;
  background: #fff;
  border-right: 1px solid #f0f0f0;
}
.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 4px 8px 16px;
  text-decoration: none;
}
.brand-icon {
  flex: none;
  width: 34px;
  height: 34px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  background: #1677ff;
}
.brand-text {
  display: flex;
  flex-direction: column;
  gap: 1px;
  white-space: nowrap;
}
.brand-text b {
  font-size: 15px;
  color: #1f2329;
}
.brand-text i {
  font-style: normal;
  font-size: 8.5px;
  letter-spacing: 1.2px;
  color: #a3a9b3;
}
.role-card {
  padding: 10px;
  border-radius: 6px;
  background: #f7f8fa;
  border: 1px solid #f0f0f0;
  margin-bottom: 14px;
}
.role-label {
  margin: 0 0 6px;
  font-size: 11px;
  color: #86909c;
}
.role-switch {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2px;
  padding: 2px;
  border-radius: 6px;
  background: #eceef1;
}
.role-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  padding: 5px 4px;
  border: none;
  border-radius: 4px;
  background: transparent;
  color: #4e5969;
  font-family: inherit;
  font-size: 12px;
  white-space: nowrap;
  cursor: pointer;
  transition: all 0.16s;
}
.role-btn:hover {
  color: #1677ff;
}
.role-btn.active {
  background: #fff;
  color: #1677ff;
  font-weight: 500;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.06);
}
.scope-line {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 7px;
  padding: 0 2px;
  font-size: 11px;
  color: #86909c;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.nav {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 10px;
  border-radius: 6px;
  text-decoration: none;
  color: #4e5969;
  font-size: 13px;
  transition: all 0.16s;
}
.nav-item:hover {
  background: #f5f6f8;
  color: #1f2329;
}
.nav-item.active {
  background: #e8f3ff;
  color: #1677ff;
  font-weight: 500;
}
.nav-icon {
  flex: none;
  display: flex;
  align-items: center;
  color: #86909c;
}
.nav-item.active .nav-icon,
.nav-item:hover .nav-icon {
  color: #1677ff;
}
.nav-label {
  flex: 1;
  white-space: nowrap;
}
.nav-badge {
  min-width: 18px;
  height: 18px;
  padding: 0 5px;
  border-radius: 9px;
  background: #fff1f0;
  color: #f53f3f;
  font-size: 11px;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
}
.sidebar-foot {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.sidebar-note {
  display: flex;
  align-items: center;
  gap: 6px;
  margin: 0;
  padding: 6px 8px;
  font-size: 11px;
  color: #86909c;
  white-space: nowrap;
}
.back-home {
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 7px 8px;
  border-radius: 4px;
  color: #6b7280;
  font-size: 12px;
  text-decoration: none;
  transition: all 0.15s;
}
.back-home:hover {
  background: #f5f6f8;
  color: #1677ff;
}
.main {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
}
.topbar {
  position: sticky;
  top: 0;
  z-index: 30;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  height: 56px;
  padding: 0 20px;
  background: #fff;
  border-bottom: 1px solid #f0f0f0;
}
.top-left {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
}
.crumb {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12.5px;
  color: #86909c;
  white-space: nowrap;
}
.crumb-current {
  color: #1f2329;
  font-weight: 500;
}
.menu-btn {
  display: none;
  width: 32px;
  height: 32px;
  align-items: center;
  justify-content: center;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  background: #fff;
  color: #4e5969;
  cursor: pointer;
}
.top-right {
  display: flex;
  align-items: center;
  gap: 12px;
}
.scope-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  height: 26px;
  padding: 0 10px;
  border-radius: 4px;
  background: #f2f3f5;
  color: #4e5969;
  font-size: 12px;
  white-space: nowrap;
}
.icon-btn {
  position: relative;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: 6px;
  background: transparent;
  color: #4e5969;
  cursor: pointer;
  transition: all 0.15s;
}
.icon-btn:hover {
  background: #f2f3f5;
  color: #1f2329;
}
.icon-btn .dot {
  position: absolute;
  top: 7px;
  right: 8px;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #ff4d4f;
  box-shadow: 0 0 0 2px #fff;
}
.user {
  display: flex;
  align-items: center;
  gap: 8px;
  padding-left: 12px;
  border-left: 1px solid #f0f0f0;
}
.user-text {
  display: flex;
  flex-direction: column;
  gap: 1px;
  white-space: nowrap;
}
.user-text b {
  font-size: 13px;
  color: #1f2329;
}
.user-text span {
  font-size: 11px;
  color: #86909c;
}
.content {
  width: 100%;
  max-width: 1600px;
  margin: 0 auto;
  padding: 20px 20px 40px;
}
.sidebar-mask {
  display: none;
}
@media (max-width: 1100px) {
  .content {
    padding: 16px 16px 32px;
  }
  .topbar {
    padding: 0 16px;
  }
  .scope-chip {
    display: none;
  }
}
@media (max-width: 900px) {
  .sidebar {
    position: fixed;
    left: 0;
    top: 0;
    transform: translateX(-102%);
    transition: transform 0.24s ease;
    box-shadow: 20px 0 50px rgba(30, 50, 90, 0.12);
  }
  .sidebar.mobile-open {
    transform: translateX(0);
  }
  .sidebar-mask {
    display: block;
    position: fixed;
    inset: 0;
    z-index: 35;
    background: rgba(26, 36, 58, 0.36);
    backdrop-filter: blur(2px);
  }
  .menu-btn {
    display: flex;
  }
  .user-text {
    display: none;
  }
  .user {
    padding-left: 10px;
  }
}
@media (max-width: 560px) {
  .crumb-muted,
  .crumb svg {
    display: none;
  }
  .content {
    padding: 14px 12px 30px;
  }
  .topbar {
    padding: 0 12px;
    height: 58px;
  }
}
</style>
