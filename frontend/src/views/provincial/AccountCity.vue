<template>
  <div>
    <div class="toolbar">
      <div class="search-group">
        <input class="search-input" placeholder="输入市州名称 / 市州编码搜索" />
      </div>
      <div class="actions">
        <button class="btn-outline">批量创建</button>
        <button class="btn-primary">新增市州账号</button>
      </div>
    </div>

    <div class="stat-row">
      <StatCard label="市州总数" :value="14" accent="#4f9cf9" />
      <StatCard label="已接入" :value="14" trend="0" accent="#2fbfa5" />
      <StatCard label="覆盖区县" :value="125" accent="#a06ee8" />
      <StatCard label="覆盖学生" :value="284520" accent="#f2709c" />
    </div>

    <CommonTable :columns="columns" :data="list" :showOp="true" :searchable="false">
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
  { key: 'cityCode', label: '市州编码', width: 140 },
  { key: 'cityName', label: '市州名称' },
  { key: 'leader', label: '负责人' },
  { key: 'phone', label: '联系电话' },
  { key: 'districtCount', label: '下属区县', align: 'center' },
  { key: 'schoolCount', label: '学校数', align: 'center' },
  { key: 'studentCount', label: '学生数', align: 'center' },
  { key: 'createTime', label: '创建时间' },
  { key: 'status', label: '状态', width: 90 }
]
const list = [
  { cityCode: 'C01', cityName: '成都市', leader: '李主任', phone: '028-81000000', districtCount: 20, schoolCount: 82, studentCount: 75600, createTime: '2026-01-15', status: { type: 'success', label: '已接入' } },
  { cityCode: 'C02', cityName: '绵阳市', leader: '王主任', phone: '0816-6000000', districtCount: 9, schoolCount: 36, studentCount: 28400, createTime: '2026-01-15', status: { type: 'success', label: '已接入' } },
  { cityCode: 'C03', cityName: '德阳市', leader: '张主任', phone: '0838-2000000', districtCount: 6, schoolCount: 24, studentCount: 18200, createTime: '2026-01-16', status: { type: 'success', label: '已接入' } },
  { cityCode: 'C04', cityName: '乐山市', leader: '陈主任', phone: '0833-2000000', districtCount: 11, schoolCount: 28, studentCount: 22500, createTime: '2026-01-18', status: { type: 'success', label: '已接入' } },
  { cityCode: 'C05', cityName: '宜宾市', leader: '赵主任', phone: '0831-2000000', districtCount: 10, schoolCount: 26, studentCount: 21000, createTime: '2026-01-18', status: { type: 'success', label: '已接入' } },
  { cityCode: 'C06', cityName: '自贡市', leader: '周主任', phone: '0813-2000000', districtCount: 4, schoolCount: 18, studentCount: 14000, createTime: '2026-01-20', status: { type: 'success', label: '已接入' } },
  { cityCode: 'C07', cityName: '广元市', leader: '孙主任', phone: '0839-2000000', districtCount: 7, schoolCount: 16, studentCount: 12000, createTime: '2026-01-20', status: { type: 'success', label: '已接入' } },
  { cityCode: 'C08', cityName: '攀枝花市', leader: '吴主任', phone: '0812-2000000', districtCount: 5, schoolCount: 14, studentCount: 10500, createTime: '2026-01-22', status: { type: 'success', label: '已接入' } },
  { cityCode: 'C09', cityName: '泸州市', leader: '郑主任', phone: '0830-2000000', districtCount: 7, schoolCount: 22, studentCount: 19800, createTime: '2026-01-25', status: { type: 'success', label: '已接入' } },
  { cityCode: 'C10', cityName: '南充市', leader: '冯主任', phone: '0817-2000000', districtCount: 9, schoolCount: 28, studentCount: 25600, createTime: '2026-01-28', status: { type: 'success', label: '已接入' } },
  { cityCode: 'C11', cityName: '达州市', leader: '何主任', phone: '0818-2000000', districtCount: 7, schoolCount: 22, studentCount: 18500, createTime: '2026-02-02', status: { type: 'success', label: '已接入' } },
  { cityCode: 'C12', cityName: '眉山市', leader: '罗主任', phone: '028-38000000', districtCount: 6, schoolCount: 20, studentCount: 16800, createTime: '2026-02-05', status: { type: 'success', label: '已接入' } },
  { cityCode: 'C13', cityName: '资阳市', leader: '梁主任', phone: '028-26000000', districtCount: 3, schoolCount: 16, studentCount: 14200, createTime: '2026-02-08', status: { type: 'success', label: '已接入' } },
  { cityCode: 'C14', cityName: '内江市', leader: '余主任', phone: '0832-2000000', districtCount: 5, schoolCount: 18, studentCount: 15000, createTime: '2026-02-10', status: { type: 'success', label: '已接入' } }
]
</script>

<style scoped>
.toolbar { display: flex; justify-content: space-between; align-items: center; gap: 16px; margin-bottom: 16px; flex-wrap: wrap; }
.search-group { display: flex; gap: 10px; flex-wrap: wrap; }
.search-input { padding: 8px 12px; border: 1px solid #e0e5ef; border-radius: 6px; font-size: 13px; width: 240px; outline: none; }
.actions { display: flex; gap: 10px; }
.btn-outline { padding: 8px 16px; border: 1px solid #c9d6ee; border-radius: 6px; background: #fff; color: #2f6fe4; font-size: 13px; cursor: pointer; }
.btn-primary { padding: 8px 18px; border: none; border-radius: 6px; background: linear-gradient(95deg, #3f8ef7, #7b6cf0); color: #fff; font-size: 13px; cursor: pointer; }
.stat-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 18px; }
@media (max-width: 1100px) { .stat-row { grid-template-columns: repeat(2, 1fr); } }
.op-link { background: none; border: none; cursor: pointer; color: #2f6fe4; font-size: 12px; padding: 2px 5px; }
.op-link.danger { color: #ef4444; }
</style>
