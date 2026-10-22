<!-- 教师端整体布局：左侧固定侧栏 + 右侧顶栏/内容区 -->
<template>
  <div class="app">
    <aside class="sidebar">
      <div class="logo" @click="$router.push('/teacher/dashboard')">
        <svg viewBox="0 0 24 24" width="28" height="28" fill="none">
          <path d="M12 2a10 10 0 1 0 0 20c1.1 0 2-.9 2-2 0-.5-.2-1-.5-1.3-.3-.4-.5-.8-.5-1.2 0-1.1.9-2 2-2h2.3A4.7 4.7 0 0 0 22 10.8C21.9 5.9 17.4 2 12 2Z" fill="url(#t-lg)"/>
          <circle cx="7.5" cy="10.5" r="1.4" fill="#fff"/>
          <circle cx="12" cy="7.5" r="1.4" fill="#fff"/>
          <circle cx="16.5" cy="10.5" r="1.4" fill="#fff"/>
          <defs>
            <linearGradient id="t-lg" x1="0" y1="0" x2="24" y2="24">
              <stop stop-color="#3f8ef7"/><stop offset="1" stop-color="#7b6cf0"/>
            </linearGradient>
          </defs>
        </svg>
        <span>艺术测评 · 教师端</span>
      </div>

      <nav class="nav">
        <div v-for="group in sidebar" :key="group.name" class="group">
          <div class="group-title">{{ group.name }}</div>
          <router-link
            v-for="item in group.items"
            :key="item.path"
            :to="item.path"
            class="nav-item"
            :class="{ active: isActive(item.path) }"
          >
            <span v-if="item.icon" class="nav-icon">{{ item.icon }}</span>
            {{ item.label }}
          </router-link>
        </div>
      </nav>
    </aside>

    <div class="right">
      <header class="topbar">
        <div class="breadcrumb">
          <span v-for="(b, i) in breadcrumb" :key="i">
            <span v-if="i > 0" class="sep">/</span>
            <span>{{ b }}</span>
          </span>
        </div>
        <div class="topbar-right">
          <button class="btn-home" @click="$router.push('/')">返回主页</button>
          <div class="user">
            <div class="avatar">师</div>
            <span class="user-name">老师</span>
            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="#8a93a5" stroke-width="2.2" stroke-linecap="round"><path d="m6 9 6 6 6-6"/></svg>
          </div>
        </div>
      </header>

      <main class="content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { api } from '../api'

const route = useRoute()
const sidebar = ref([])

onMounted(async () => {
  try {
    sidebar.value = await api.teacher.sidebar()
  } catch {
    sidebar.value = []
  }
})

function isActive(path) {
  if (!path) return false
  return route.path === path || route.path.startsWith(path + '/')
}

const breadcrumb = computed(() => {
  const crumbs = ['教师端']
  const title = route.meta?.title
  if (title) crumbs.push(title)
  return crumbs
})
</script>

<style scoped>
.app {
  min-height: 100vh;
  display: flex;
  background: #fdfcf9;
}
.sidebar {
  width: 220px;
  flex-shrink: 0;
  background: linear-gradient(180deg, #eef4ff, #faf6ff);
  border-right: 1px solid #eef1f6;
  padding: 22px 0;
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
}
.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0 22px 24px;
  font-size: 15px;
  font-weight: 700;
  color: #2b3445;
  cursor: pointer;
  border-bottom: 1px solid rgba(120, 130, 180, 0.15);
}
.group { padding: 14px 14px 4px; }
.group-title {
  padding: 8px 10px 6px;
  font-size: 12px;
  color: #8a93a5;
  letter-spacing: 2px;
}
.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  margin: 2px 0;
  border-radius: 10px;
  font-size: 14px;
  color: #556074;
  transition: background 0.2s, color 0.2s;
  position: relative;
}
.nav-item:hover {
  background: rgba(123, 108, 240, 0.08);
  color: #3f5fd4;
}
.nav-item.active {
  background: linear-gradient(90deg, rgba(63, 142, 247, 0.12), rgba(123, 108, 240, 0.12));
  color: #2b3fa8;
  font-weight: 600;
}
.nav-item.active::before {
  content: '';
  position: absolute;
  left: -14px;
  top: 10px;
  bottom: 10px;
  width: 4px;
  border-radius: 3px;
  background: linear-gradient(180deg, #3f8ef7, #7b6cf0);
}
.nav-icon { font-size: 16px; }
.right { flex: 1; display: flex; flex-direction: column; min-width: 0; }
.topbar {
  height: 58px;
  padding: 0 28px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #fff;
  border-bottom: 1px solid #eef1f6;
  position: sticky;
  top: 0;
  z-index: 5;
}
.breadcrumb { font-size: 14px; color: #8a93a5; }
.breadcrumb .sep { margin: 0 8px; color: #cfd5e2; }
.breadcrumb span:last-child { color: #2b3445; font-weight: 600; }
.topbar-right { display: flex; align-items: center; gap: 16px; }
.btn-home {
  padding: 7px 16px;
  border-radius: 999px;
  font-size: 13px;
  color: #3f8ef7;
  border: 1px solid #c9d6ee;
  background: #fff;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-home:hover { background: #eef4ff; }
.user {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #2b3445;
  cursor: pointer;
}
.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3f8ef7, #7b6cf0);
  color: #fff;
  font-size: 13px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.content { padding: 28px; }
</style>
