<template>
  <div>
    <div class="toolbar">
      <div class="filters">
        <select class="filter">
          <option>全部市州</option>
          <option>成都市</option><option>绵阳市</option><option>德阳市</option>
        </select>
        <select class="filter">
          <option>全部学科</option>
          <option>音乐</option><option>美术</option>
        </select>
        <select class="filter">
          <option>全部年级</option>
          <option>七年级</option><option>八年级</option><option>九年级</option>
        </select>
        <select class="filter">
          <option>2026秋季</option>
          <option>2026春季</option><option>2025秋季</option>
        </select>
      </div>
      <div class="actions">
        <button class="btn-outline">导出 Excel</button>
        <button class="btn-primary">生成统计报告</button>
      </div>
    </div>

    <div class="stat-row">
      <StatCard label="应参加学生" :value="284520" accent="#4f9cf9" />
      <StatCard label="实参加学生" :value="268974" trend="5" accent="#2fbfa5" />
      <StatCard label="平均成绩" :value="'82.3'" subLabel="满分 100" accent="#a06ee8" />
      <StatCard label="优秀率" :value="'38.6%'" trend="4" accent="#f2709c" />
    </div>

    <div class="grid-2">
      <DataCard title="各市州成绩分布（音乐）" accent="#a06ee8">
        <div class="bar-chart">
          <div v-for="item in musicCityScores" :key="item.name" class="bar-row">
            <span class="bar-label">{{ item.name }}</span>
            <div class="bar-track">
              <div class="bar-fill" :style="{ width: item.score + '%', background: '#a06ee8' }"></div>
            </div>
            <span class="bar-val">{{ item.score }}</span>
          </div>
        </div>
      </DataCard>

      <DataCard title="各市州成绩分布（美术）" accent="#2fbfa5">
        <div class="bar-chart">
          <div v-for="item in artCityScores" :key="item.name" class="bar-row">
            <span class="bar-label">{{ item.name }}</span>
            <div class="bar-track">
              <div class="bar-fill" :style="{ width: item.score + '%', background: '#2fbfa5' }"></div>
            </div>
            <span class="bar-val">{{ item.score }}</span>
          </div>
        </div>
      </DataCard>
    </div>

    <DataCard title="年级维度对比（音乐 vs 美术）" accent="#4f9cf9">
      <CommonTable
        :columns="columns"
        :data="gradeData"
        :showOp="false"
      >
        <template #op></template>
      </CommonTable>
    </DataCard>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import StatCard from '../../components/StatCard.vue'
import DataCard from '../../components/DataCard.vue'
import CommonTable from '../../components/CommonTable.vue'

const musicCityScores = [
  { name: '成都市', score: 88 }, { name: '绵阳市', score: 85 }, { name: '德阳市', score: 82 },
  { name: '乐山市', score: 79 }, { name: '宜宾市', score: 77 }, { name: '自贡市', score: 74 },
  { name: '广元市', score: 71 }, { name: '攀枝花', score: 73 }
]
const artCityScores = [
  { name: '成都市', score: 86 }, { name: '绵阳市', score: 83 }, { name: '德阳市', score: 84 },
  { name: '乐山市', score: 81 }, { name: '宜宾市', score: 79 }, { name: '自贡市', score: 76 },
  { name: '广元市', score: 72 }, { name: '攀枝花', score: 75 }
]
const columns = [
  { key: 'grade', label: '年级' },
  { key: 'musicCount', label: '音乐参考人' },
  { key: 'musicAvg', label: '音乐平均分' },
  { key: 'musicRate', label: '音乐优秀率' },
  { key: 'artCount', label: '美术参考人' },
  { key: 'artAvg', label: '美术平均分' },
  { key: 'artRate', label: '美术优秀率' },
  { key: 'totalRate', label: '综合参与率' }
]
const gradeData = [
  { grade: '七年级', musicCount: 98230, musicAvg: 83.2, musicRate: '39.2%', artCount: 97620, artAvg: 81.8, artRate: '37.5%', totalRate: '96.8%' },
  { grade: '八年级', musicCount: 92140, musicAvg: 81.5, musicRate: '36.7%', artCount: 91880, artAvg: 83.1, artRate: '40.1%', totalRate: '94.3%' },
  { grade: '九年级', musicCount: 78604, musicAvg: 82.8, musicRate: '38.1%', artCount: 77474, artAvg: 82.6, artRate: '38.2%', totalRate: '91.5%' }
]
</script>

<style scoped>
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  margin-bottom: 18px;
  flex-wrap: wrap;
}
.filters { display: flex; gap: 10px; flex-wrap: wrap; }
.filter {
  padding: 8px 14px;
  border: 1px solid #e0e5ef;
  border-radius: 6px;
  font-size: 13px;
  background: #fff;
  color: #2b3445;
}
.actions { display: flex; gap: 10px; }
.btn-outline {
  padding: 8px 16px; border: 1px solid #c9d6ee; border-radius: 6px;
  background: #fff; color: #2f6fe4; font-size: 13px; cursor: pointer;
}
.btn-outline:hover { background: #eef4ff; }
.btn-primary {
  padding: 8px 18px; border: none; border-radius: 6px;
  background: linear-gradient(95deg, #3f8ef7, #7b6cf0);
  color: #fff; font-size: 13px; cursor: pointer; font-weight: 500;
}

.stat-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 20px;
}
.grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}
@media (max-width: 1100px) {
  .stat-row { grid-template-columns: repeat(2, 1fr); }
  .grid-2 { grid-template-columns: 1fr; }
}

.bar-chart { display: flex; flex-direction: column; gap: 14px; }
.bar-row { display: flex; align-items: center; gap: 12px; font-size: 13px; }
.bar-label { width: 70px; color: #6b7688; flex-shrink: 0; }
.bar-track { flex: 1; height: 10px; background: #f0f2f7; border-radius: 5px; overflow: hidden; }
.bar-fill { height: 100%; border-radius: 5px; transition: width 0.8s ease; }
.bar-val { width: 40px; text-align: right; color: #2b3445; font-weight: 600; }
</style>
