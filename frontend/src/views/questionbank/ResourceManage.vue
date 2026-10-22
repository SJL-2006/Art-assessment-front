<template>
  <div>
    <div class="page-header">
      <div>
        <h2>试题资源管理</h2>
        <p class="page-sub">管理试题关联的图片、音频等多媒体资源</p>
      </div>
      <button class="btn-primary">
        <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="M17 8l-5-5-5 5"/><path d="M12 3v12"/></svg>
        批量上传
      </button>
    </div>

    <div class="stat-row">
      <StatCard label="资源总数" :value="2480" accent="#4f9cf9" />
      <StatCard label="图片资源" :value="1620" accent="#2fbfa5" />
      <StatCard label="音频资源" :value="860" accent="#a06ee8" />
      <StatCard label="占用空间" :value="'3.8 GB'" accent="#f2709c" />
    </div>

    <div class="toolbar">
      <div class="filters">
        <input class="search" placeholder="搜索文件名 / 关联试题" />
        <select class="filter"><option>全部类型</option><option>图片</option><option>音频</option></select>
        <select class="filter"><option>全部学科</option><option>音乐</option><option>美术</option></select>
        <select class="filter"><option>全部状态</option><option>已关联</option><option>未关联</option></select>
      </div>
    </div>

    <div class="resource-grid">
      <div v-for="item in resources" :key="item.id" class="resource-card">
        <div class="thumb" :class="item.type === 'image' ? 'img' : 'audio'">
          <div v-if="item.type === 'image'" class="img-placeholder" :style="{ background: item.color }">
            <svg viewBox="0 0 24 24" width="36" height="36" fill="none" stroke="#fff" stroke-width="1.2"><rect x="3" y="3" width="18" height="18" rx="3"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="m21 15-5-5L5 21"/></svg>
          </div>
          <div v-else class="audio-placeholder">
            <svg viewBox="0 0 24 24" width="40" height="40" fill="none" stroke="#a06ee8" stroke-width="1.5" stroke-linecap="round"><path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/></svg>
          </div>
          <span class="tag" :class="item.type === 'image' ? 'img' : 'aud'">{{ item.type === 'image' ? '图片' : '音频' }}</span>
        </div>
        <div class="info">
          <div class="filename" :title="item.filename">{{ item.filename }}</div>
          <div class="meta">
            <span>{{ item.size }}</span>
            <span class="dot">·</span>
            <span>{{ item.subject }}</span>
          </div>
          <div class="meta link-info">
            <span v-if="item.linked" class="linked">已关联 · {{ item.questionId }}</span>
            <span v-else class="unlinked">未关联试题</span>
          </div>
        </div>
        <div class="actions">
          <button class="act-btn">预览</button>
          <button class="act-btn">下载</button>
          <button class="act-btn link">关联试题</button>
          <button class="act-btn danger">删除</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import StatCard from '../../components/StatCard.vue'

const resources = Array.from({ length: 12 }).map((_, i) => ({
  id: i + 1,
  filename: i % 2 ? `audio_${String(1001 + i)}.mp3` : `image_${String(2001 + i)}.jpg`,
  type: i % 2 ? 'audio' : 'image',
  size: i % 2 ? `${(1 + i * 0.3).toFixed(1)} MB` : `${(300 + i * 50)} KB`,
  subject: i % 2 ? '音乐' : '美术',
  color: ['#a06ee8', '#2fbfa5', '#4f9cf9', '#f2709c'][i % 4],
  linked: i % 3 !== 0,
  questionId: i % 3 !== 0 ? `Q${String(5862 - i).padStart(4, '0')}` : ''
}))
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 18px; gap: 16px; flex-wrap: wrap; }
.page-header h2 { margin: 0; font-size: 20px; font-weight: 700; color: #1f2a44; }
.page-sub { margin: 4px 0 0; font-size: 13px; color: #8a93a5; }
.btn-primary { padding: 9px 18px; border: none; border-radius: 6px; background: linear-gradient(95deg, #3f8ef7, #7b6cf0); color: #fff; font-size: 13px; cursor: pointer; display: inline-flex; align-items: center; gap: 5px; }

.stat-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 18px; }
@media (max-width: 1100px) { .stat-row { grid-template-columns: repeat(2, 1fr); } }

.toolbar { margin-bottom: 16px; }
.filters { display: flex; gap: 10px; flex-wrap: wrap; }
.search { padding: 8px 12px; border: 1px solid #e0e5ef; border-radius: 6px; font-size: 13px; width: 240px; outline: none; }
.filter { padding: 8px 12px; border: 1px solid #e0e5ef; border-radius: 6px; font-size: 13px; background: #fff; }

.resource-grid {
  display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px;
}
@media (max-width: 1200px) { .resource-grid { grid-template-columns: repeat(3, 1fr); } }
@media (max-width: 800px) { .resource-grid { grid-template-columns: repeat(2, 1fr); } }

.resource-card {
  background: #fff; border-radius: 12px; box-shadow: 0 2px 14px rgba(70,90,130,0.06);
  overflow: hidden; display: flex; flex-direction: column;
  transition: transform 0.2s, box-shadow 0.2s;
}
.resource-card:hover { transform: translateY(-2px); box-shadow: 0 8px 22px rgba(70,90,130,0.1); }

.thumb {
  position: relative; aspect-ratio: 4 / 3;
  display: flex; align-items: center; justify-content: center;
}
.thumb.img .img-placeholder { width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; }
.thumb.audio { background: linear-gradient(135deg, #f3e8ff, #eef4ff); }
.thumb .tag {
  position: absolute; top: 8px; left: 8px;
  font-size: 10px; padding: 3px 8px; border-radius: 8px; font-weight: 600;
  background: rgba(255,255,255,0.9); color: #2b3445;
}

.info { padding: 12px 14px; flex: 1; }
.filename { font-size: 13px; font-weight: 600; color: #1f2a44; margin-bottom: 4px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.meta { font-size: 11px; color: #8a93a5; display: flex; align-items: center; gap: 6px; }
.dot { color: #c9d1e0; }
.link-info { margin-top: 2px; }
.linked { color: #16a34a; font-weight: 500; }
.unlinked { color: #d97706; }

.actions {
  display: flex; gap: 4px; padding: 10px 14px; border-top: 1px solid #f0f2f7;
}
.act-btn { flex: 1; padding: 6px 0; border: none; border-radius: 5px; background: transparent; font-size: 11px; color: #4a5568; cursor: pointer; transition: all 0.15s; }
.act-btn:hover { background: #eef4ff; color: #2f6fe4; }
.act-btn.link:hover { background: #fef3e2; color: #d97706; }
.act-btn.danger:hover { background: #fdecee; color: #ef4444; }
</style>
