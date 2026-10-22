<template>
  <div>
    <div class="toolbar">
      <div class="filters">
        <input class="search" placeholder="搜索课程名称 / 教材版本" />
        <select class="filter"><option>全部学科</option><option>音乐</option><option>美术</option></select>
        <select class="filter"><option>全部教材</option><option>人教版</option><option>苏教版</option><option>岭南版</option><option>通用</option></select>
      </div>
      <div class="actions">
        <button class="btn-outline">导入课程</button>
        <button class="btn-primary">
          <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg>
          新建课程
        </button>
      </div>
    </div>

    <div class="course-grid">
      <div v-for="item in courses" :key="item.id" class="course-card" @click="$router.push('/questionbank/chapter')">
        <div class="course-cover" :style="{ background: item.gradient }">
          <div class="cover-icon">
            <svg v-if="item.subject === '音乐'" viewBox="0 0 24 24" width="42" height="42" fill="none" stroke="#fff" stroke-width="1.2"><path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/></svg>
            <svg v-else viewBox="0 0 24 24" width="42" height="42" fill="none" stroke="#fff" stroke-width="1.2"><path d="M12 3a9 9 0 1 0 0 18c1 0 1.8-.8 1.8-1.8 0-.5-.2-.9-.4-1.2-.3-.3-.4-.7-.4-1.1 0-1 .8-1.8 1.8-1.8h2A4.2 4.2 0 0 0 21 11c-.1-4.5-4-8-9-8Z"/></svg>
          </div>
          <span class="cover-tag">{{ item.subject }}</span>
        </div>
        <div class="course-body">
          <div class="course-name">{{ item.name }}</div>
          <div class="course-version">{{ item.version }} · {{ item.stage }}</div>
          <div class="course-meta">
            <span>{{ item.chapters }} 章节</span>
            <span class="sep">·</span>
            <span>{{ item.questions }} 试题</span>
          </div>
          <div class="course-actions" @click.stop>
            <button class="act-btn">章节管理</button>
            <button class="act-btn ghost">查看试题</button>
            <button class="act-btn ghost danger">删除</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const courses = [
  { id: 1, name: '初中音乐（人教版）', subject: '音乐', version: '人教版', stage: '初中', chapters: 36, questions: 1680, gradient: 'linear-gradient(135deg, #a06ee8, #8b7cf6)' },
  { id: 2, name: '初中音乐（苏教版）', subject: '音乐', version: '苏教版', stage: '初中', chapters: 32, questions: 1240, gradient: 'linear-gradient(135deg, #4f9cf9, #a06ee8)' },
  { id: 3, name: '初中美术（人教版）', subject: '美术', version: '人教版', stage: '初中', chapters: 30, questions: 1420, gradient: 'linear-gradient(135deg, #2fbfa5, #4f9cf9)' },
  { id: 4, name: '初中美术（岭南版）', subject: '美术', version: '岭南版', stage: '初中', chapters: 28, questions: 1202, gradient: 'linear-gradient(135deg, #2fbfa5, #f2b23e)' },
  { id: 5, name: '小学音乐（通用）', subject: '音乐', version: '通用', stage: '小学', chapters: 48, questions: 720, gradient: 'linear-gradient(135deg, #f2709c, #a06ee8)' },
  { id: 6, name: '小学美术（通用）', subject: '美术', version: '通用', stage: '小学', chapters: 42, questions: 600, gradient: 'linear-gradient(135deg, #f2b23e, #2fbfa5)' }
]
</script>

<style scoped>
.toolbar { display: flex; justify-content: space-between; align-items: center; gap: 16px; margin-bottom: 18px; flex-wrap: wrap; }
.filters { display: flex; gap: 10px; flex-wrap: wrap; }
.search { padding: 8px 12px; border: 1px solid #e0e5ef; border-radius: 6px; font-size: 13px; width: 240px; outline: none; }
.filter { padding: 8px 12px; border: 1px solid #e0e5ef; border-radius: 6px; font-size: 13px; background: #fff; }
.actions { display: flex; gap: 10px; }
.btn-outline { padding: 8px 16px; border: 1px solid #c9d6ee; border-radius: 6px; background: #fff; color: #2f6fe4; font-size: 13px; cursor: pointer; }
.btn-primary { padding: 8px 18px; border: none; border-radius: 6px; background: linear-gradient(95deg, #3f8ef7, #7b6cf0); color: #fff; font-size: 13px; cursor: pointer; display: inline-flex; align-items: center; gap: 5px; }

.course-grid {
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px;
}
@media (max-width: 1100px) { .course-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 600px) { .course-grid { grid-template-columns: 1fr; } }

.course-card {
  background: #fff; border-radius: 12px; box-shadow: 0 2px 14px rgba(70,90,130,0.06);
  overflow: hidden; cursor: pointer; transition: transform 0.2s, box-shadow 0.2s;
}
.course-card:hover { transform: translateY(-2px); box-shadow: 0 8px 22px rgba(70,90,130,0.12); }
.course-cover {
  height: 130px; display: flex; flex-direction: column; align-items: center; justify-content: center; position: relative;
}
.cover-icon { margin-bottom: 6px; }
.cover-tag { position: absolute; top: 10px; right: 10px; font-size: 11px; padding: 3px 10px; border-radius: 10px; background: rgba(255,255,255,0.9); color: #2b3445; font-weight: 600; }
.course-body { padding: 14px 16px; }
.course-name { font-size: 15px; font-weight: 700; color: #1f2a44; margin-bottom: 4px; }
.course-version { font-size: 12px; color: #8a93a5; margin-bottom: 8px; }
.course-meta { font-size: 12px; color: #6b7688; display: flex; align-items: center; gap: 6px; }
.course-meta .sep { color: #c9d1e0; }

.course-actions { display: flex; gap: 6px; margin-top: 12px; padding-top: 12px; border-top: 1px solid #f0f2f7; }
.act-btn { flex: 1; padding: 7px 0; border: none; border-radius: 6px; font-size: 12px; cursor: pointer; background: #eef4ff; color: #2f6fe4; font-weight: 500; }
.act-btn.ghost { background: transparent; color: #6b7688; border: 1px solid #e0e5ef; }
.act-btn.ghost:hover { border-color: #4f9cf9; color: #4f9cf9; }
.act-btn.ghost.danger:hover { border-color: #ef4444; color: #ef4444; }
</style>
