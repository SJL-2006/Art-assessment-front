<template>
  <div class="page">
    <!-- 顶部导航 -->
    <header class="header">
      <div class="header-inner">
        <div class="logo">
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
          <span class="logo-text">{{ data.siteName }}</span>
        </div>

        <nav class="nav">
          <a
            v-for="item in data.nav"
            :key="item.name"
            :href="item.path"
            class="nav-item"
            :class="{ active: item.active }"
            @click.prevent="setActive(item)"
          >{{ item.name }}</a>
        </nav>

        <div class="header-right">
          <label class="search">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#9aa3b2" stroke-width="2" stroke-linecap="round">
              <circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>
            </svg>
            <input type="text" placeholder="搜索功能、内容..." />
          </label>
          <button class="btn btn-ghost">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
              <circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 3.6-6.5 8-6.5s8 2.5 8 6.5"/>
            </svg>
            登录
          </button>
          <button class="btn btn-outline">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
              <path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4Z"/>
            </svg>
            注册
          </button>
        </div>
      </div>
    </header>

    <!-- 英雄区 -->
    <section class="hero">
      <div class="hero-inner">
        <div class="hero-text">
          <p class="hero-tagline">
            {{ data.hero.tagline }}
            <svg class="tagline-swoosh" viewBox="0 0 220 12" preserveAspectRatio="none">
              <path d="M2 9 C 60 2, 160 2, 218 8" fill="none" stroke="#7fb8f5" stroke-width="2.5" stroke-linecap="round"/>
            </svg>
          </p>
          <h1 class="hero-title">{{ data.hero.title }}</h1>
          <p class="hero-subtitle">{{ data.hero.subtitle }}</p>
          <p class="hero-desc">{{ data.hero.description }}</p>
          <button class="hero-btn">
            {{ data.hero.buttonText }}
            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M5 12h14"/><path d="m13 6 6 6-6 6"/>
            </svg>
          </button>
        </div>
      </div>
    </section>

    <!-- 功能卡片 -->
    <section class="features">
      <div class="features-inner">
        <div v-for="card in data.features" :key="card.key" class="card">
          <div class="card-icon" :style="{ background: card.color + '1f', color: card.color }">
            <!-- 调色板 -->
            <svg v-if="card.icon === 'palette'" viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round">
              <path d="M12 3a9 9 0 1 0 0 18c1 0 1.8-.8 1.8-1.8 0-.5-.2-.9-.4-1.2-.3-.3-.4-.7-.4-1.1 0-1 .8-1.8 1.8-1.8h2A4.2 4.2 0 0 0 21 11c-.1-4.5-4-8-9-8Z"/>
              <circle cx="7.6" cy="10.4" r="1.1" fill="currentColor" stroke="none"/>
              <circle cx="12" cy="7.6" r="1.1" fill="currentColor" stroke="none"/>
              <circle cx="16.4" cy="10.4" r="1.1" fill="currentColor" stroke="none"/>
            </svg>
            <!-- 音符 -->
            <svg v-else-if="card.icon === 'music'" viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/>
            </svg>
            <!-- 舞蹈 -->
            <svg v-else-if="card.icon === 'dance'" viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="4.5" r="2"/><path d="M12 8.5c-2.5 1-4.5 1-6-.5M12 8.5c2.5 1 4.5 1 6-.5M12 8.5V13m0 0-3.5 7m3.5-7 3.5 7"/>
            </svg>
            <!-- 书本 -->
            <svg v-else-if="card.icon === 'book'" viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M2 4h6a4 4 0 0 1 4 4v12a3 3 0 0 0-3-3H2Z"/><path d="M22 4h-6a4 4 0 0 0-4 4v12a3 3 0 0 1 3-3h7Z"/>
            </svg>
            <!-- 柱状图 -->
            <svg v-else-if="card.icon === 'chart'" viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round">
              <path d="M3 3v16a2 2 0 0 0 2 2h16"/><path d="M8 17v-5M13 17V8M18 17v-8"/>
            </svg>
            <!-- 报告 -->
            <svg v-else viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z"/><path d="M14 2v6h6"/><path d="M9 13h6M9 17h6"/>
            </svg>
          </div>
          <h3 class="card-title">{{ card.title }}</h3>
          <p v-for="(line, i) in card.lines" :key="i" class="card-line">{{ line }}</p>
          <span class="card-arrow" :style="{ background: card.color + '1f', color: card.color }">
            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M5 12h14"/><path d="m13 6 6 6-6 6"/>
            </svg>
          </span>
        </div>
      </div>
    </section>

    <!-- 页脚 -->
    <footer class="footer">
      <div class="footer-inner">
        <div class="footer-left">
          <span class="logo-icon small">
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
          <span>{{ data.slogan }}</span>
        </div>
        <div class="footer-right">—— {{ data.siteName }} ——</div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { onMounted, reactive } from 'vue'
import { api } from '../api'

// 默认数据（后端未启动时也能正常渲染，启动后由接口数据覆盖）
const data = reactive({
  siteName: '艺术测评系统',
  slogan: '艺术，让生活更有色彩',
  nav: [
    { name: '首页', path: '/', active: true },
    { name: '测评练习', path: '/practice' },
    { name: '成绩分析', path: '/analysis' },
    { name: '个人中心', path: '/profile' },
    { name: '系统帮助', path: '/help' }
  ],
  hero: {
    tagline: '发现艺术之美 · 让成长更有色彩',
    title: '艺术测评系统',
    subtitle: '以艺术为桥 · 发现更好的你',
    description: '通过专业的艺术测评，帮助你全面了解自己的艺术潜能，激发创造力，提升艺术素养，成就更好的未来。',
    buttonText: '开启艺术之旅'
  },
  features: [
    { key: 'art', title: '美术测评', lines: ['发现你的绘画潜能', '感受色彩的魅力'], color: '#2fbfa5', icon: 'palette' },
    { key: 'music', title: '音乐测评', lines: ['聆听你的音乐天赋', '感受旋律的力量'], color: '#a06ee8', icon: 'music' },
    { key: 'dance', title: '舞蹈测评', lines: ['展现你的肢体语言', '释放无限可能'], color: '#f2b23e', icon: 'dance' },
    { key: 'general', title: '综合测评', lines: ['多维度评估', '全面了解艺术素养'], color: '#4f9cf9', icon: 'book' },
    { key: 'analysis', title: '成绩分析', lines: ['数据化分析', '助力成长与提升'], color: '#8b7cf6', icon: 'chart' },
    { key: 'report', title: '个人报告', lines: ['专属艺术成长报告', '记录你的每一步进步'], color: '#f2709c', icon: 'report' }
  ]
})

function setActive(item) {
  data.nav.forEach(n => (n.active = false))
  item.active = true
}

onMounted(async () => {
  try {
    const remote = await api.home()
    Object.assign(data, remote)
  } catch {
    // 后端未启动时使用默认数据
  }
})
</script>

<style scoped>
.page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  font-family: 'PingFang SC', 'Microsoft YaHei', 'Helvetica Neue', sans-serif;
  color: #2b3445;
  background: #fdfcf9;
}

/* ===== 顶部导航 ===== */
.header {
  position: sticky;
  top: 0;
  z-index: 10;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(8px);
  box-shadow: 0 1px 6px rgba(60, 70, 100, 0.08);
}
.header-inner {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 32px;
  height: 64px;
  display: flex;
  align-items: center;
  gap: 40px;
}
.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 19px;
  font-weight: 700;
  color: #1f2a44;
  white-space: nowrap;
}
.logo-icon {
  display: inline-flex;
}
.nav {
  display: flex;
  gap: 34px;
  flex: 1;
}
.nav-item {
  position: relative;
  font-size: 15px;
  color: #4a5568;
  text-decoration: none;
  padding: 20px 2px;
  transition: color 0.2s;
}
.nav-item:hover {
  color: #3b82f6;
}
.nav-item.active {
  color: #2f6fe4;
  font-weight: 600;
}
.nav-item.active::after {
  content: '';
  position: absolute;
  left: 50%;
  bottom: 12px;
  transform: translateX(-50%);
  width: 22px;
  height: 3px;
  border-radius: 2px;
  background: #2f6fe4;
}
.header-right {
  display: flex;
  align-items: center;
  gap: 14px;
}
.search {
  display: flex;
  align-items: center;
  gap: 6px;
  background: #f3f5f9;
  border-radius: 18px;
  padding: 7px 14px;
}
.search input {
  border: none;
  outline: none;
  background: transparent;
  font-size: 13px;
  width: 130px;
  color: #4a5568;
}
.btn {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 14px;
  padding: 7px 16px;
  border-radius: 18px;
  cursor: pointer;
  border: none;
  background: transparent;
  color: #4a5568;
  transition: all 0.2s;
}
.btn-ghost:hover {
  color: #2f6fe4;
}
.btn-outline {
  border: 1px solid #c9d6ee;
  color: #2f6fe4;
}
.btn-outline:hover {
  background: #eef4ff;
}

/* ===== 英雄区 ===== */
.hero {
  background: url('../assets/bg.png') center / cover no-repeat;
}
.hero-inner {
  max-width: 1280px;
  margin: 0 auto;
  padding: 72px 32px 96px;
}
.hero-text {
  max-width: 560px;
}
.hero-tagline {
  position: relative;
  display: inline-block;
  font-size: 16px;
  letter-spacing: 3px;
  color: #4a6a9e;
  transform: rotate(-2deg);
  padding-bottom: 10px;
  margin: 0 0 18px;
}
.tagline-swoosh {
  position: absolute;
  left: 0;
  bottom: 0;
  width: 100%;
  height: 10px;
}
.hero-title {
  margin: 0 0 20px;
  font-family: 'STKaiti', 'KaiTi', 'STSong', 'SimSun', serif;
  font-size: 76px;
  font-weight: 700;
  letter-spacing: 6px;
  line-height: 1.15;
  background: linear-gradient(100deg, #3a8dde 15%, #9b6de3 55%, #f2a03d 90%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}
.hero-subtitle {
  margin: 0 0 22px;
  font-size: 20px;
  letter-spacing: 5px;
  color: #33415e;
  font-weight: 500;
}
.hero-desc {
  margin: 0 0 36px;
  font-size: 14px;
  line-height: 1.9;
  color: #6b7688;
  max-width: 460px;
}
.hero-btn {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  border: none;
  cursor: pointer;
  font-size: 16px;
  color: #fff;
  padding: 14px 34px;
  border-radius: 999px;
  background: linear-gradient(95deg, #3f8ef7, #7b6cf0);
  box-shadow: 0 8px 20px rgba(80, 120, 240, 0.35);
  transition: transform 0.2s, box-shadow 0.2s;
}
.hero-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 26px rgba(80, 120, 240, 0.45);
}

/* ===== 功能卡片 ===== */
.features {
  background: rgba(255, 255, 255, 0.75);
  margin-top: -36px;
}
.features-inner {
  max-width: 1280px;
  margin: 0 auto;
  padding: 40px 32px 56px;
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 22px;
}
.card {
  position: relative;
  background: #fff;
  border-radius: 16px;
  padding: 26px 20px 58px;
  box-shadow: 0 6px 22px rgba(70, 90, 130, 0.08);
  transition: transform 0.25s, box-shadow 0.25s;
}
.card:hover {
  transform: translateY(-6px);
  box-shadow: 0 14px 30px rgba(70, 90, 130, 0.14);
}
.card-icon {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 18px;
}
.card-title {
  margin: 0 0 12px;
  font-size: 18px;
  font-weight: 700;
  color: #2b3445;
}
.card-line {
  margin: 0 0 4px;
  font-size: 13px;
  color: #7a8494;
  line-height: 1.6;
}
.card-arrow {
  position: absolute;
  left: 20px;
  bottom: 18px;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: transform 0.2s;
}
.card:hover .card-arrow {
  transform: translateX(4px);
}

/* ===== 页脚 ===== */
.footer {
  margin-top: auto;
  background: #fff;
  border-top: 1px solid #eef1f6;
}
.footer-inner {
  max-width: 1280px;
  margin: 0 auto;
  padding: 20px 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 13px;
  color: #8a93a5;
}
.footer-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* ===== 响应式 ===== */
@media (max-width: 1100px) {
  .features-inner {
    grid-template-columns: repeat(3, 1fr);
  }
  .hero-title {
    font-size: 56px;
  }
}
@media (max-width: 760px) {
  .header-inner {
    flex-wrap: wrap;
    height: auto;
    padding: 12px 20px;
    gap: 12px;
  }
  .nav {
    order: 3;
    width: 100%;
    justify-content: space-between;
    gap: 8px;
  }
  .features-inner {
    grid-template-columns: repeat(2, 1fr);
    padding: 32px 20px 44px;
  }
  .hero-inner {
    padding: 56px 20px 80px;
  }
  .hero-title {
    font-size: 42px;
  }
}
</style>
