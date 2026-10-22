<template>
  <div>
    <div class="toolbar">
      <div class="search-group">
        <input class="search-input" placeholder="输入区县名称 / 区县编码搜索" />
        <select class="filter">
          <option>全部市州</option><option>成都市</option><option>绵阳市</option>
        </select>
      </div>
      <div class="actions">
        <button class="btn-outline">批量创建</button>
        <button class="btn-primary">新增区县账号</button>
      </div>
    </div>

    <div class="stat-row">
      <StatCard label="区县总数" :value="125" accent="#4f9cf9" />
      <StatCard label="已接入" :value="118" trend="5" accent="#2fbfa5" />
      <StatCard label="覆盖学生" :value="284520" accent="#a06ee8" />
      <StatCard label="下属学校" :value="328" accent="#f2709c" />
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
  { key: 'districtCode', label: '区县编码', width: 140 },
  { key: 'districtName', label: '区县名称' },
  { key: 'city', label: '所属市州' },
  { key: 'leader', label: '负责人' },
  { key: 'phone', label: '联系电话' },
  { key: 'schoolCount', label: '下属学校', align: 'center' },
  { key: 'studentCount', label: '学生数', align: 'center' },
  { key: 'createTime', label: '创建时间' },
  { key: 'status', label: '状态', width: 90 }
]
const list = Array.from({ length: 24 }).map((_, i) => ({
  districtCode: `Q${String(100 + i)}`,
  districtName: ['锦江区', '青羊区', '武侯区', '涪城区', '游仙区', '旌阳区', '中江县', '乐至县', '市中区', '翠屏区', '自流井区', '大安区'][i % 12],
  city: ['成都市', '成都市', '成都市', '绵阳市', '绵阳市', '德阳市', '德阳市', '资阳市', '乐山市', '宜宾市', '自贡市', '自贡市'][i % 12],
  leader: ['李主任', '王主任', '张主任', '陈主任', '赵主任', '周主任'][i % 6],
  phone: `028-${String(81000000 + i * 123)}`,
  schoolCount: 20 + (i % 15) * 3,
  studentCount: 3000 + (i % 30) * 200,
  createTime: `2026-0${(i % 9) + 1}-${String((i % 28) + 1).padStart(2, '0')}`,
  status: i % 12 === 0 ? { type: 'warning', label: '待接入' } : { type: 'success', label: '已接入' }
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
