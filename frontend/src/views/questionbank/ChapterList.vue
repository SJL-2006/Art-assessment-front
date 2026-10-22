<template>
  <div>
    <div class="page-header">
      <div>
        <h2>章节管理</h2>
        <p class="page-sub">
          当前课程：
          <span class="course-link">{{ currentCourse.name }}</span>
          · {{ currentCourse.version }} · {{ currentCourse.stage }}
        </p>
      </div>
      <div class="actions">
        <button class="btn-outline">切换课程</button>
        <button class="btn-primary">
          <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg>
          新增章节
        </button>
      </div>
    </div>

    <div class="chapter-tree">
      <div v-for="(chapter, ci) in chapters" :key="ci" class="chapter-node">
        <div class="chapter-bar">
          <div class="chapter-num">{{ String(ci + 1).padStart(2, '0') }}</div>
          <div class="chapter-info">
            <div class="chapter-name">{{ chapter.name }}</div>
            <div class="chapter-meta">
              <span>{{ chapter.sections }} 节</span>
              <span class="sep">·</span>
              <span>{{ chapter.questions }} 题</span>
              <span class="sep">·</span>
              <span>{{ chapter.status }}</span>
            </div>
          </div>
          <button class="toggle-btn" @click="chapter.expanded = !chapter.expanded">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"
              :style="{ transform: chapter.expanded ? 'rotate(180deg)' : 'none', transition: 'transform 0.2s' }">
              <path d="m6 9 6 6 6-6"/>
            </svg>
          </button>
          <div class="chapter-actions">
            <button class="act-btn">编辑</button>
            <button class="act-btn">题目</button>
            <button class="act-btn danger">删除</button>
          </div>
        </div>
        <div v-if="chapter.expanded && chapter.children" class="children">
          <div v-for="(sec, si) in chapter.children" :key="si" class="section">
            <div class="sec-dot"></div>
            <div class="sec-name">{{ sec.name }}</div>
            <div class="sec-meta">{{ sec.questions }} 题</div>
            <div class="sec-actions">
              <button class="act-btn">编辑</button>
              <button class="act-btn danger">删除</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="add-chapter">
      <button class="add-btn">
        <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg>
        添加新章节
      </button>
    </div>
  </div>
</template>

<script setup>
const currentCourse = { name: '初中音乐（人教版）', version: '人教版', stage: '初中' }
const chapters = [
  { name: '第一单元 音乐的魅力', sections: 3, questions: 120, status: '已发布', expanded: true,
    children: [
      { name: '第1节 音乐与人类生活', questions: 45 },
      { name: '第2节 音乐的表现要素', questions: 40 },
      { name: '第3节 音乐的社会功能', questions: 35 }
    ] },
  { name: '第二单元 民族音乐花园', sections: 4, questions: 160, status: '已发布', expanded: false,
    children: [
      { name: '第1节 汉族民歌', questions: 50 },
      { name: '第2节 少数民族民歌', questions: 40 },
      { name: '第3节 民间器乐', questions: 40 },
      { name: '第4节 戏曲音乐', questions: 30 }
    ] },
  { name: '第三单元 交响音乐殿堂', sections: 3, questions: 180, status: '已发布', expanded: false,
    children: [
      { name: '第1节 交响乐的基本结构', questions: 55 },
      { name: '第2节 贝多芬与《命运交响曲》', questions: 65 },
      { name: '第3节 莫扎特与古典音乐', questions: 60 }
    ] },
  { name: '第四单元 流行音乐世界', sections: 3, questions: 140, status: '编辑中', expanded: false,
    children: [
      { name: '第1节 流行音乐的特点', questions: 40 },
      { name: '第2节 经典流行作品赏析', questions: 55 },
      { name: '第3节 流行音乐与创作', questions: 45 }
    ] },
  { name: '第五单元 中外音乐比较', sections: 2, questions: 100, status: '编辑中', expanded: false,
    children: [
      { name: '第1节 中西音乐文化差异', questions: 50 },
      { name: '第2节 世界音乐一瞥', questions: 50 }
    ] },
  { name: '第六单元 音乐创作实践', sections: 2, questions: 80, status: '未开始', expanded: false, children: [] }
]
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 18px; gap: 16px; flex-wrap: wrap; }
.page-header h2 { margin: 0; font-size: 20px; font-weight: 700; color: #1f2a44; }
.page-sub { margin: 4px 0 0; font-size: 13px; color: #8a93a5; }
.course-link { color: #2f6fe4; font-weight: 500; cursor: pointer; }
.course-link:hover { text-decoration: underline; }

.actions { display: flex; gap: 10px; }
.btn-outline { padding: 8px 16px; border: 1px solid #c9d6ee; border-radius: 6px; background: #fff; color: #2f6fe4; font-size: 13px; cursor: pointer; }
.btn-primary { padding: 8px 18px; border: none; border-radius: 6px; background: linear-gradient(95deg, #3f8ef7, #7b6cf0); color: #fff; font-size: 13px; cursor: pointer; display: inline-flex; align-items: center; gap: 5px; }

.chapter-tree { display: flex; flex-direction: column; gap: 10px; margin-bottom: 20px; }
.chapter-node { background: #fff; border-radius: 10px; box-shadow: 0 2px 12px rgba(70,90,130,0.05); overflow: hidden; }
.chapter-bar {
  display: flex; align-items: center; gap: 12px; padding: 14px 18px;
  border-left: 4px solid transparent; transition: border-color 0.2s;
}
.chapter-node:hover .chapter-bar { border-left-color: #4f9cf9; }
.chapter-num { width: 38px; height: 38px; border-radius: 10px; background: #eef4ff; color: #2f6fe4; display: flex; align-items: center; justify-content: center; font-size: 14px; font-weight: 700; flex-shrink: 0; }
.chapter-info { flex: 1; }
.chapter-name { font-size: 14px; font-weight: 600; color: #1f2a44; }
.chapter-meta { font-size: 11px; color: #8a93a5; margin-top: 3px; display: flex; align-items: center; gap: 6px; }
.chapter-meta .sep { color: #d9dfe9; }

.toggle-btn {
  width: 28px; height: 28px; border: none; background: transparent; color: #8a93a5; cursor: pointer;
  border-radius: 4px; display: flex; align-items: center; justify-content: center;
}
.toggle-btn:hover { background: #f4f6fa; color: #2b3445; }

.chapter-actions { display: flex; gap: 6px; }
.act-btn { padding: 5px 12px; border: 1px solid #e0e5ef; border-radius: 5px; background: #fff; font-size: 12px; color: #6b7688; cursor: pointer; }
.act-btn:hover { border-color: #4f9cf9; color: #4f9cf9; }
.act-btn.danger:hover { border-color: #ef4444; color: #ef4444; }

.children {
  background: #fafbfe; padding: 10px 18px 14px 70px; border-top: 1px solid #f0f2f7;
}
.section {
  display: flex; align-items: center; gap: 12px; padding: 8px 0; border-bottom: 1px dashed #eef1f6;
}
.section:last-child { border-bottom: none; }
.sec-dot { width: 6px; height: 6px; border-radius: 50%; background: #c9d6ee; }
.sec-name { flex: 1; font-size: 13px; color: #4a5568; }
.sec-meta { font-size: 11px; color: #8a93a5; margin-right: 14px; }
.sec-actions { display: flex; gap: 6px; }
.sec-actions .act-btn { padding: 4px 10px; font-size: 11px; }

.add-chapter { padding: 10px 0; }
.add-btn {
  width: 100%; padding: 14px; border: 2px dashed #c9d6ee; border-radius: 10px;
  background: transparent; font-size: 13px; color: #8a93a5; cursor: pointer;
  display: flex; align-items: center; justify-content: center; gap: 6px;
  transition: all 0.15s;
}
.add-btn:hover { border-color: #4f9cf9; color: #4f9cf9; background: #fafbfe; }
</style>
