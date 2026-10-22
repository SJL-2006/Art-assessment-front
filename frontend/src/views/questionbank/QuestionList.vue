<template>
  <div>
    <div class="toolbar">
      <div class="filters">
        <input class="search" placeholder="搜索题干 / 关键词" />
        <select class="filter"><option>全部学科</option><option>音乐</option><option>美术</option></select>
        <select class="filter"><option>全部题型</option><option>选择题</option><option>判断题</option><option>填空题</option><option>简答题</option></select>
        <select class="filter"><option>全部难度</option><option>易</option><option>中</option><option>难</option></select>
        <select class="filter"><option>全部年级</option><option>七年级</option><option>八年级</option><option>九年级</option></select>
        <select class="filter"><option>全部状态</option><option>已审核</option><option>待审核</option></select>
      </div>
      <div class="actions">
        <button class="btn-outline">批量导出</button>
        <button class="btn-primary">
          <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg>
          新建试题
        </button>
      </div>
    </div>

    <CommonTable :columns="columns" :data="list" :showOp="true" :paged="true" :pageSize="12" :searchable="false">
      <template #subject="{ row }">
        <span class="subject-tag" :style="{ background: row.subject === '音乐' ? '#f3e8ff' : '#e6f8ed', color: row.subject === '音乐' ? '#a06ee8' : '#2fbfa5' }">{{ row.subject }}</span>
      </template>
      <template #difficulty="{ row }">
        <span class="diff" :class="'d-' + row.difficulty">{{ {易:'易',中:'中',难:'难'}[row.difficulty] }}</span>
      </template>
      <template #status="{ row }">
        <span class="tag" :class="row.auditStatus === '通过' ? 'success' : row.auditStatus === '待审核' ? 'warning' : 'danger'">{{ row.auditStatus }}</span>
      </template>
      <template #op="{ row }">
        <button class="op-link">预览</button>
        <button class="op-link">编辑</button>
        <button class="op-link">解析</button>
        <button class="op-link">资源</button>
        <button class="op-link danger">删除</button>
      </template>
    </CommonTable>

    <!-- 新建/编辑弹层 -->
    <div v-if="showEditor" class="modal-overlay" @click.self="showEditor = false">
      <div class="modal big">
        <div class="modal-head">
          <h3>{{ editing ? '编辑试题' : '新建试题' }}</h3>
          <button class="close" @click="showEditor = false">×</button>
        </div>
        <div class="modal-body">
          <div class="form-grid">
            <div class="form-item"><label>学科 *</label><select><option>音乐</option><option>美术</option></select></div>
            <div class="form-item"><label>题型 *</label><select><option>选择题</option><option>判断题</option><option>填空题</option><option>简答题</option><option>创作题</option></select></div>
            <div class="form-item"><label>难度 *</label><select><option>易</option><option>中</option><option>难</option></select></div>
            <div class="form-item"><label>年级 *</label><select><option>七年级</option><option>八年级</option><option>九年级</option></select></div>
            <div class="form-item"><label>所属课程 *</label><select><option>初中音乐（人教版）</option><option>初中音乐（苏教版）</option></select></div>
            <div class="form-item"><label>所属章节 *</label><select><option>第一单元 音乐的魅力</option><option>第二单元 民族音乐</option></select></div>
            <div class="form-item"><label>分值 *</label><input type="number" value="2" /></div>
            <div class="form-item"><label>时长（秒）</label><input type="number" value="0" placeholder="仅音视频题填" /></div>
          </div>
          <div class="form-block">
            <label>题干 *</label>
            <textarea rows="4" placeholder="请输入试题题干..."></textarea>
          </div>
          <div class="form-block">
            <label>选项（选择题用，A/B/C/D 每行一条，正确项前打√）</label>
            <div class="option-list">
              <div class="option-row"><input type="checkbox" /> <span>A</span> <input value="选项 A 内容" /></div>
              <div class="option-row"><input type="checkbox" /> <span>B</span> <input value="选项 B 内容" /></div>
              <div class="option-row"><input type="checkbox" checked /> <span>C</span> <input value="选项 C 内容（正确项）" /></div>
              <div class="option-row"><input type="checkbox" /> <span>D</span> <input value="选项 D 内容" /></div>
            </div>
          </div>
          <div class="form-block">
            <label>答案 *</label>
            <textarea rows="2" placeholder="请输入参考答案...">C</textarea>
          </div>
          <div class="form-block">
            <label>解析</label>
            <textarea rows="3" placeholder="请输入试题解析..."></textarea>
          </div>
          <div class="form-block">
            <label>关联资源（图片/音频）</label>
            <div class="upload-zone">
              <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#4f9cf9" stroke-width="1.8"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="M17 8l-5-5-5 5"/><path d="M12 3v12"/></svg>
              <span>点击或拖拽上传图片 / 音频文件</span>
              <small>支持 png/jpg/mp3/wav，单个 ≤ 10MB</small>
            </div>
          </div>
        </div>
        <div class="modal-foot">
          <button class="btn-outline" @click="showEditor = false">取消</button>
          <button class="btn-outline">暂存（待审核）</button>
          <button class="btn-primary" @click="showEditor = false">保存并提交审核</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import CommonTable from '../../components/CommonTable.vue'

const showEditor = ref(false)
const editing = ref(false)

const columns = [
  { key: 'id', label: '编号', width: 90 },
  { key: 'subject', label: '学科', width: 80, slot: 'subject' },
  { key: 'type', label: '题型', width: 90 },
  { key: 'question', label: '题干', width: 260 },
  { key: 'difficulty', label: '难度', width: 80, slot: 'difficulty' },
  { key: 'grade', label: '年级', width: 80 },
  { key: 'score', label: '分值', width: 70, align: 'center' },
  { key: 'chapter', label: '章节' },
  { key: 'creator', label: '创建人' },
  { key: 'useCount', label: '使用次数', width: 90, align: 'center' },
  { key: 'auditStatus', label: '审核状态', width: 90, slot: 'status' }
]
const list = [
  { id: 'Q5862', subject: '音乐', type: '选择题', question: '以下哪件乐器属于打击乐器？A.小提琴 B.钢琴 C.架子鼓 D.长笛', difficulty: '易', grade: '七年级', score: 2, chapter: '第一单元·乐器家族', creator: '张老师', useCount: 36, auditStatus: '通过' },
  { id: 'Q5861', subject: '美术', type: '判断题', question: '中国画中的"四君子"指的是梅、兰、竹、菊。', difficulty: '易', grade: '八年级', score: 2, chapter: '第二单元·中国画欣赏', creator: '李老师', useCount: 28, auditStatus: '通过' },
  { id: 'Q5860', subject: '音乐', type: '选择题', question: '贝多芬的《命运交响曲》是第几交响曲？A.第三 B.第五 C.第六 D.第九', difficulty: '中', grade: '九年级', score: 3, chapter: '第三单元·交响音乐', creator: '王老师', useCount: 42, auditStatus: '通过' },
  { id: 'Q5859', subject: '美术', type: '填空题', question: '文艺复兴时期最著名的艺术家之一______创作了《蒙娜丽莎》。', difficulty: '易', grade: '七年级', score: 3, chapter: '第一单元·西方绘画', creator: '陈老师', useCount: 20, auditStatus: '通过' },
  { id: 'Q5858', subject: '音乐', type: '简答题', question: '请简述中国传统音乐与西方古典音乐在节奏上的主要差异。', difficulty: '难', grade: '九年级', score: 10, chapter: '第五单元·中外音乐比较', creator: '赵老师', useCount: 8, auditStatus: '通过' },
  { id: 'Q5857', subject: '美术', type: '创作题', question: '请以"春天"为主题，创作一幅水彩画，要求构图均衡、色彩和谐。', difficulty: '难', grade: '八年级', score: 15, chapter: '第四单元·水彩画创作', creator: '孙老师', useCount: 12, auditStatus: '通过' },
  { id: 'Q5856', subject: '音乐', type: '判断题', question: '五线谱中，高音谱号也叫 G 谱号。', difficulty: '易', grade: '七年级', score: 2, chapter: '第一单元·记谱法', creator: '张老师', useCount: 32, auditStatus: '待审核' },
  { id: 'Q5855', subject: '美术', type: '选择题', question: '以下哪种色彩搭配属于互补色？A.红与橙 B.蓝与橙 C.黄与绿 D.蓝与紫', difficulty: '中', grade: '七年级', score: 2, chapter: '第二单元·色彩知识', creator: '李老师', useCount: 18, auditStatus: '待审核' }
]
</script>

<style scoped>
.toolbar { display: flex; justify-content: space-between; align-items: center; gap: 16px; margin-bottom: 16px; flex-wrap: wrap; }
.filters { display: flex; gap: 8px; flex-wrap: wrap; }
.search { padding: 8px 12px; border: 1px solid #e0e5ef; border-radius: 6px; font-size: 13px; width: 220px; outline: none; }
.filter { padding: 8px 12px; border: 1px solid #e0e5ef; border-radius: 6px; font-size: 13px; background: #fff; }
.actions { display: flex; gap: 10px; }
.btn-outline { padding: 8px 16px; border: 1px solid #c9d6ee; border-radius: 6px; background: #fff; color: #2f6fe4; font-size: 13px; cursor: pointer; }
.btn-primary { padding: 8px 18px; border: none; border-radius: 6px; background: linear-gradient(95deg, #3f8ef7, #7b6cf0); color: #fff; font-size: 13px; cursor: pointer; display: inline-flex; align-items: center; gap: 5px; }

.subject-tag { font-size: 11px; padding: 3px 9px; border-radius: 10px; font-weight: 600; }
.diff { font-size: 11px; padding: 2px 9px; border-radius: 10px; font-weight: 600; }
.diff.d-易 { background: #e6f8ed; color: #16a34a; }
.diff.d-中 { background: #fef3e2; color: #d97706; }
.diff.d-难 { background: #fdecee; color: #ef4444; }

.op-link { background: none; border: none; cursor: pointer; color: #2f6fe4; font-size: 12px; padding: 2px 5px; }
.op-link.danger { color: #ef4444; }

/* 弹层 */
.modal-overlay { position: fixed; inset: 0; background: rgba(20,28,50,0.45); display: flex; align-items: center; justify-content: center; z-index: 100; }
.modal { background: #fff; border-radius: 14px; width: 680px; max-width: 95vw; max-height: 90vh; overflow: hidden; display: flex; flex-direction: column; box-shadow: 0 20px 60px rgba(20,28,50,0.2); }
.modal.big { width: 780px; }
.modal-head { display: flex; justify-content: space-between; align-items: center; padding: 18px 22px; border-bottom: 1px solid #f0f2f7; }
.modal-head h3 { margin: 0; font-size: 16px; font-weight: 600; color: #1f2a44; }
.close { border: none; background: none; font-size: 22px; color: #8a93a5; cursor: pointer; width: 28px; height: 28px; border-radius: 4px; }
.close:hover { background: #f4f6fa; color: #2b3445; }
.modal-body { padding: 22px; overflow-y: auto; flex: 1; }
.modal-foot { display: flex; justify-content: flex-end; gap: 10px; padding: 16px 22px; border-top: 1px solid #f0f2f7; }

.form-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 14px 16px; margin-bottom: 14px; }
.form-item label, .form-block label { display: block; font-size: 12px; color: #6b7688; margin-bottom: 6px; font-weight: 500; }
.form-item input, .form-item select, .form-block textarea, .option-row input[type="text"] {
  width: 100%; padding: 8px 12px; border: 1px solid #e0e5ef; border-radius: 6px;
  font-size: 13px; outline: none; box-sizing: border-box; background: #fff;
}
.form-block { margin-bottom: 14px; }
.form-block textarea { resize: vertical; font-family: inherit; }

.option-list { display: flex; flex-direction: column; gap: 8px; }
.option-row { display: flex; align-items: center; gap: 8px; }
.option-row span { width: 18px; font-size: 13px; font-weight: 600; color: #4a5568; }
.option-row input[type="text"] { flex: 1; padding: 7px 10px; border: 1px solid #e0e5ef; border-radius: 6px; font-size: 13px; outline: none; }

.upload-zone {
  border: 2px dashed #c9d6ee; border-radius: 10px; padding: 24px;
  text-align: center; display: flex; flex-direction: column; align-items: center; gap: 6px;
  color: #6b7688; cursor: pointer; transition: border-color 0.15s;
}
.upload-zone:hover { border-color: #4f9cf9; color: #4f9cf9; }
.upload-zone span { font-size: 13px; }
.upload-zone small { font-size: 11px; color: #a8b0c0; }
</style>
