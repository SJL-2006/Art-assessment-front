<template>
  <div>
    <div class="toolbar">
      <div class="search-group">
        <input class="search-input" placeholder="输入学籍号 / 账号 / 姓名搜索" />
        <select class="filter">
          <option>全部市州</option><option>成都市</option><option>绵阳市</option>
        </select>
        <select class="filter">
          <option>全部学校</option><option>第一中学</option>
        </select>
        <select class="filter">
          <option>全部年级</option><option>七年级</option>
        </select>
      </div>
      <div class="actions">
        <button class="btn-outline">批量导入</button>
        <button class="btn-primary">
          <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg>
          新增学生
        </button>
      </div>
    </div>

    <div class="stat-row">
      <StatCard label="学生总数" :value="284520" accent="#4f9cf9" />
      <StatCard label="已激活" :value="268974" trend="5" accent="#2fbfa5" />
      <StatCard label="未激活" :value="12546" accent="#f2b23e" />
      <StatCard label="禁用账号" :value="3000" accent="#f2709c" />
    </div>

    <CommonTable :columns="columns" :data="list" :showOp="true" :paged="true" :pageSize="15" :searchable="false">
      <template #op="{ row }">
        <button class="op-link">查看</button>
        <button class="op-link">修改</button>
        <button class="op-link">重置密码</button>
        <button class="op-link danger">禁用</button>
      </template>
    </CommonTable>
  </div>
</template>

<script setup>
import StatCard from '../../components/StatCard.vue'
import CommonTable from '../../components/CommonTable.vue'

const columns = [
  { key: 'id', label: '序号', width: 60 },
  { key: 'studentNo', label: '学籍号' },
  { key: 'account', label: '登录账号' },
  { key: 'name', label: '姓名' },
  { key: 'gender', label: '性别', width: 70 },
  { key: 'city', label: '市州' },
  { key: 'district', label: '区县' },
  { key: 'school', label: '学校' },
  { key: 'grade', label: '年级', width: 80 },
  { key: 'class', label: '班级', width: 80 },
  { key: 'phone', label: '联系电话' },
  { key: 'createTime', label: '创建时间' },
  { key: 'status', label: '状态', width: 90 }
]
const list = Array.from({ length: 36 }).map((_, i) => ({
  id: i + 1,
  studentNo: `51010${String(i * 12 + 3).padStart(6, '0')}`,
  account: `stu_chen_${String(1001 + i)}`,
  name: ['陈同学', '李同学', '王同学', '张同学', '赵同学', '周同学'][i % 6],
  gender: i % 2 ? '女' : '男',
  city: ['成都市', '绵阳市', '德阳市', '乐山市'][i % 4],
  district: ['锦江区', '涪城区', '旌阳区', '市中区'][i % 4],
  school: ['第一中学', '第二小学', '实验中学', '外国语学校'][i % 4],
  grade: ['七年级', '八年级', '九年级'][i % 3],
  class: `${(i % 6) + 1}班`,
  phone: `138****${String(1000 + i * 7).padStart(4, '0')}`,
  createTime: `2026-0${(i % 9) + 1}-${String((i % 28) + 1).padStart(2, '0')}`,
  status: i % 10 === 0 ? { type: 'danger', label: '禁用' } : { type: 'success', label: '已激活' }
}))
</script>

<style scoped>
.toolbar { display: flex; justify-content: space-between; align-items: center; gap: 16px; margin-bottom: 16px; flex-wrap: wrap; }
.search-group { display: flex; gap: 10px; flex-wrap: wrap; }
.search-input { padding: 8px 12px; border: 1px solid #e0e5ef; border-radius: 6px; font-size: 13px; width: 240px; outline: none; }
.filter { padding: 8px 12px; border: 1px solid #e0e5ef; border-radius: 6px; font-size: 13px; background: #fff; }
.actions { display: flex; gap: 10px; }
.btn-outline { padding: 8px 16px; border: 1px solid #c9d6ee; border-radius: 6px; background: #fff; color: #2f6fe4; font-size: 13px; cursor: pointer; }
.btn-primary { padding: 8px 18px; border: none; border-radius: 6px; background: linear-gradient(95deg, #3f8ef7, #7b6cf0); color: #fff; font-size: 13px; cursor: pointer; display: inline-flex; align-items: center; gap: 5px; }

.stat-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 18px; }
@media (max-width: 1100px) { .stat-row { grid-template-columns: repeat(2, 1fr); } }

.op-link { background: none; border: none; cursor: pointer; color: #2f6fe4; font-size: 12px; padding: 2px 5px; }
.op-link:hover { text-decoration: underline; }
.op-link.danger { color: #ef4444; }
</style>
