<!-- 学生端工作台：欢迎语 + 统计卡 + 待完成测评 + 最近成绩 + SVG 成绩曲线 -->
<template>
  <div class="page">
    <!-- 欢迎区 -->
    <section class="welcome card">
      <div class="welcome-text">
        <h2>你好，{{ data.name || '同学' }} 同学 👋</h2>
        <p>{{ data.className || '' }} · 今天也是努力成为小小艺术家的一天！</p>
      </div>
      <div class="welcome-deco">
        <div class="deco-blob" style="background:#c6ddff"></div>
        <div class="deco-blob" style="background:#e0d2ff; top:20px; right:-20px;"></div>
        <div class="deco-blob" style="background:#ffe2c0; bottom:-10px; left:30px;"></div>
      </div>
    </section>

    <!-- 统计卡片 -->
    <section class="stats">
      <div v-for="s in statCards" :key="s.label" class="stat">
        <div class="stat-icon" :style="{ background: s.bg, color: s.color }">{{ s.icon }}</div>
        <div class="stat-body">
          <div class="stat-val">{{ s.value }}</div>
          <div class="stat-label">{{ s.label }}</div>
        </div>
        <div class="trend" :style="{ color: s.color }">{{ s.trend }}</div>
      </div>
    </section>

    <!-- 主体两栏 -->
    <section class="main-grid">
      <!-- 左侧：待完成测评 -->
      <div class="card">
        <div class="card-head">
          <h3 class="title-splash">待完成测评</h3>
          <span class="count">{{ upcoming.length }} 项</span>
        </div>
        <ul class="upcoming">
          <li v-for="u in upcoming" :key="u.id" class="up-item">
            <span class="emoji">{{ u.subject === 'music' ? '🎵' : '🎨' }}</span>
            <div class="up-body">
              <div class="up-title">{{ u.title }}</div>
              <div class="up-meta">截止 {{ u.deadline }} · 时长 {{ u.duration }}</div>
            </div>
            <button class="btn-gradient btn-sm">开始</button>
          </li>
          <li v-if="!upcoming.length" class="empty">暂无待完成的测评 🎉</li>
        </ul>
      </div>

      <!-- 右侧：最近成绩 -->
      <div class="card">
        <div class="card-head">
          <h3 class="title-splash">最近成绩</h3>
          <router-link to="/student/curve" class="link">查看曲线 →</router-link>
        </div>
        <table class="scores">
          <thead><tr><th>测评</th><th>类型</th><th>得分</th><th>等级</th></tr></thead>
          <tbody>
            <tr v-for="r in recent" :key="r.id">
              <td>{{ r.title }}</td>
              <td>{{ r.type === 'music' ? '音乐' : '美术' }}</td>
              <td>
                <span class="score" :class="scoreClass(r.score)">{{ r.score }}</span>
              </td>
              <td>{{ r.grade }}</td>
            </tr>
            <tr v-if="!recent.length"><td colspan="4" class="empty">暂无成绩</td></tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- 底部：SVG 成绩曲线 -->
    <section class="card curve-card">
      <div class="card-head">
        <h3 class="title-splash">成绩曲线</h3>
        <div class="legend">
          <span class="lg-item"><i style="background:linear-gradient(90deg,#3f8ef7,#7b6cf0)"></i>音乐</span>
          <span class="lg-item"><i style="background:linear-gradient(90deg,#f2a03d,#f2709c)"></i>美术</span>
        </div>
      </div>
      <svg :viewBox="`0 0 ${svgW} ${svgH}`" class="curve-svg">
        <defs>
          <linearGradient id="gradMusic" x1="0" y1="0" x2="1" y2="0">
            <stop stop-color="#3f8ef7"/><stop offset="1" stop-color="#7b6cf0"/>
          </linearGradient>
          <linearGradient id="gradArt" x1="0" y1="0" x2="1" y2="0">
            <stop stop-color="#f2a03d"/><stop offset="1" stop-color="#f2709c"/>
          </linearGradient>
        </defs>
        <!-- Y 轴网格 -->
        <line v-for="i in 4" :key="'y'+i" :x1="padL" :x2="padL + plotW" :y1="padT + (plotH/3)*(i-1)" :y2="padT + (plotH/3)*(i-1)" stroke="#eef1f6" stroke-dasharray="3,3"/>
        <!-- X 轴标签 -->
        <text v-for="(m, i) in months" :key="m" :x="padL + (plotW/(months.length-1))*i" :y="svgH - 12" fill="#8a93a5" font-size="12" text-anchor="middle">{{ m }}</text>
        <!-- Y 轴标签 -->
        <text v-for="(v, i) in yTicks" :key="'yt'+i" :x="padL - 8" :y="padT + (plotH/3)*i + 4" fill="#8a93a5" font-size="12" text-anchor="end">{{ v }}</text>
        <!-- 音乐线 -->
        <path :d="buildPath(musicPts)" fill="none" stroke="url(#gradMusic)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
        <circle v-for="(p, i) in musicPts" :key="'mc'+i" :cx="p.x" :cy="p.y" r="4" fill="#fff" stroke="#3f8ef7" stroke-width="2"/>
        <!-- 美术线 -->
        <path :d="buildPath(artPts)" fill="none" stroke="url(#gradArt)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
        <circle v-for="(p, i) in artPts" :key="'ac'+i" :cx="p.x" :cy="p.y" r="4" fill="#fff" stroke="#f2a03d" stroke-width="2"/>
      </svg>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { api } from '../../api'

const data = reactive({ name: '', className: '', stats: {}, upcoming: [], recent: [], curve: {} })

onMounted(async () => {
  try {
    const res = await api.student.workspace()
    Object.assign(data, res)
  } catch {
    // 后端未启动时使用占位数据
    Object.assign(data, {
      name: '李明', className: '五(3)班',
      stats: { done: 8, practice: 23, avgScore: 86, certs: 2 },
      upcoming: [
        { id: 1, subject: 'music', title: '五年级音乐素养测评', deadline: '10-28', duration: '40分钟' },
        { id: 2, subject: 'art', title: '色彩感知练习', deadline: '11-02', duration: '30分钟' },
      ],
      recent: [
        { id: 1, title: '音乐正式测评', type: 'music', score: 92, grade: 'A' },
        { id: 2, title: '美术正式测评', type: 'art', score: 85, grade: 'B+' },
        { id: 3, title: '音乐练习', type: 'music', score: 78, grade: 'C+' },
      ],
      curve: {
        music: [78, 80, 82, 81, 85, 88, 92],
        art:   [72, 75, 77, 80, 83, 84, 85],
        months: ['03','04','05','06','07','08','09','10']
      }
    })
  }
})

const statCards = computed(() => [
  { label: '已完成测评', icon: '📝', value: data.stats.done ?? 0, trend: '+2', bg: '#eef4ff', color: '#3f8ef7' },
  { label: '练习次数',   icon: '🎯', value: data.stats.practice ?? 0, trend: '+5', bg: '#f4effe', color: '#7b6cf0' },
  { label: '平均得分',   icon: '📊', value: data.stats.avgScore ?? 0, trend: '+3', bg: '#fff1e0', color: '#f2a03d' },
  { label: '获得证书',   icon: '🏆', value: data.stats.certs ?? 0, trend: '+1', bg: '#e6f9ef', color: '#2fbfa5' },
])

const upcoming = computed(() => data.upcoming || [])
const recent   = computed(() => data.recent || [])

function scoreClass(s) {
  if (s >= 90) return 's-green'
  if (s >= 80) return 's-blue'
  return 's-orange'
}

// --- SVG 坐标 ---
const svgW = 760, svgH = 260
const padL = 44, padR = 20, padT = 20, padB = 30
const plotW = svgW - padL - padR
const plotH = svgH - padT - padB
const yMin = 70, yMax = 100
const yTicks = [100, 90, 80, 70]

const months = computed(() => data.curve?.months || ['03','04','05','06','07','08','09','10'])
const curveMusic = computed(() => data.curve?.music || [])
const curveArt   = computed(() => data.curve?.art   || [])

function pts(values) {
  const n = values.length
  return values.map((v, i) => ({
    x: padL + (plotW / Math.max(n - 1, 1)) * i,
    y: padT + plotH - ((v - yMin) / (yMax - yMin)) * plotH
  }))
}
const musicPts = computed(() => pts(curveMusic.value))
const artPts   = computed(() => pts(curveArt.value))

function buildPath(points) {
  if (!points.length) return ''
  return points.map((p, i) => (i === 0 ? 'M' : 'L') + p.x + ' ' + p.y).join(' ')
}
</script>

<style scoped>
.page { display: flex; flex-direction: column; gap: 22px; }

/* 欢迎区 */
.welcome {
  position: relative;
  overflow: hidden;
  padding: 28px 32px;
  background: linear-gradient(100deg, rgba(63, 142, 247, 0.08), rgba(123, 108, 240, 0.08));
}
.welcome-text h2 { margin: 0 0 6px; font-size: 22px; color: #2b3445; }
.welcome-text p { margin: 0; font-size: 14px; color: #6b7688; }
.welcome-deco { position: absolute; right: 20px; top: 0; width: 140px; height: 140px; }
.deco-blob {
  position: absolute;
  width: 80px; height: 80px;
  border-radius: 50%;
  filter: blur(10px);
  opacity: 0.5;
}

/* 统计卡 */
.stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 18px;
}
.stat {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 22px;
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 4px 20px rgba(70, 90, 130, 0.06);
}
.stat-icon {
  width: 48px; height: 48px;
  border-radius: 12px;
  font-size: 22px;
  display: flex; align-items: center; justify-content: center;
}
.stat-body { flex: 1; }
.stat-val { font-size: 26px; font-weight: 700; color: #2b3445; }
.stat-label { font-size: 13px; color: #8a93a5; margin-top: 2px; }
.trend { font-size: 13px; font-weight: 600; }

/* 两栏 */
.main-grid {
  display: grid;
  grid-template-columns: 1.1fr 1fr;
  gap: 22px;
}
.card-head { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; }
.card-head .count { font-size: 12px; color: #8a93a5; }
.link { font-size: 13px; color: #3f8ef7; }

/* 待完成 */
.upcoming { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 10px; }
.up-item {
  display: flex; align-items: center; gap: 12px;
  padding: 12px 14px;
  background: #fafbff;
  border-radius: 10px;
}
.up-item .emoji { font-size: 22px; }
.up-body { flex: 1; min-width: 0; }
.up-title { font-size: 14px; font-weight: 600; color: #2b3445; }
.up-meta { font-size: 12px; color: #8a93a5; margin-top: 2px; }
.btn-sm { padding: 6px 14px; font-size: 12px; }
.empty { text-align: center; color: #8a93a5; padding: 22px; font-size: 13px; }

/* 成绩表 */
.scores { width: 100%; border-collapse: collapse; font-size: 14px; }
.scores th, .scores td { padding: 12px 8px; text-align: left; border-bottom: 1px solid #eef1f6; }
.scores th { font-size: 12px; color: #8a93a5; font-weight: 500; }
.score { font-weight: 700; padding: 2px 10px; border-radius: 10px; font-size: 13px; }
.s-green { color: #2fbfa5; background: #e6f9ef; }
.s-blue  { color: #3f8ef7; background: #eef4ff; }
.s-orange{ color: #f2a03d; background: #fff1e0; }

/* 曲线 */
.curve-svg { width: 100%; height: auto; }
.legend { display: flex; gap: 16px; font-size: 13px; color: #556074; }
.lg-item { display: inline-flex; align-items: center; gap: 6px; }
.lg-item i { width: 22px; height: 3px; border-radius: 2px; }
</style>
