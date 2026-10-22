<!-- 教师端工作台：欢迎语 + 统计卡 + 班级 + 最近发布 + 待审核 -->
<template>
  <div class="page">
    <!-- 欢迎区 -->
    <section class="welcome card">
      <div class="welcome-text">
        <h2>王美丽老师，你好 👩‍🏫</h2>
        <p>{{ data.school || '' }} · 今天是管理班级、批改作业的高效一天！</p>
      </div>
      <button class="btn-gradient">
        <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg>
        发布测评
      </button>
    </section>

    <!-- 统计卡 -->
    <section class="stats">
      <div v-for="s in statCards" :key="s.label" class="stat card">
        <div class="stat-icon" :style="{ background: s.bg, color: s.color }">{{ s.icon }}</div>
        <div class="stat-body">
          <div class="stat-val">{{ s.value }}</div>
          <div class="stat-label">{{ s.label }}</div>
        </div>
      </div>
    </section>

    <!-- 主区 -->
    <section class="main-grid">
      <!-- 我的班级 -->
      <div class="card">
        <div class="card-head">
          <h3 class="title-splash">我的班级</h3>
          <router-link to="/teacher/class" class="link">管理班级 →</router-link>
        </div>
        <ul class="classes">
          <li v-for="c in myClasses" :key="c.id" class="cls">
            <div class="cls-code">{{ c.id }}</div>
            <div class="cls-body">
              <div class="cls-name">{{ c.name }}</div>
              <div class="cls-meta">{{ c.studentCount }} 人 · 班主任 {{ c.teacher }}</div>
            </div>
            <span class="cls-tag">运行中</span>
          </li>
          <li v-if="!myClasses.length" class="empty">暂无班级</li>
        </ul>
      </div>

      <!-- 最近发布的测评 -->
      <div class="card">
        <div class="card-head">
          <h3 class="title-splash">最近发布的测评</h3>
          <router-link to="/teacher/papers" class="link">试卷列表 →</router-link>
        </div>
        <table class="papers">
          <thead><tr><th>名称</th><th>学科</th><th>状态</th><th>参与</th></tr></thead>
          <tbody>
            <tr v-for="p in recentPapers" :key="p.id">
              <td>{{ p.title }}</td>
              <td>{{ p.subject === 'music' ? '🎵 音乐' : '🎨 美术' }}</td>
              <td><span class="status" :class="p.status">{{ p.statusText }}</span></td>
              <td>{{ p.participated }}/{{ p.total }}</td>
            </tr>
            <tr v-if="!recentPapers.length"><td colspan="4" class="empty">暂无数据</td></tr>
          </tbody>
        </table>
      </div>

      <!-- 待审核队列 -->
      <div class="card audit">
        <div class="card-head">
          <h3 class="title-splash">待审核队列</h3>
          <span class="count">{{ auditQueue.length }}</span>
        </div>
        <ul class="audits">
          <li v-for="a in auditQueue" :key="a.id" class="aud">
            <div class="aud-avatar">{{ a.name.charAt(0) }}</div>
            <div class="aud-body">
              <div class="aud-name">{{ a.name }}</div>
              <div class="aud-reason">{{ a.reason }}</div>
            </div>
            <div class="aud-actions">
              <button class="mini ok">通过</button>
              <button class="mini no">拒绝</button>
            </div>
          </li>
          <li v-if="!auditQueue.length" class="empty">全部审核完成 🎉</li>
        </ul>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive } from 'vue'
import { api } from '../../api'

const data = reactive({
  name: '王美丽', school: '阳光小学',
  stats: { classes: 5, students: 218, papers: 16, pending: 3 },
  myClasses: [], recentPapers: [], auditQueue: []
})

onMounted(async () => {
  try {
    const res = await api.teacher.workspace()
    Object.assign(data, res)
  } catch {
    Object.assign(data, {
      myClasses: [
        { id: 'C001', name: '五(1)班', studentCount: 45, teacher: '张丽' },
        { id: 'C002', name: '五(2)班', studentCount: 42, teacher: '李明' },
        { id: 'C003', name: '六(1)班', studentCount: 48, teacher: '王美丽' },
        { id: 'C004', name: '六(3)班', studentCount: 41, teacher: '赵强' },
      ],
      recentPapers: [
        { id: 1, title: '五年级音乐期中测评', subject: 'music', status: 'ongoing', statusText: '进行中', participated: 32, total: 45 },
        { id: 2, title: '六年级美术单元测评', subject: 'art', status: 'done', statusText: '已结束', participated: 41, total: 41 },
        { id: 3, title: '音乐练习：节奏感知', subject: 'music', status: 'draft', statusText: '草稿', participated: 0, total: 0 },
      ],
      auditQueue: [
        { id: 1, name: '张小华', reason: '申请更换到五(2)班' },
        { id: 2, name: '王小明', reason: '申请延长测评时间' },
      ]
    })
  }
})

const statCards = computed(() => [
  { label: '管理班级', icon: '🏫', value: data.stats.classes ?? 0, bg: '#eef4ff', color: '#3f8ef7' },
  { label: '学生人数', icon: '👥', value: data.stats.students ?? 0, bg: '#f4effe', color: '#7b6cf0' },
  { label: '已发布测评', icon: '📄', value: data.stats.papers ?? 0, bg: '#fff1e0', color: '#f2a03d' },
  { label: '待批改材料', icon: '✏️', value: data.stats.pending ?? 0, bg: '#ffe4e0', color: '#f2709c' },
])

const myClasses   = computed(() => data.myClasses || [])
const recentPapers = computed(() => data.recentPapers || [])
const auditQueue  = computed(() => data.auditQueue || [])
</script>

<style scoped>
.page { display: flex; flex-direction: column; gap: 22px; }

/* 欢迎区 */
.welcome {
  display: flex; align-items: center; justify-content: space-between;
  padding: 28px 32px;
  background: linear-gradient(100deg, rgba(123, 108, 240, 0.08), rgba(63, 142, 247, 0.08));
}
.welcome-text h2 { margin: 0 0 6px; font-size: 22px; color: #2b3445; }
.welcome-text p { margin: 0; font-size: 14px; color: #6b7688; }
.welcome .btn-gradient { padding: 11px 22px; }

/* 统计 */
.stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 18px; }
.stat { display: flex; align-items: center; gap: 14px; }
.stat-icon {
  width: 48px; height: 48px;
  border-radius: 12px; font-size: 22px;
  display: flex; align-items: center; justify-content: center;
}
.stat-val { font-size: 26px; font-weight: 700; color: #2b3445; }
.stat-label { font-size: 13px; color: #8a93a5; margin-top: 2px; }

/* 主区 */
.main-grid {
  display: grid;
  grid-template-columns: 1fr 1.1fr 1fr;
  gap: 22px;
  align-items: start;
}
.card-head { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; }
.card-head .count { font-size: 12px; color: #8a93a5; }
.link { font-size: 13px; color: #3f8ef7; }
.empty { text-align: center; color: #8a93a5; padding: 20px; font-size: 13px; list-style: none; }

/* 班级 */
.classes { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 10px; }
.cls {
  display: flex; align-items: center; gap: 12px;
  padding: 12px 14px;
  background: #fafbff;
  border-radius: 10px;
}
.cls-code {
  width: 42px; height: 42px;
  background: linear-gradient(135deg, #3f8ef7, #7b6cf0);
  color: #fff; font-size: 12px; font-weight: 600;
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
}
.cls-body { flex: 1; min-width: 0; }
.cls-name { font-size: 14px; font-weight: 600; color: #2b3445; }
.cls-meta { font-size: 12px; color: #8a93a5; margin-top: 2px; }
.cls-tag { font-size: 11px; color: #2fbfa5; background: #e6f9ef; padding: 3px 10px; border-radius: 10px; }

/* 试卷表 */
.papers { width: 100%; border-collapse: collapse; font-size: 14px; }
.papers th, .papers td { padding: 12px 8px; text-align: left; border-bottom: 1px solid #eef1f6; }
.papers th { font-size: 12px; color: #8a93a5; font-weight: 500; }
.status { font-size: 12px; padding: 2px 10px; border-radius: 10px; }
.status.ongoing { color: #3f8ef7; background: #eef4ff; }
.status.done    { color: #2fbfa5; background: #e6f9ef; }
.status.draft   { color: #8a93a5; background: #f0f2f7; }

/* 审核 */
.audits { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 10px; }
.aud {
  display: flex; align-items: center; gap: 10px;
  padding: 12px 12px;
  background: linear-gradient(135deg, #fff8f0, #fff);
  border-radius: 10px;
  border: 1px solid #fde6cf;
}
.aud-avatar {
  width: 36px; height: 36px; border-radius: 50%;
  background: linear-gradient(135deg, #f2a03d, #f2709c);
  color: #fff; font-size: 14px; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
}
.aud-body { flex: 1; min-width: 0; }
.aud-name { font-size: 14px; font-weight: 600; color: #2b3445; }
.aud-reason { font-size: 12px; color: #8a93a5; margin-top: 2px; }
.aud-actions { display: flex; gap: 6px; }
.mini {
  padding: 4px 10px;
  font-size: 12px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-family: inherit;
}
.mini.ok { background: linear-gradient(135deg, #3f8ef7, #7b6cf0); color: #fff; }
.mini.no { background: #fff; color: #8a93a5; border: 1px solid #dfe4ee; }
</style>
