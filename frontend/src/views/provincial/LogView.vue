<template>
  <div>
    <div class="toolbar">
      <div class="search-group">
        <input class="search-input" placeholder="搜索操作人 / 操作内容" />
        <select class="filter">
          <option>全部模块</option><option>账号管理</option><option>组卷</option><option>发布</option><option>系统</option>
        </select>
        <select class="filter">
          <option>全部动作</option><option>登录</option><option>新增</option><option>修改</option><option>删除</option><option>发布</option>
        </select>
        <input type="date" class="filter" />
      </div>
      <div class="actions">
        <button class="btn-outline">导出日志</button>
        <button class="btn-outline">清空筛选</button>
      </div>
    </div>

    <div class="stat-row">
      <StatCard label="今日操作数" :value="128" accent="#4f9cf9" />
      <StatCard label="本周操作数" :value="892" trend="6" accent="#a06ee8" />
      <StatCard label="本月操作数" :value="3845" accent="#2fbfa5" />
      <StatCard label="异常操作" :value="3" accent="#f2709c" />
    </div>

    <CommonTable :columns="columns" :data="list" :showOp="true" :paged="true" :pageSize="20" :searchable="false">
      <template #op="{ row }">
        <button class="op-link">详情</button>
        <button class="op-link" v-if="row.needAttention" style="color:#ef4444">处理</button>
      </template>
    </CommonTable>
  </div>
</template>

<script setup>
import StatCard from '../../components/StatCard.vue'
import CommonTable from '../../components/CommonTable.vue'

const columns = [
  { key: 'time', label: '时间', width: 160 },
  { key: 'module', label: '模块', width: 120 },
  { key: 'action', label: '操作', width: 100 },
  { key: 'operator', label: '操作人', width: 140 },
  { key: 'target', label: '操作对象' },
  { key: 'ip', label: 'IP 地址', width: 140 },
  { key: 'result', label: '结果', width: 90 },
  { key: 'remark', label: '备注' }
]
const list = [
  { time: '2026-10-22 10:45:12', module: '发布管理', action: '发布', operator: 'admin（省管理员）', target: 'S20261001 音乐七年级', ip: '10.12.34.56', result: { type: 'success', label: '成功' }, remark: '发布到全部14市州' },
  { time: '2026-10-22 10:30:01', module: '账号管理', action: '新增', operator: 'admin（省管理员）', target: '区县账号 Q112（眉山市丹棱县）', ip: '10.12.34.56', result: { type: 'success', label: '成功' }, remark: '' },
  { time: '2026-10-22 09:58:22', module: '组卷管理', action: '修改', operator: 'admin（省管理员）', target: 'S20261004 美术九年级', ip: '10.12.34.56', result: { type: 'success', label: '成功' }, remark: '替换3道题目' },
  { time: '2026-10-22 09:45:10', module: '账号管理', action: '登录', operator: 'admin（省管理员）', target: '管理员账号登录', ip: '10.12.34.56', result: { type: 'success', label: '成功' }, remark: '' },
  { time: '2026-10-22 09:44:58', module: '系统', action: '登录', operator: 'unknown', target: '登录失败：密码错误', ip: '118.24.5.89', result: { type: 'danger', label: '失败' }, remark: '连续3次失败，可能异常', needAttention: true },
  { time: '2026-10-21 17:22:45', module: '发布管理', action: '发布', operator: 'admin（省管理员）', target: 'S20261003 美术七年级', ip: '10.12.34.56', result: { type: 'success', label: '成功' }, remark: '' },
  { time: '2026-10-21 16:05:12', module: '账号管理', action: '批量导入', operator: 'admin（省管理员）', target: '学生账号 锦江区 3285 条', ip: '10.12.34.56', result: { type: 'success', label: '成功' }, remark: 'Excel 导入' },
  { time: '2026-10-21 14:33:00', module: '组卷管理', action: '删除', operator: 'admin（省管理员）', target: 'S20261000（已删除）', ip: '10.12.34.56', result: { type: 'success', label: '成功' }, remark: '误创建，删除' },
  { time: '2026-10-21 11:20:33', module: '系统', action: '导出', operator: 'admin（省管理员）', target: '省级测评参与率 Excel', ip: '10.12.34.56', result: { type: 'success', label: '成功' }, remark: '导出 14市州 × 125区县' },
  { time: '2026-10-20 14:32:00', module: '发布管理', action: '发布', operator: 'admin（省管理员）', target: 'S20261001 音乐七年级', ip: '10.12.34.56', result: { type: 'success', label: '成功' }, remark: '' },
  { time: '2026-10-20 14:10:11', module: '发布管理', action: '发布', operator: 'admin（省管理员）', target: 'S20261002 音乐八年级', ip: '10.12.34.56', result: { type: 'success', label: '成功' }, remark: '' },
  { time: '2026-10-20 10:00:00', module: '账号管理', action: '重置密码', operator: 'admin（省管理员）', target: '成都学校账号 SC1015', ip: '10.12.34.56', result: { type: 'success', label: '成功' }, remark: '' }
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
