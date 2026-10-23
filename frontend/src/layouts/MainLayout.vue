<template>
  <div class="page">
    <!-- 与主页完全一致的顶栏 -->
    <header class="header">
      <div class="header-inner">
        <div class="logo" @click="$router.push('/')">
          <span class="logo-icon">
            <svg viewBox="0 0 24 24" width="26" height="26" fill="none">
              <path d="M12 2a10 10 0 1 0 0 20c1.1 0 2-.9 2-2 0-.5-.2-1-.5-1.3-.3-.4-.5-.8-.5-1.2 0-1.1.9-2 2-2h2.3A4.7 4.7 0 0 0 22 10.8C21.9 5.9 17.4 2 12 2Z" fill="url(#lg)"/>
              <circle cx="7.5" cy="10.5" r="1.4" fill="#fff"/>
              <circle cx="12" cy="7.5" r="1.4" fill="#fff"/>
              <circle cx="16.5" cy="10.5" r="1.4" fill="#fff"/>
              <defs>
                <linearGradient id="lg" x1="0" y1="0" x2="24" y2="24">
                  <stop stop-color="#4f9cf9"/><stop offset=".5" stop-color="#a06ee8"/><stop offset="1" stop-color="#f2709c"/>
                </linearGradient>
              </defs>
            </svg>
          </span>
          <span class="logo-text">艺术测评系统</span>
        </div>

        <nav class="nav">
          <router-link
            v-for="item in navItems"
            :key="item.name"
            :to="item.path"
            class="nav-item"
            :class="{ active: isActive(item.path) }"
          >{{ item.name }}</router-link>
        </nav>

        <div class="header-right">
          <label class="search">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#9aa3b2" stroke-width="2" stroke-linecap="round">
              <circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>
            </svg>
            <input type="text" placeholder="搜索功能、内容..." />
          </label>
          <button type="button" class="btn btn-outline" @click="showLoginModal = true">登录</button>
          <router-link to="/register" class="btn btn-outline">注册</router-link>
        </div>
      </div>
    </header>

    <main class="main">
      <router-view />
    </main>

    <BaseModal v-model="showLoginModal" title="登录" subtitle="请输入账号和密码后进入系统" width="420px">
      <form class="login-modal-form" @submit.prevent="submitLoginModal">
        <label class="login-field">
          <span>账号</span>
          <input v-model="loginForm.username" type="text" placeholder="请输入账号" />
        </label>
        <label class="login-field">
          <span>密码</span>
          <input v-model="loginForm.password" type="password" placeholder="请输入密码" />
        </label>
        <p v-if="loginError" class="login-error">{{ loginError }}</p>
        <button class="login-submit" type="submit">进入系统</button>
      </form>
    </BaseModal>

    <!-- 与主页一致的页脚 -->
    <footer class="footer">
      <div class="footer-inner">
        <div class="footer-left">
          <span class="logo-icon">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="none">
              <path d="M12 2a10 10 0 1 0 0 20c1.1 0 2-.9 2-2 0-.5-.2-1-.5-1.3-.3-.4-.5-.8-.5-1.2 0-1.1.9-2 2-2h2.3A4.7 4.7 0 0 0 22 10.8C21.9 5.9 17.4 2 12 2Z" fill="url(#lg2)"/>
              <circle cx="7.5" cy="10.5" r="1.4" fill="#fff"/>
              <circle cx="12" cy="7.5" r="1.4" fill="#fff"/>
              <circle cx="16.5" cy="10.5" r="1.4" fill="#fff"/>
              <defs>
                <linearGradient id="lg2" x1="0" y1="0" x2="24" y2="24">
                  <stop stop-color="#4f9cf9"/><stop offset=".5" stop-color="#a06ee8"/><stop offset="1" stop-color="#f2709c"/>
                </linearGradient>
              </defs>
            </svg>
          </span>
          <span>艺术，让生活更有色彩</span>
        </div>
        <div class="footer-right">—— 艺术测评系统 ——</div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import BaseModal from '../components/BaseModal.vue'

const route = useRoute()
const router = useRouter()

const showLoginModal = ref(false)
const loginForm = ref({ username: '', password: '' })
const loginError = ref('')

const navItems = [
  { name: '首页', path: '/' },
  { name: '测评练习', path: '/practice' },
  { name: '成绩分析', path: '/analysis' },
  { name: '个人中心', path: '/profile' },
  { name: '系统帮助', path: '/help' },
]

function isActive(p) {
  if (p === '/') return route.path === '/'
  return route.path.startsWith(p.split('?')[0])
}

function submitLoginModal() {
  const username = loginForm.value.username.trim()
  const password = loginForm.value.password.trim()

  if (!username || !password) {
    loginError.value = '请输入账号和密码后再登录。'
    return
  }

  loginError.value = ''
  showLoginModal.value = false
  loginForm.value = { username: '', password: '' }
  router.push('/student/dashboard')
}
</script>

<style scoped>
.page { min-height: 100vh; display: flex; flex-direction: column; }

.header {
  position: sticky; top: 0; z-index: 10;
  background: rgba(255,255,255,0.92);
  backdrop-filter: blur(8px);
  box-shadow: 0 1px 6px rgba(60,70,100,0.08);
}
.header-inner {
  max-width: 1280px; margin: 0 auto; padding: 0 32px;
  height: 64px; display: flex; align-items: center; gap: 40px;
}
.logo { display: flex; align-items: center; gap: 8px; font-size: 19px; font-weight: 700; color: #1f2a44; cursor: pointer; white-space: nowrap; }
.nav { display: flex; gap: 34px; flex: 1; }
.nav-item {
  position: relative; font-size: 15px; color: #4a5568; padding: 20px 2px;
}
.nav-item:hover { color: #3b82f6; }
.nav-item.active { color: #2f6fe4; font-weight: 600; }
.nav-item.active::after {
  content: ''; position: absolute; left: 50%; bottom: 12px;
  transform: translateX(-50%); width: 22px; height: 3px; border-radius: 2px; background: #2f6fe4;
}
.header-right { display: flex; align-items: center; gap: 14px; }
.search { display: flex; align-items: center; gap: 6px; background: #f3f5f9; border-radius: 18px; padding: 7px 14px; }
.search input { border: none; outline: none; background: transparent; font-size: 13px; width: 130px; color: #4a5568; }
.btn-outline { display: inline-flex; align-items: center; gap: 5px; font-size: 14px; padding: 7px 16px; border-radius: 18px; border: 1px solid #c9d6ee; color: #2f6fe4; background: #fff; cursor: pointer; }

.login-modal-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.login-field {
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-size: 13px;
  color: #5c6a80;
}
.login-field input {
  width: 100%;
  height: 44px;
  padding: 0 12px;
  border: 1px solid #dfe7f5;
  border-radius: 10px;
  font-size: 14px;
  color: #1f2a44;
  background: #fff;
  outline: none;
  box-sizing: border-box;
}
.login-field input:focus {
  border-color: #8ab7ff;
  box-shadow: 0 0 0 3px rgba(79, 156, 249, 0.12);
}
.login-error {
  margin: 0;
  font-size: 12px;
  color: #d94a4a;
}
.login-submit {
  height: 44px;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  color: #fff;
  background: linear-gradient(90deg, #3f8ef7, #7b6cf0);
  cursor: pointer;
}

.main { flex: 1; }
.footer { background: #fff; border-top: 1px solid #eef1f6; margin-top: auto; }
.footer-inner {
  max-width: 1280px; margin: 0 auto; padding: 20px 32px;
  display: flex; align-items: center; justify-content: space-between; font-size: 13px; color: #8a93a5;
}
.footer-left { display: flex; align-items: center; gap: 8px; }
</style>
