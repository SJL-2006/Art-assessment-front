<template>
  <div>
    <div class="page-header">
      <div>
        <h2>全省地区测评参与率</h2>
        <p class="page-sub">导出各市州/区县测评参与率与成绩汇总数据</p>
      </div>
      <button class="btn-primary">
        <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="M7 10l5 5 5-5"/><path d="M12 15V3"/></svg>
        导出全部（Excel）
      </button>
    </div>

    <div class="toolbar">
      <div class="filters">
        <select class="filter">
          <option>2026秋季</option><option>2026春季</option><option>2025秋季</option>
        </select>
        <select class="filter">
          <option>全部学科</option><option>音乐</option><option>美术</option>
        </select>
        <select class="filter">
          <option>按市州汇总</option><option>按区县汇总</option>
        </select>
        <select class="filter">
          <option>全部年级</option><option>七年级</option><option>八年级</option><option>九年级</option>
        </select>
      </div>
      <button class="btn-outline">生成报告</button>
    </div>

    <div class="stat-row">
      <StatCard label="全省参与率" :value="participationRate" trend="3" accent="#4f9cf9" />
      <StatCard label="已参与学生" :value="268974" trend="12" accent="#2fbfa5" />
      <StatCard label="参考学校" :value="328" accent="#a06ee8" />
      <StatCard label="参考区县" :value="125" accent="#f2709c" />
    </div>

    <DataCard title="各市州参与率排名" accent="#4f9cf9">
      <CommonTable :columns="columns" :data="list" :showOp="false" :searchable="false">
        <template #rate="{ row }">
          <div class="rate-col">
            <div class="rate-track"><div class="rate-fill" :style="{ width: row.rate + '%', background: row.rateColor }"></div></div>
            <span class="rate-num">{{ row.rate }}%</span>
          </div>
        </template>
      </CommonTable>
    </DataCard>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import StatCard from '../../components/StatCard.vue'
import DataCard from '../../components/DataCard.vue'
import CommonTable from '../../components/CommonTable.vue'

const participationRate = computed(() => 94.5)
const cityData = [
  { name: '成都市', schools: 82, students: 75600, total: 78800, rate: 96, color: '#4f9cf9' },
  { name: '绵阳市', schools: 36, students: 28400, total: 32100, rate: 88, color: '#a06ee8' },
  { name: '德阳市', schools: 24, students: 18200, total: 22200, rate: 82, color: '#2fbfa5' },
  { name: '乐山市', schools: 28, students: 22500, total: 28500, rate: 79, color: '#f2709c' },
  { name: '宜宾市', schools: 26, students: 21000, total: 27200, rate: 77, color: '#f2b23e' },
  { name: '自贡市', schools: 18, students: 14000, total: 18900, rate: 74, color: '#8b7cf6' },
  { name: '泸州市', schools: 22, students: 19800, total: 27100, rate: 73, color: '#2fbfa5' },
  { name: '南充市', schools: 28, students: 25600, total: 35600, rate: 72, color: '#4f9cf9' },
  { name: '达州市', schools: 22, students: 18500, total: 26400, rate: 70, color: '#a06ee8' },
  { name: '内江市', schools: 18, students: 15000, total: 21600, rate: 69, color: '#f2709c' },
  { name: '眉山市', schools: 20, students: 16800, total: 24600, rate: 68, color: '#f2b23e' },
  { name: '广元市', schools: 16, students: 12000, total: 17900, rate: 67, color: '#8b7cf6' },
  { name: '攀枝花市', schools: 14, students: 10500, total: 15800, rate: 66, color: '#2fbfa5' },
  { name: '资阳市', schools: 16, students: 14200, total: 21800, rate: 65, color: '#4f9cf9' }
]
const columns = [
  { key: 'rank', label: '排名', width: 70 },
  { key: 'name', label: '市州' },
  { key: 'schools', label: '参考学校', align: 'center' },
  { key: 'students', label: '已参与学生', align: 'center' },
  { key: 'total', label: '应参与学生', align: 'center' },
  { key: 'rate', label: '参与率', width: 260, slot: 'rate' }
]
const list = cityData.map((d, i) => ({ ...d, rank: i + 1, rateColor: i < 3 ? '#16a34a' : i < 7 ? '#4f9cf9' : '#f2709c' }))
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px; }
.page-header h2 { margin: 0; font-size: 20px; font-weight: 700; color: #1f2a44; }
.page-sub { margin: 4px 0 0; font-size: 13px; color: #8a93a5; }
.btn-primary { padding: 9px 18px; border: none; border-radius: 6px; background: linear-gradient(95deg, #3f8ef7, #7b6cf0); color: #fff; font-size: 13px; cursor: pointer; display: inline-flex; align-items: center; gap: 5px; }

.toolbar { display: flex; justify-content: space-between; align-items: center; gap: 16px; margin-bottom: 18px; flex-wrap: wrap; }
.filters { display: flex; gap: 10px; flex-wrap: wrap; }
.filter { padding: 8px 12px; border: 1px solid #e0e5ef; border-radius: 6px; font-size: 13px; background: #fff; }
.btn-outline { padding: 8px 16px; border: 1px solid #c9d6ee; border-radius: 6px; background: #fff; color: #2f6fe4; font-size: 13px; cursor: pointer; }

.stat-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 18px; }
@media (max-width: 1100px) { .stat-row { grid-template-columns: repeat(2, 1fr); } }

.rate-col { display: flex; align-items: center; gap: 10px; }
.rate-track { flex: 1; height: 10px; background: #f0f2f7; border-radius: 5px; overflow: hidden; min-width: 120px; }
.rate-fill { height: 100%; border-radius: 5px; }
.rate-num { width: 50px; text-align: right; font-size: 13px; font-weight: 600; color: #2b3445; }
</style>
