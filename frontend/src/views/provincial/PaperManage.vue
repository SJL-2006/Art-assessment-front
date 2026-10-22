<template>
  <div>
    <div class="toolbar">
      <div class="tabs">
        <button class="tab active">全部试卷</button>
        <button class="tab">暂存</button>
        <button class="tab">已发布</button>
        <button class="tab">已结束</button>
      </div>
      <button class="btn-primary" @click="showCreate = true">
        <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
          <path d="M12 5v14M5 12h14"/>
        </svg>
        新建省级试卷
      </button>
    </div>

    <CommonTable
      :columns="columns"
      :data="papers"
      :showOp="true"
      :searchable="true"
      :showAdd="false"
      :filterable="true"
      :filterOptions="statusFilters"
      searchPlaceholder="搜索试卷名称..."
      @add="() => {}"
    >
      <template #default>
        <div class="toolbar-left">
          <input class="search-input" placeholder="搜索试卷名称..." />
          <select class="filter-select">
            <option>全部状态</option>
            <option>暂存</option><option>已发布</option><option>已结束</option>
          </select>
          <select class="filter-select">
            <option>全部学科</option>
            <option>音乐</option><option>美术</option>
          </select>
        </div>
      </template>
      <template #op="{ row }">
        <button class="op-link">查看</button>
        <button class="op-link">编辑</button>
        <button class="op-link">试题预览</button>
        <button v-if="row.status === '暂存'" class="op-link" style="color:#16a34a">发布</button>
        <button v-if="row.status === '已发布'" class="op-link danger">撤回</button>
        <button class="op-link danger">删除</button>
      </template>
    </CommonTable>

    <!-- 新建弹层 -->
    <div v-if="showCreate" class="modal-overlay" @click.self="showCreate = false">
      <div class="modal">
        <div class="modal-head">
          <h3>新建省级测评试卷</h3>
          <button class="close" @click="showCreate = false">×</button>
        </div>
        <div class="modal-body">
          <div class="form-grid">
            <div class="form-item">
              <label>试卷名称 *</label>
              <input value="2026秋季省级音乐统一测评（七年级）" />
            </div>
            <div class="form-item">
              <label>学科 *</label>
              <select><option>音乐</option><option>美术</option></select>
            </div>
            <div class="form-item">
              <label>适用年级 *</label>
              <select><option>七年级</option><option>八年级</option><option>九年级</option></select>
            </div>
            <div class="form-item">
              <label>组卷方式</label>
              <select><option>自动组卷</option><option>手动组卷</option></select>
            </div>
            <div class="form-item">
              <label>总题数</label>
              <input value="50" type="number" />
            </div>
            <div class="form-item">
              <label>考试时长（分钟）</label>
              <input value="60" type="number" />
            </div>
          </div>
          <div class="form-section">
            <div class="section-title">题目构成预览</div>
            <table class="mini-table">
              <thead><tr><th>题型</th><th>数量</th><th>每题分值</th><th>难度</th><th>小计分</th></tr></thead>
              <tbody>
                <tr><td>选择题（听音识器）</td><td>15</td><td>2</td><td>易-中</td><td>30</td></tr>
                <tr><td>判断题</td><td>10</td><td>2</td><td>易</td><td>20</td></tr>
                <tr><td>听音填空</td><td>10</td><td>3</td><td>中</td><td>30</td></tr>
                <tr><td>简答/创作题</td><td>2</td><td>10</td><td>难</td><td>20</td></tr>
                <tr><td colspan="4" style="text-align:right;font-weight:600">合计：</td><td>100</td></tr>
              </tbody>
            </table>
          </div>
        </div>
        <div class="modal-foot">
          <button class="btn-outline" @click="showCreate = false">取消</button>
          <button class="btn-outline">暂存</button>
          <button class="btn-primary" @click="showCreate = false">下一步：选题</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import CommonTable from '../../components/CommonTable.vue'

const showCreate = ref(false)
const columns = [
  { key: 'id', label: '编号', width: 100 },
  { key: 'name', label: '试卷名称' },
  { key: 'subject', label: '学科' },
  { key: 'grade', label: '年级' },
  { key: 'questionCount', label: '题数', align: 'center' },
  { key: 'duration', label: '时长(分钟)', align: 'center' },
  { key: 'scope', label: '覆盖范围' },
  { key: 'creator', label: '创建人' },
  { key: 'createTime', label: '创建时间' },
  { key: 'status', label: '状态', width: 100, slot: 'status' }
]
const papers = [
  { id: 'S20261001', name: '2026秋季省级音乐统一测评（七年级）', subject: '音乐', grade: '七年级', questionCount: 50, duration: 60, scope: '14 市州 · 328 所学校', creator: '省管理员', createTime: '2026-10-01', status: { type: 'run', label: '已发布' } },
  { id: 'S20261002', name: '2026秋季省级音乐统一测评（八年级）', subject: '音乐', grade: '八年级', questionCount: 55, duration: 70, scope: '14 市州', creator: '省管理员', createTime: '2026-10-02', status: { type: 'run', label: '已发布' } },
  { id: 'S20261003', name: '2026秋季省级美术统一测评（七年级）', subject: '美术', grade: '七年级', questionCount: 45, duration: 90, scope: '14 市州 · 321 所学校', creator: '省管理员', createTime: '2026-10-03', status: { type: 'run', label: '已发布' } },
  { id: 'S20261004', name: '2026秋季省级美术统一测评（九年级）', subject: '美术', grade: '九年级', questionCount: 50, duration: 100, scope: '14 市州', creator: '省管理员', createTime: '2026-10-05', status: { type: 'warning', label: '暂存' } },
  { id: 'S20260401', name: '2026春季省级音乐测评（九年级）', subject: '音乐', grade: '九年级', questionCount: 52, duration: 70, scope: '14 市州 · 315 所学校', creator: '省管理员', createTime: '2026-04-01', status: { type: 'success', label: '已结束' } },
  { id: 'S20260402', name: '2026春季省级美术测评（八年级）', subject: '美术', grade: '八年级', questionCount: 48, duration: 90, scope: '14 市州 · 310 所学校', creator: '省管理员', createTime: '2026-04-02', status: { type: 'success', label: '已结束' } }
]
const statusFilters = [
  { value: 'run', label: '已发布' }, { value: 'warning', label: '暂存' }, { value: 'success', label: '已结束' }
]
</script>

<style scoped>
.toolbar {
  display: flex; justify-content: space-between; align-items: center; gap: 16px;
  margin-bottom: 16px; flex-wrap: wrap;
}
.tabs { display: flex; gap: 4px; background: #fff; border-radius: 8px; padding: 4px; box-shadow: 0 2px 10px rgba(70,90,130,0.06); }
.tab {
  padding: 6px 18px; border: none; background: transparent; border-radius: 6px;
  font-size: 13px; color: #6b7688; cursor: pointer;
}
.tab:hover { color: #2f6fe4; }
.tab.active { background: #2f6fe4; color: #fff; }
.btn-primary {
  padding: 9px 18px; border: none; border-radius: 6px;
  background: linear-gradient(95deg, #3f8ef7, #7b6cf0);
  color: #fff; font-size: 13px; cursor: pointer; font-weight: 500;
  display: inline-flex; align-items: center; gap: 5px;
}
.btn-outline {
  padding: 9px 16px; border: 1px solid #c9d6ee; border-radius: 6px;
  background: #fff; color: #2f6fe4; font-size: 13px; cursor: pointer;
}

/* 通用表格内工具栏 */
.toolbar-left { display: flex; gap: 10px; align-items: center; }
.search-input {
  padding: 7px 12px; border: 1px solid #e0e5ef; border-radius: 6px;
  font-size: 13px; width: 220px; outline: none;
}
.filter-select {
  padding: 7px 12px; border: 1px solid #e0e5ef; border-radius: 6px;
  font-size: 13px; outline: none; background: #fff;
}
.op-link {
  background: none; border: none; cursor: pointer; color: #2f6fe4; font-size: 12px; padding: 2px 6px;
}
.op-link:hover { text-decoration: underline; }
.op-link.danger { color: #ef4444; }

/* 弹层 */
.modal-overlay {
  position: fixed; inset: 0; background: rgba(20,28,50,0.45);
  display: flex; align-items: center; justify-content: center; z-index: 100;
}
.modal {
  background: #fff; border-radius: 14px; width: 720px; max-width: 95vw;
  max-height: 90vh; overflow: hidden; display: flex; flex-direction: column;
  box-shadow: 0 20px 60px rgba(20,28,50,0.2);
}
.modal-head {
  display: flex; justify-content: space-between; align-items: center;
  padding: 18px 22px; border-bottom: 1px solid #f0f2f7;
}
.modal-head h3 { margin: 0; font-size: 16px; font-weight: 600; color: #1f2a44; }
.close { border: none; background: none; font-size: 22px; color: #8a93a5; cursor: pointer; width: 28px; height: 28px; border-radius: 4px; }
.close:hover { background: #f4f6fa; color: #2b3445; }
.modal-body { padding: 22px; overflow-y: auto; flex: 1; }
.modal-foot {
  display: flex; justify-content: flex-end; gap: 10px;
  padding: 16px 22px; border-top: 1px solid #f0f2f7;
}

.form-grid {
  display: grid; grid-template-columns: repeat(2, 1fr); gap: 14px 16px; margin-bottom: 18px;
}
.form-item label {
  display: block; font-size: 12px; color: #6b7688; margin-bottom: 6px; font-weight: 500;
}
.form-item input, .form-item select {
  width: 100%; padding: 8px 12px; border: 1px solid #e0e5ef; border-radius: 6px;
  font-size: 13px; outline: none; box-sizing: border-box;
}
.form-item input:focus, .form-item select:focus { border-color: #4f9cf9; }

.form-section { margin-top: 8px; }
.section-title { font-size: 13px; font-weight: 600; color: #4a5568; margin-bottom: 10px; }
.mini-table { width: 100%; border-collapse: collapse; font-size: 12px; }
.mini-table th { background: #f7f9fc; padding: 8px 10px; text-align: left; color: #6b7688; font-weight: 500; border-bottom: 1px solid #eef1f6; }
.mini-table td { padding: 8px 10px; border-bottom: 1px solid #f4f6fa; color: #2b3445; }
</style>
