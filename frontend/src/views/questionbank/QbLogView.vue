<template>
  <div>
    <div class="toolbar">
      <div class="search-group">
        <input class="search-input" placeholder="搜索操作人 / 操作内容" />
        <select class="filter"><option>全部模块</option><option>试题管理</option><option>审核</option><option>课程</option><option>章节</option><option>资源</option></select>
        <select class="filter"><option>全部动作</option><option>上传</option><option>审核通过</option><option>审核驳回</option><option>编辑</option><option>删除</option></select>
        <input type="date" class="filter" />
      </div>
      <div class="actions">
        <button class="btn-outline">导出日志</button>
      </div>
    </div>

    <div class="stat-row">
      <StatCard label="今日操作" :value="156" accent="#4f9cf9" />
      <StatCard label="本周操作" :value="1024" trend="8" accent="#a06ee8" />
      <StatCard label="本月操作" :value="4280" accent="#2fbfa5" />
      <StatCard label="待处理驳回" :value="12" accent="#f2709c" />
    </div>

    <CommonTable :columns="columns" :data="list" :showOp="true" :paged="true" :pageSize="20" :searchable="false">
      <template #op="{ row }">
        <button class="op-link">详情</button>
      </template>
    </CommonTable>
  </div>
</template>

<script setup>
import StatCard from '../../components/StatCard.vue'
import CommonTable from '../../components/CommonTable.vue'

const columns = [
  { key: 'time', label: '时间', width: 160 },
  { key: 'module', label: '模块', width: 110 },
  { key: 'action', label: '操作', width: 100 },
  { key: 'operator', label: '操作人', width: 140 },
  { key: 'role', label: '角色', width: 100 },
  { key: 'target', label: '操作对象' },
  { key: 'result', label: '结果', width: 90 },
  { key: 'remark', label: '备注' }
]
const list = [
  { time: '2026-10-22 10:45:12', module: '试题审核', action: '审核通过', operator: '题库管理员', role: '管理员', target: 'Q5856 音乐·七年级·判断题', result: { type: 'success', label: '成功' }, remark: '第 1289 个通过' },
  { time: '2026-10-22 10:30:01', module: '资源管理', action: '上传', operator: '张老师', role: '教师', target: 'audio_1025.mp3（2.4MB）', result: { type: 'success', label: '成功' }, remark: '为 Q5853 添加' },
  { time: '2026-10-22 10:10:22', module: '试题管理', action: '新增', operator: '李老师', role: '教师', target: '美术·七年级·选择题·2 道', result: { type: 'warning', label: '待审' }, remark: '提交审核' },
  { time: '2026-10-22 09:58:30', module: '章节管理', action: '编辑', operator: '题库管理员', role: '管理员', target: '初中音乐·第三单元·第2节', result: { type: 'success', label: '成功' }, remark: '' },
  { time: '2026-10-22 09:45:10', module: '系统', action: '登录', operator: 'admin', role: '管理员', target: '题库管理端登录', result: { type: 'success', label: '成功' }, remark: '' },
  { time: '2026-10-22 09:22:15', module: '试题审核', action: '驳回', operator: '题库管理员', role: '管理员', target: 'Q5847 音乐·九年级·简答题', result: { type: 'danger', label: '驳回' }, remark: '答案要点不够具体' },
  { time: '2026-10-21 17:22:45', module: '试题管理', action: '编辑', operator: '王老师', role: '教师', target: 'Q5860 音乐·九年级·选择题', result: { type: 'success', label: '成功' }, remark: '' },
  { time: '2026-10-21 16:30:00', module: '资源管理', action: '删除', operator: '题库管理员', role: '管理员', target: 'image_1990.jpg（未关联）', result: { type: 'success', label: '成功' }, remark: '清理未使用资源' },
  { time: '2026-10-21 15:20:33', module: '课程管理', action: '新增', operator: '题库管理员', role: '管理员', target: '初中美术（岭南版）', result: { type: 'success', label: '成功' }, remark: '28 章节 · 1202 题' },
  { time: '2026-10-21 11:08:00', module: '试题审核', action: '审核通过', operator: '题库管理员', role: '管理员', target: 'Q5857 美术·八年级·创作题', result: { type: 'success', label: '成功' }, remark: '' }
]
</script>

<style scoped>
.toolbar { display: flex; justify-content: space-between; align-items: center; gap: 16px; margin-bottom: 16px; flex-wrap: wrap; }
.search-group { display: flex; gap: 10px; flex-wrap: wrap; }
.search-input { padding: 8px 12px; border: 1px solid #e0e5ef; border-radius: 6px; font-size: 13px; width: 240px; outline: none; }
.filter { padding: 8px 12px; border: 1px solid #e0e5ef; border-radius: 6px; font-size: 13px; background: #fff; }
.actions { display: flex; gap: 10px; }
.btn-outline { padding: 8px 16px; border: 1px solid #c9d6ee; border-radius: 6px; background: #fff; color: #2f6fe4; font-size: 13px; cursor: pointer; }
.stat-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 18px; }
@media (max-width: 1100px) { .stat-row { grid-template-columns: repeat(2, 1fr); } }
.op-link { background: none; border: none; cursor: pointer; color: #2f6fe4; font-size: 12px; padding: 2px 5px; }
</style>
