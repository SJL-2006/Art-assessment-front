<template>
  <div>
    <div class="toolbar">
      <div class="search-group">
        <input class="search-input" placeholder="输入学校名称 / 学校编码搜索" />
        <select class="filter">
          <option>全部市州</option><option>成都市</option><option>绵阳市</option>
        </select>
        <select class="filter">
          <option>全部类型</option><option>小学</option><option>初中</option><option>高中</option>
        </select>
      </div>
      <div class="actions">
        <button class="btn-outline">批量创建</button>
        <button class="btn-outline">批量重置密码</button>
        <button class="btn-primary">新增学校账号</button>
      </div>
    </div>

    <div class="stat-row">
      <StatCard label="学校总数" :value="328" accent="#4f9cf9" />
      <StatCard label="已接入" :value="318" trend="3" accent="#2fbfa5" />
      <StatCard label="待接入" :value="10" accent="#f2b23e" />
      <StatCard label="覆盖区县" :value="125" accent="#a06ee8" />
    </div>

    <CommonTable :columns="columns" :data="list" :showOp="true" :paged="true" :pageSize="12" :searchable="false">
      <template #op="{ row }">
        <button class="op-link">查看</button>
        <button class="op-link">修改</button>
        <button class="op-link">重置密码</button>
        <button class="op-link danger">删除</button>
      </template>
    </CommonTable>
  </div>
</template>

<script setup>
import StatCard from '../../components/StatCard.vue'
import CommonTable from '../../components/CommonTable.vue'

const columns = [
  { key: 'schoolCode', label: '学校编码', width: 140 },
  { key: 'schoolName', label: '学校名称' },
  { key: 'type', label: '类型', width: 80 },
  { key: 'city', label: '所属市州' },
  { key: 'district', label: '所属区县' },
  { key: 'principal', label: '校长' },
  { key: 'phone', label: '联系电话' },
  { key: 'teacherCount', label: '教师数', align: 'center' },
  { key: 'studentCount', label: '学生数', align: 'center' },
  { key: 'connectTime', label: '接入时间' },
  { key: 'status', label: '状态', width: 90 }
]
const list = Array.from({ length: 24 }).map((_, i) => ({
  schoolCode: `SC${String(1000 + i)}`,
  schoolName: ['锦江区第一中学', '涪城区实验中学', '旌阳区外国语学校', '市中区第一小学', '武侯区附属小学', '高新区双语学校'][i % 6],
  type: ['初中', '初中', '初中', '小学', '小学', '小学'][i % 6],
  city: ['成都市', '绵阳市', '德阳市', '乐山市', '成都市', '成都市'][i % 6],
  district: ['锦江区', '涪城区', '旌阳区', '市中区', '武侯区', '高新区'][i % 6],
  principal: ['王校长', '李校长', '张校长', '陈校长', '赵校长', '刘校长'][i % 6],
  phone: `028-${String(80000000 + i * 123)}`,
  teacherCount: 80 + (i % 20) * 5,
  studentCount: 1200 + (i % 30) * 40,
  connectTime: `2026-0${(i % 9) + 1}-${String((i % 28) + 1).padStart(2, '0')}`,
  status: i % 15 === 0 ? { type: 'warning', label: '待接入' } : { type: 'success', label: '已接入' }
}))
</script>

<style scoped>
.toolbar { display: flex; justify-content: space-between; align-items: center; gap: 16px; margin-bottom: 16px; flex-wrap: wrap; }
.search-group { display: flex; gap: 10px; flex-wrap: wrap; }
.search-input { padding: 8px 12px; border: 1px solid #e0e5ef; border-radius: 6px; font-size: 13px; width: 240px; outline: none; }
.filter { padding: 8px 12px; border: 1px solid #e0e5ef; border-radius: 6px; font-size: 13px; background: #fff; }
.actions { display: flex; gap: 10px; }
.btn-outline { padding: 8px 16px; border: 1px solid #c9d6ee; border-radius: 6px; background: #fff; color: #2f6fe4; font-size: 13px; cursor: pointer; }
.btn-primary { padding: 8px 18px; border: none; border-radius: 6px; background: linear-gradient(95deg, #3f8ef7, #7b6cf0); color: #fff; font-size: 13px; cursor: pointer; }
.stat-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 18px; }
@media (max-width: 1100px) { .stat-row { grid-template-columns: repeat(2, 1fr); } }
.op-link { background: none; border: none; cursor: pointer; color: #2f6fe4; font-size: 12px; padding: 2px 5px; }
.op-link.danger { color: #ef4444; }
</style>
