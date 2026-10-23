<!-- 登录页：以「登录背景图.jpg」为整屏背景，左侧留白区域放置玻璃质感登录卡片 -->
<template>
  <div class="login-page">
    <!-- 整屏背景图 -->
    <div class="bg-layer" :style="{ backgroundImage: `url(${bgUrl})` }"></div>
    <div class="bg-veil"></div>

    <!-- 返回首页 -->
    <button class="back-home" @click="$router.push('/')">
      <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M19 12H5"/><path d="m12 19-7-7 7-7"/>
      </svg>
      返回首页
    </button>

    <!-- 登录卡片：落在背景图左侧的空白区域 -->
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

      <h1 class="title">欢迎登录</h1>
      <p class="slogan">以艺术为桥 · 发现更好的你</p>

      <div class="divider"></div>

      <p class="label">请选择你的身份</p>

      <div class="role-list">
        <button
          v-for="r in roles"
          :key="r.key"
          class="role-btn"
          :class="[r.key, { selected: selected === r.key, wide: r.wide }]"
          @click="selected = r.key"
        >
          <span class="role-icon" v-html="r.icon"></span>
          <span class="role-text">
            <span class="role-title">{{ r.title }}</span>
            <span class="role-sub">{{ r.sub }}</span>
          </span>
          <span class="radio" :class="{ on: selected === r.key }"></span>
        </button>
      </div>

      <button class="submit" :disabled="!selected" @click="doLogin">
        <span>{{ loading ? '正在进入…' : '进入系统' }}</span>
        <svg v-if="!loading" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M5 12h14"/><path d="m13 6 6 6-6 6"/>
        </svg>
      </button>

      <p class="tip">首次使用？<button class="inline-link" type="button" @click="$router.push('/register')">立即注册</button></p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { api } from '../api'
import bgUrl from '../assets/login-bg.jpg'

const route = useRoute()
const router = useRouter()
const selected = ref('')
const loading = ref(false)

// 七类身份：学生、教师、学校 / 区县 / 市州管理员、省级管理员、题库管理员
const iconBase = 'viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"'
const roles = [
  {
    key: 'student',
    title: '学生登录',
    sub: '参加测评 · 查看成长曲线',
    to: '/student/dashboard',
    icon: `<svg ${iconBase}><path d="M22 10 12 5 2 10l10 5 10-5Z"/><path d="M6 12v5c0 1.5 2.7 3 6 3s6-1.5 6-3v-5"/></svg>`,
  },
  {
    key: 'teacher',
    title: '教师登录',
    sub: '管理班级 · 发布测评任务',
    to: '/teacher/dashboard',
    icon: `<svg ${iconBase}><path d="M4 19.5V5a2 2 0 0 1 2-2h13v18H6a2 2 0 0 1-2-2v-.5Z"/><path d="M8 7h8M8 11h8"/></svg>`,
  },
  {
    key: 'school',
    title: '学校管理员',
    sub: '本校数据 · 账号班级',
    to: '/admin/dashboard?role=school',
    icon: `<svg ${iconBase}><path d="M3 21h18"/><path d="M5 21V8l7-5 7 5v13"/><path d="M9 21v-6h6v6"/></svg>`,
  },
  {
    key: 'district',
    title: '区县管理员',
    sub: '辖区学校 · 测评统计',
    to: '/admin/dashboard?role=district',
    icon: `<svg ${iconBase}><path d="M3 9.5 12 3l9 6.5"/><path d="M5 21V11h14v10"/><path d="M9 21v-5h6v5"/></svg>`,
  },
  {
    key: 'city',
    title: '市州管理员',
    sub: '全市数据 · 汇总上报',
    to: '/admin/dashboard?role=city',
    icon: `<svg ${iconBase}><path d="M3 21h18"/><path d="M6 21V6l6-3 6 3v15"/><path d="M10 21v-4h4v4"/><path d="M9 9h1M14 9h1"/></svg>`,
  },
  {
    key: 'provincial',
    title: '省级管理员',
    sub: '全省数据 · 组卷发布',
    to: '/provincial/dashboard',
    icon: `<svg ${iconBase}><path d="M12 2 3 7v6c0 5 3.8 8 9 9 5.2-1 9-4 9-9V7l-9-5Z"/><path d="M9 12h6"/></svg>`,
  },
  {
    key: 'questionbank',
    title: '题库管理员',
    sub: '试题审核 · 课程章节',
    to: '/questionbank/dashboard',
    wide: true,
    icon: `<svg ${iconBase}><path d="M4 19.5V5a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2Z"/><path d="M9.1 9a3 3 0 0 1 5.8 1c0 2-3 2-3 4"/><path d="M12 17h.01"/></svg>`,
  },
]

onMounted(() => {
  selected.value = route.query.role || ''
})

async function doLogin() {
  if (!selected.value || loading.value) return
  loading.value = true
  const target = roles.find(r => r.key === selected.value)?.to || '/student/dashboard'
  try {
    await api.login(selected.value)
  } catch {
    // 后端未启动时静默失败，便于纯前端预览
  }
  loading.value = false
  router.push(target)
}
</script>

<style scoped>
.login-page {
  position: relative;
  min-height: 100vh;
  width: 100%;
  overflow: hidden;
}

/* ---------- 背景图 ---------- */
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
/* 左侧提亮，保证表单可读；右侧保留画面 */
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

/* ---------- 返回首页 ---------- */
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

/* ---------- 登录卡片 ---------- */
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

.brand { display: flex; align-items: center; gap: 10px; margin-bottom: 40px; }
.brand-icon { display: flex; }
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
  margin: 26px 0 30px;
  border-radius: 2px;
  background: linear-gradient(90deg, #3f8ef7, #7b6cf0);
}
.label { margin: 0 0 14px; font-size: 13px; color: #8a93a5; letter-spacing: 1px; }

/* ---------- 身份选择 ---------- */
.role-list {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.role-btn {
  position: relative;
  display: flex;
  align-items: center;
  gap: 9px;
  width: 100%;
  padding: 12px 11px;
  font-family: inherit;
  text-align: left;
  border: 1.5px solid rgba(216, 225, 240, 0.96);
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.76);
  backdrop-filter: blur(10px);
  cursor: pointer;
  transition: all 0.24s;
}
/* 题库管理员独占一行，横向更舒展 */
.role-btn.wide {
  grid-column: 1 / -1;
  padding: 14px 16px;
}
.role-btn:hover {
  background: rgba(255, 255, 255, 0.94);
  border-color: #c2d3ee;
  transform: translateY(-2px);
  box-shadow: 0 8px 22px rgba(80, 110, 180, 0.12);
}
.role-btn.selected.student {
  border-color: #3f8ef7;
  background: linear-gradient(100deg, rgba(238, 244, 255, 0.97), rgba(255, 255, 255, 0.94));
  box-shadow: 0 8px 24px rgba(63, 142, 247, 0.24);
}
.role-btn.selected.teacher {
  border-color: #7b6cf0;
  background: linear-gradient(100deg, rgba(246, 241, 255, 0.97), rgba(255, 255, 255, 0.94));
  box-shadow: 0 8px 24px rgba(123, 108, 240, 0.24);
}
.role-btn.selected.school {
  border-color: #f2a03d;
  background: linear-gradient(100deg, rgba(255, 247, 235, 0.97), rgba(255, 255, 255, 0.94));
  box-shadow: 0 8px 24px rgba(242, 160, 61, 0.24);
}
.role-btn.selected.district {
  border-color: #26b3a7;
  background: linear-gradient(100deg, rgba(235, 250, 248, 0.97), rgba(255, 255, 255, 0.94));
  box-shadow: 0 8px 24px rgba(38, 179, 167, 0.24);
}
.role-btn.selected.city {
  border-color: #5a6fd8;
  background: linear-gradient(100deg, rgba(238, 240, 255, 0.97), rgba(255, 255, 255, 0.94));
  box-shadow: 0 8px 24px rgba(90, 111, 216, 0.24);
}
.role-btn.selected.provincial {
  border-color: #f2709c;
  background: linear-gradient(100deg, rgba(255, 241, 247, 0.97), rgba(255, 255, 255, 0.94));
  box-shadow: 0 8px 24px rgba(242, 112, 156, 0.24);
}
.role-btn.selected.questionbank {
  border-color: #2fbfa5;
  background: linear-gradient(100deg, rgba(237, 250, 246, 0.97), rgba(255, 255, 255, 0.94));
  box-shadow: 0 8px 24px rgba(47, 191, 165, 0.24);
}

.role-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  flex: 0 0 34px;
  border-radius: 10px;
  color: #3f8ef7;
  background: rgba(63, 142, 247, 0.1);
  transition: all 0.24s;
}
.teacher .role-icon { color: #7b6cf0; background: rgba(123, 108, 240, 0.1); }
.school .role-icon { color: #f2a03d; background: rgba(242, 160, 61, 0.12); }
.district .role-icon { color: #26b3a7; background: rgba(38, 179, 167, 0.12); }
.city .role-icon { color: #5a6fd8; background: rgba(90, 111, 216, 0.12); }
.provincial .role-icon { color: #f2709c; background: rgba(242, 112, 156, 0.12); }
.questionbank .role-icon { color: #2fbfa5; background: rgba(47, 191, 165, 0.12); }

.selected.student .role-icon { color: #fff; background: linear-gradient(135deg, #3f8ef7, #6aa6fb); }
.selected.teacher .role-icon { color: #fff; background: linear-gradient(135deg, #7b6cf0, #a48eff); }
.selected.school .role-icon { color: #fff; background: linear-gradient(135deg, #f2a03d, #f7c079); }
.selected.district .role-icon { color: #fff; background: linear-gradient(135deg, #26b3a7, #63d4c9); }
.selected.city .role-icon { color: #fff; background: linear-gradient(135deg, #5a6fd8, #8d9bf0); }
.selected.provincial .role-icon { color: #fff; background: linear-gradient(135deg, #f2709c, #f79fb8); }
.selected.questionbank .role-icon { color: #fff; background: linear-gradient(135deg, #2fbfa5, #63d4bd); }

.role-text { display: flex; flex-direction: column; flex: 1; min-width: 0; }
.role-title { font-size: 13px; font-weight: 700; color: #2b3445; white-space: nowrap; }
.role-sub {
  margin-top: 2px;
  font-size: 10px;
  color: #8a93a5;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.role-btn.wide .role-title { font-size: 14px; }
.role-btn.wide .role-sub { font-size: 11px; }
.role-btn.wide .role-icon { width: 38px; height: 38px; flex: 0 0 38px; }

.radio {
  width: 14px;
  height: 14px;
  flex: 0 0 14px;
  border-radius: 50%;
  border: 1.5px solid #c9d6ee;
  background: #fff;
  transition: all 0.24s;
}
.role-btn.wide .radio { width: 16px; height: 16px; flex: 0 0 16px; }
.radio.on {
  border-color: transparent;
  background: radial-gradient(circle at center, #fff 0 3px, #3f8ef7 3.5px);
}
.teacher.selected .radio.on { background: radial-gradient(circle at center, #fff 0 3px, #7b6cf0 3.5px); }
.school.selected .radio.on { background: radial-gradient(circle at center, #fff 0 3px, #f2a03d 3.5px); }
.district.selected .radio.on { background: radial-gradient(circle at center, #fff 0 3px, #26b3a7 3.5px); }
.city.selected .radio.on { background: radial-gradient(circle at center, #fff 0 3px, #5a6fd8 3.5px); }
.provincial.selected .radio.on { background: radial-gradient(circle at center, #fff 0 3px, #f2709c 3.5px); }
.questionbank.selected .radio.on { background: radial-gradient(circle at center, #fff 0 3px, #2fbfa5 3.5px); }

/* ---------- 提交 ---------- */
.submit {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  margin-top: 26px;
  padding: 14px 0;
  font-size: 15px;
  letter-spacing: 3px;
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
.submit:disabled { opacity: 0.45; cursor: not-allowed; box-shadow: none; }

.tip {
  margin: 22px 0 0;
  font-size: 12px;
  color: #9aa3b5;
  letter-spacing: 0.5px;
}

.inline-link {
  margin-left: 4px;
  padding: 0;
  border: none;
  background: transparent;
  color: #2f6fe4;
  font-size: 12px;
  font-family: inherit;
  cursor: pointer;
}

/* ---------- 响应式 ---------- */
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
  .role-list { grid-template-columns: repeat(2, 1fr); }
  .title { font-size: 28px; }
}
@media (max-width: 440px) {
  .role-list { grid-template-columns: 1fr; }
}
</style>
