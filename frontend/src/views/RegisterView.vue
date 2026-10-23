<template>
  <div class="login-page">
    <div class="bg-layer" :style="{ backgroundImage: `url(${bgUrl})` }"></div>
    <div class="bg-veil"></div>

    <button class="back-home" @click="$router.push('/')">
      <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M19 12H5"/><path d="m12 19-7-7 7-7"/>
      </svg>
      返回首页
    </button>

    <div class="login-card">
      <div class="brand">
        <span class="brand-icon">
          <svg viewBox="0 0 24 24" width="34" height="34" fill="none">
            <path d="M12 2a10 10 0 1 0 0 20c1.1 0 2-.9 2-2 0-.5-.2-1-.5-1.3-.3-.4-.5-.8-.5-1.2 0-1.1.9-2 2-2h2.3A4.7 4.7 0 0 0 22 10.8C21.9 5.9 17.4 2 12 2Z" fill="url(#lg3)"/>
            <circle cx="7.5" cy="10.5" r="1.4" fill="#fff"/>
            <circle cx="12" cy="7.5" r="1.4" fill="#fff"/>
            <circle cx="16.5" cy="10.5" r="1.4" fill="#fff"/>
            <defs>
              <linearGradient id="lg3" x1="0" y1="0" x2="24" y2="24">
                <stop stop-color="#3f8ef7"/><stop offset=".55" stop-color="#7b6cf0"/><stop offset="1" stop-color="#f2709c"/>
              </linearGradient>
            </defs>
          </svg>
        </span>
        <span class="brand-text">艺术测评系统</span>
      </div>

      <h1 class="title">创建账号</h1>
      <p class="slogan">开启你的艺术成长之旅</p>

      <div class="divider"></div>

      <form class="register-form" @submit.prevent="submitRegister">
        <div class="field-row">
          <label class="form-field">
            <span>真实姓名</span>
            <input v-model="form.name" type="text" placeholder="请输入真实姓名" />
          </label>
          <label class="form-field">
            <span>手机号</span>
            <input v-model="form.phone" type="tel" placeholder="请输入手机号" />
          </label>
        </div>

        <div class="field-row">
          <label class="form-field">
            <span>账号名</span>
            <input v-model="form.username" type="text" placeholder="设置登录账号" />
          </label>
          <label class="form-field">
            <span>所在学校</span>
            <input v-model="form.school" type="text" placeholder="例如：XX中学" />
          </label>
        </div>

        <label class="form-field full">
          <span>选择身份</span>
          <select v-model="form.role">
            <option value="">请选择你的身份</option>
            <option v-for="role in roles" :key="role.value" :value="role.value">
              {{ role.label }}
            </option>
          </select>
        </label>

        <div class="field-row">
          <label class="form-field">
            <span>密码</span>
            <input v-model="form.password" type="password" placeholder="请输入密码" />
          </label>
          <label class="form-field">
            <span>确认密码</span>
            <input v-model="form.confirmPassword" type="password" placeholder="请再次输入密码" />
          </label>
        </div>

        <label class="agreement">
          <input v-model="agree" type="checkbox" />
          <span>我已阅读并同意《艺术测评系统用户协议》</span>
        </label>

        <button class="submit" type="submit" :disabled="submitting || !canSubmit">
          <span>{{ submitting ? '正在注册…' : '立即注册' }}</span>
          <svg v-if="!submitting" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M5 12h14"/><path d="m13 6 6 6-6 6"/>
          </svg>
        </button>

        <div class="login-link-row">
          <span>已有账号？</span>
          <button type="button" class="text-btn" @click="$router.push('/login')">立即登录</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import bgUrl from '../assets/login-bg.jpg'

const router = useRouter()
const agree = ref(false)
const submitting = ref(false)

const roles = [
  { value: 'student', label: '学生' },
  { value: 'teacher', label: '教师' },
  { value: 'school', label: '学校管理员' },
  { value: 'district', label: '区县管理员' },
  { value: 'city', label: '市州管理员' },
  { value: 'provincial', label: '省级管理员' },
  { value: 'questionbank', label: '题库管理员' },
]

const form = ref({
  name: '',
  phone: '',
  username: '',
  school: '',
  role: '',
  password: '',
  confirmPassword: '',
})

const canSubmit = computed(() => {
  return (
    form.value.name &&
    form.value.phone &&
    form.value.username &&
    form.value.school &&
    form.value.role &&
    form.value.password &&
    form.value.confirmPassword &&
    form.value.password === form.value.confirmPassword &&
    agree.value
  )
})

function submitRegister() {
  if (!canSubmit.value || submitting.value) return

  submitting.value = true

  setTimeout(() => {
    submitting.value = false
    router.push(`/login?role=${form.value.role}`)
  }, 700)
}
</script>

<style scoped>
.login-page {
  position: relative;
  min-height: 100vh;
  width: 100%;
  overflow: hidden;
}

.bg-layer {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center right;
  background-repeat: no-repeat;
  animation: bgFade 1.1s ease-out both;
}

@keyframes bgFade {
  from { opacity: 0; transform: scale(1.04); }
  to { opacity: 1; transform: scale(1); }
}

.bg-veil {
  position: absolute;
  inset: 0;
  background: linear-gradient(100deg,
    rgba(253, 252, 249, 0.94) 0%,
    rgba(253, 252, 249, 0.82) 32%,
    rgba(253, 252, 249, 0.34) 55%,
    rgba(253, 252, 249, 0.02) 78%);
  pointer-events: none;
}

.back-home {
  position: absolute;
  top: 26px;
  left: 32px;
  z-index: 3;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px 8px 13px;
  font-size: 13px;
  font-family: inherit;
  color: #5c6a80;
  background: rgba(255, 255, 255, 0.72);
  border: 1px solid rgba(200, 214, 235, 0.9);
  border-radius: 999px;
  cursor: pointer;
  backdrop-filter: blur(8px);
  transition: all 0.22s;
}

.back-home:hover {
  color: #2f6fe4;
  background: #fff;
  box-shadow: 0 4px 16px rgba(80, 110, 180, 0.16);
  transform: translateX(-2px);
}

.login-card {
  position: relative;
  z-index: 2;
  width: 620px;
  margin-left: 7vw;
  min-height: 100vh;
  padding: 64px 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  animation: cardIn 0.75s cubic-bezier(0.22, 0.9, 0.3, 1) both;
}

@keyframes cardIn {
  from { opacity: 0; transform: translateX(-26px); }
  to { opacity: 1; transform: translateX(0); }
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 30px;
}

.brand-icon {
  display: flex;
}

.brand-text {
  font-size: 19px;
  font-weight: 700;
  letter-spacing: 1px;
  color: #1f2a44;
}

.title {
  margin: 0;
  font-size: 34px;
  font-weight: 700;
  letter-spacing: 2px;
  color: #1f2a44;
  font-family: 'KaiTi', 'STKaiti', 'PingFang SC', serif;
  background: linear-gradient(96deg, #3f8ef7 0%, #7b6cf0 52%, #f2a03d 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.slogan {
  margin: 10px 0 0;
  font-size: 14px;
  letter-spacing: 2px;
  color: #8a93a5;
}

.divider {
  width: 54px;
  height: 3px;
  margin: 26px 0 18px;
  border-radius: 2px;
  background: linear-gradient(90deg, #3f8ef7, #7b6cf0);
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.field-row {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-size: 13px;
  color: #5c6a80;
}

.form-field.full {
  width: 100%;
}

.form-field span {
  font-weight: 600;
}

.form-field input,
.form-field select {
  width: 100%;
  height: 46px;
  padding: 0 14px;
  border: 1px solid #dfe8f5;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.82);
  font-family: inherit;
  font-size: 14px;
  color: #2b3445;
  outline: none;
  box-sizing: border-box;
  transition: all 0.2s ease;
}

.form-field input:focus,
.form-field select:focus {
  border-color: #8ab7ff;
  box-shadow: 0 0 0 4px rgba(79, 156, 249, 0.1);
}

.agreement {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: #7d8897;
  cursor: pointer;
}

.agreement input {
  width: 15px;
  height: 15px;
  accent-color: #3f8ef7;
}

.submit {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  margin-top: 8px;
  padding: 14px 0;
  font-size: 15px;
  letter-spacing: 2px;
  font-family: inherit;
  color: #fff;
  border: none;
  border-radius: 999px;
  cursor: pointer;
  background: linear-gradient(96deg, #3f8ef7, #7b6cf0);
  box-shadow: 0 8px 24px rgba(83, 122, 235, 0.36);
  transition: all 0.24s;
}

.submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 11px 30px rgba(83, 122, 235, 0.46);
}

.submit:disabled {
  opacity: 0.45;
  cursor: not-allowed;
  box-shadow: none;
}

.login-link-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  margin-top: 6px;
  font-size: 13px;
  color: #7d8897;
}

.text-btn {
  padding: 0;
  border: none;
  background: transparent;
  font-family: inherit;
  font-size: 13px;
  color: #2f6fe4;
  cursor: pointer;
}

@media (max-width: 1100px) {
  .login-card { margin-left: 5vw; width: 560px; }
}

@media (max-width: 820px) {
  .bg-veil {
    background: linear-gradient(180deg,
      rgba(253, 252, 249, 0.95) 0%,
      rgba(253, 252, 249, 0.88) 60%,
      rgba(253, 252, 249, 0.72) 100%);
  }

  .login-card {
    width: min(620px, 100%);
    margin: 0 auto;
    padding: 88px 22px 48px;
  }

  .back-home { top: 18px; left: 18px; }
}

@media (max-width: 620px) {
  .field-row { grid-template-columns: 1fr; }
  .title { font-size: 28px; }
}
</style>
