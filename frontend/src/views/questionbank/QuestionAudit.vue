<template>
  <div>
    <div class="page-header">
      <div>
        <h2>试题审核</h2>
        <p class="page-sub">教师提交的试题需经管理员审核后才能入库</p>
      </div>
      <div class="page-stats">
        <span class="chip warn">待审核 {{ pendingCount }}</span>
        <span class="chip ok">今日已通过 {{ passedToday }}</span>
        <span class="chip no">今日驳回 {{ rejectedToday }}</span>
      </div>
    </div>

    <div class="tabs">
      <button class="tab active">全部待审核（{{ pendingCount }}）</button>
      <button class="tab">我审核的通过</button>
      <button class="tab">我审核的驳回</button>
    </div>

    <div class="audit-list">
      <div v-for="item in pending" :key="item.id" class="audit-card">
        <div class="audit-head">
          <span class="subject" :style="{ background: item.subject === '音乐' ? '#f3e8ff' : '#e6f8ed', color: item.subject === '音乐' ? '#a06ee8' : '#2fbfa5' }">{{ item.subject }}</span>
          <span class="type">{{ item.type }}</span>
          <span class="diff" :class="'d-' + item.difficulty">{{ item.difficulty }}</span>
          <span class="grade">{{ item.grade }}</span>
          <span class="chapter">· {{ item.chapter }}</span>
          <span class="creator">提交人：{{ item.creator }}（{{ item.school }}）</span>
          <span class="time">{{ item.submitTime }}</span>
        </div>
        <div class="audit-content">
          <div class="label">题干</div>
          <div class="content-text">{{ item.question }}</div>
          <div v-if="item.options" class="options">
            <div v-for="(opt, i) in item.options" :key="i" :class="{ correct: opt.correct }">
              {{ String.fromCharCode(65 + i) }}. {{ opt.text }}<span v-if="opt.correct" class="opt-tag">正确答案</span>
            </div>
          </div>
          <div class="label">参考答案</div>
          <div class="content-text">{{ item.answer }}</div>
          <div v-if="item.hasAudio || item.hasImage" class="resources">
            <span v-if="item.hasAudio" class="res-tag audio">🎵 音频资源</span>
            <span v-if="item.hasImage" class="res-tag image">🖼 图片资源</span>
          </div>
        </div>
        <div class="audit-reject" v-if="item.rejectReason">
          <div class="label">上一次驳回原因</div>
          <div class="content-text reject-reason">{{ item.rejectReason }}</div>
        </div>
        <div class="audit-actions">
          <button class="act-btn" @click="approve(item)">✓ 通过</button>
          <button class="act-btn reject">✕ 驳回</button>
          <button class="act-btn ghost">预览完整版</button>
          <button class="act-btn ghost">转修改</button>
        </div>
      </div>
      <div v-if="pending.length === 0" class="empty">暂无待审核试题</div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const approve = ref((item) => {})
const pendingCount = ref(186)
const passedToday = ref(42)
const rejectedToday = ref(3)

const pending = [
  { id: 5856, subject: '音乐', type: '判断题', difficulty: '易', grade: '七年级', chapter: '第一单元·记谱法', creator: '张老师', school: '成都第一中学', submitTime: '2026-10-22 09:30', question: '五线谱中，高音谱号也叫 G 谱号，中谱号叫 C 谱号。', answer: '正确', hasAudio: false, hasImage: false },
  { id: 5854, subject: '美术', type: '选择题', difficulty: '中', grade: '八年级', chapter: '第三单元·色彩知识', creator: '李老师', school: '绵阳实验中学', submitTime: '2026-10-22 09:12', question: '以下关于三原色的描述，正确的是？', options: [
    { text: '红、黄、蓝是色彩三原色', correct: true },
    { text: '红、绿、蓝是色彩三原色', correct: false },
    { text: '黄、绿、紫是色彩三原色', correct: false },
    { text: '橙、绿、紫是色彩三原色', correct: false }
  ], answer: 'A', hasAudio: false, hasImage: true },
  { id: 5853, subject: '音乐', type: '选择题', difficulty: '易', grade: '七年级', chapter: '第一单元·乐器家族', creator: '王老师', school: '德阳外国语学校', submitTime: '2026-10-21 16:45', question: '以下哪件乐器属于吹奏乐器？', options: [
    { text: '小提琴', correct: false },
    { text: '长笛', correct: true },
    { text: '钢琴', correct: false },
    { text: '架子鼓', correct: false }
  ], answer: 'B', hasAudio: true, hasImage: false },
  { id: 5850, subject: '美术', type: '填空题', difficulty: '中', grade: '九年级', chapter: '第五单元·现代艺术', creator: '陈老师', school: '乐山第一中学', submitTime: '2026-10-21 14:20', question: '立体主义的代表画家是毕加索和______。', answer: '布拉克', hasAudio: false, hasImage: false },
  { id: 5847, subject: '音乐', type: '简答题', difficulty: '难', grade: '九年级', chapter: '第五单元·中外音乐比较', creator: '赵老师', school: '宜宾第二中学', submitTime: '2026-10-21 11:08', question: '请谈谈你对"音乐教育不是培养音乐家，而是培养人"这句话的理解。', answer: '开放题，评分要点：音乐教育的美育价值、人格塑造、情感表达、文化理解等方面', hasAudio: false, hasImage: false, rejectReason: '答案要点不够具体，请补充评分细则（至少3个采分点）' }
]
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 16px; gap: 16px; flex-wrap: wrap; }
.page-header h2 { margin: 0; font-size: 20px; font-weight: 700; color: #1f2a44; }
.page-sub { margin: 4px 0 0; font-size: 13px; color: #8a93a5; }
.page-stats { display: flex; gap: 8px; }
.chip { padding: 6px 14px; border-radius: 14px; font-size: 12px; font-weight: 600; }
.chip.warn { background: #fef3e2; color: #d97706; }
.chip.ok { background: #e6f8ed; color: #16a34a; }
.chip.no { background: #fdecee; color: #ef4444; }

.tabs { display: flex; gap: 4px; background: #fff; border-radius: 8px; padding: 4px; box-shadow: 0 2px 10px rgba(70,90,130,0.06); margin-bottom: 16px; }
.tab { padding: 6px 18px; border: none; background: transparent; border-radius: 6px; font-size: 13px; color: #6b7688; cursor: pointer; }
.tab:hover { color: #2f6fe4; }
.tab.active { background: #2f6fe4; color: #fff; }

.audit-list { display: flex; flex-direction: column; gap: 14px; }
.audit-card { background: #fff; border-radius: 12px; box-shadow: 0 2px 14px rgba(70,90,130,0.06); padding: 18px 20px; }
.audit-head { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; margin-bottom: 14px; }
.subject { font-size: 11px; padding: 3px 10px; border-radius: 10px; font-weight: 600; }
.type, .grade { font-size: 12px; padding: 3px 9px; border-radius: 10px; background: #f0f2f7; color: #6b7688; }
.diff { font-size: 11px; padding: 2px 9px; border-radius: 10px; font-weight: 600; }
.diff.d-易 { background: #e6f8ed; color: #16a34a; }
.diff.d-中 { background: #fef3e2; color: #d97706; }
.diff.d-难 { background: #fdecee; color: #ef4444; }
.chapter { font-size: 12px; color: #6b7688; }
.creator { margin-left: auto; font-size: 12px; color: #8a93a5; }
.time { font-size: 11px; color: #c9d1e0; }

.audit-content { border-top: 1px solid #f0f2f7; padding-top: 12px; }
.label { font-size: 11px; color: #8a93a5; margin-bottom: 6px; letter-spacing: 1px; }
.content-text { font-size: 13px; color: #2b3445; line-height: 1.7; padding: 10px 12px; background: #fafbfe; border-radius: 8px; margin-bottom: 12px; white-space: pre-wrap; }

.options { display: flex; flex-direction: column; gap: 6px; margin-bottom: 12px; padding: 12px; background: #fafbfe; border-radius: 8px; }
.options div { font-size: 13px; color: #4a5568; display: flex; align-items: center; gap: 8px; }
.options div.correct { color: #16a34a; font-weight: 600; }
.opt-tag { margin-left: auto; font-size: 10px; padding: 2px 6px; border-radius: 4px; background: #16a34a; color: #fff; }

.resources { display: flex; gap: 8px; margin-bottom: 8px; }
.res-tag { font-size: 11px; padding: 4px 10px; border-radius: 6px; background: #f0f2f7; color: #6b7688; }
.res-tag.audio { background: #eef4ff; color: #2f6fe4; }
.res-tag.image { background: #e6f8ed; color: #16a34a; }

.audit-reject { border-top: 1px dashed #eef1f6; padding-top: 12px; margin-bottom: 12px; }
.reject-reason { color: #ef4444; background: #fef7f7; }

.audit-actions { display: flex; gap: 10px; padding-top: 14px; border-top: 1px solid #f0f2f7; }
.act-btn { padding: 7px 18px; border: none; border-radius: 6px; font-size: 13px; cursor: pointer; font-weight: 500; background: #16a34a; color: #fff; }
.act-btn.reject { background: #ef4444; }
.act-btn.ghost { background: transparent; color: #6b7688; border: 1px solid #e0e5ef; }
.act-btn.ghost:hover { border-color: #4f9cf9; color: #4f9cf9; }

.empty { text-align: center; padding: 60px 0; color: #8a93a5; font-size: 13px; }
</style>
