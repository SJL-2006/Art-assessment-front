<template>
  <div>
    <div class="page-header">
      <div>
        <h2>省级测评发布</h2>
        <p class="page-sub">选择试卷并按市州 / 学校发布</p>
      </div>
      <button class="btn-primary">
        <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
          <path d="M5 12h14"/><path d="m13 6 6 6-6 6"/>
        </svg>
        发起新发布
      </button>
    </div>

    <div class="grid-3">
      <div v-for="item in publishPlans" :key="item.id" class="plan-card">
        <div class="plan-head">
          <span class="tag" :class="item.tagClass">{{ item.status }}</span>
          <span class="plan-subject" :style="{ background: item.color + '1f', color: item.color }">{{ item.subject }}</span>
        </div>
        <h4 class="plan-title">{{ item.name }}</h4>
        <div class="plan-meta">
          <div><svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>{{ item.timeRange }}</div>
          <div><svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15 15 0 0 1 0 20M12 2a15 15 0 0 0 0 20"/></svg>{{ item.scope }}</div>
        </div>
        <div class="plan-prog">
          <div class="prog-track">
            <div class="prog-fill" :style="{ width: item.progress + '%', background: item.color }"></div>
          </div>
          <div class="prog-text">{{ item.completed }} / {{ item.total }} 学校完成发布 · 参与率 {{ item.rate }}%</div>
        </div>
        <div class="plan-actions">
          <button class="op-btn">查看详情</button>
          <button class="op-btn">撤销发布</button>
          <button class="op-btn">查看统计</button>
        </div>
      </div>
    </div>

    <DataCard title="发布操作记录" accent="#4f9cf9">
      <CommonTable :columns="logCols" :data="logs" :showOp="false" :searchable="false" />
    </DataCard>
  </div>
</template>

<script setup>
import DataCard from '../../components/DataCard.vue'
import CommonTable from '../../components/CommonTable.vue'

const publishPlans = [
  { id: 1, name: '2026秋季省级音乐统一测评（七年级）', subject: '音乐', status: '进行中', tagClass: 'warning', color: '#a06ee8', timeRange: '2026-10-20 ~ 2026-11-20', scope: '14 市州 328 校', total: 328, completed: 310, progress: 94, rate: 93 },
  { id: 2, name: '2026秋季省级音乐统一测评（八年级）', subject: '音乐', status: '进行中', tagClass: 'warning', color: '#a06ee8', timeRange: '2026-10-20 ~ 2026-11-20', scope: '14 市州 321 校', total: 321, completed: 298, progress: 93, rate: 91 },
  { id: 3, name: '2026秋季省级美术统一测评（七年级）', subject: '美术', status: '进行中', tagClass: 'warning', color: '#2fbfa5', timeRange: '2026-10-18 ~ 2026-11-18', scope: '14 市州 321 校', total: 321, completed: 302, progress: 94, rate: 92 },
  { id: 4, name: '2026春季省级音乐测评（九年级）', subject: '音乐', status: '已完成', tagClass: 'success', color: '#a06ee8', timeRange: '2026-04-22 ~ 2026-05-22', scope: '14 市州 315 校', total: 315, completed: 315, progress: 100, rate: 97 },
  { id: 5, name: '2026春季省级美术测评（八年级）', subject: '美术', status: '已完成', tagClass: 'success', color: '#2fbfa5', timeRange: '2026-04-20 ~ 2026-05-20', scope: '14 市州 310 校', total: 310, completed: 310, progress: 100, rate: 96 },
  { id: 6, name: '2026秋季省级美术统一测评（九年级）', subject: '美术', status: '待发布', tagClass: 'default', color: '#2fbfa5', timeRange: '2026-11-01 ~ 2026-12-01', scope: '14 市州', total: 318, completed: 0, progress: 0, rate: 0 }
]
const logCols = [
  { key: 'time', label: '时间', width: 160 },
  { key: 'operator', label: '操作人' },
  { key: 'action', label: '操作' },
  { key: 'paper', label: '涉及试卷' },
  { key: 'scope', label: '发布范围' },
  { key: 'result', label: '结果' }
]
const logs = [
  { time: '2026-10-20 14:32', operator: '省管理员(admin)', action: '发布', paper: 'S20261001 音乐七年级', scope: '全部 14 市州', result: '成功' },
  { time: '2026-10-20 14:10', operator: '省管理员(admin)', action: '发布', paper: 'S20261002 音乐八年级', scope: '全部 14 市州', result: '成功' },
  { time: '2026-10-18 09:15', operator: '省管理员(admin)', action: '发布', paper: 'S20261003 美术七年级', scope: '全部 14 市州', result: '成功' },
  { time: '2026-10-10 16:00', operator: '省管理员(admin)', action: '撤回', paper: 'S20260903 音乐九年级', scope: '全部 14 市州', result: '成功' }
]
</script>

<style scoped>
.page-header {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 20px;
}
.page-header h2 { margin: 0; font-size: 20px; font-weight: 700; color: #1f2a44; }
.page-sub { margin: 4px 0 0; font-size: 13px; color: #8a93a5; }
.btn-primary {
  padding: 9px 18px; border: none; border-radius: 6px;
  background: linear-gradient(95deg, #3f8ef7, #7b6cf0);
  color: #fff; font-size: 13px; cursor: pointer; font-weight: 500;
  display: inline-flex; align-items: center; gap: 5px;
}

.grid-3 {
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 20px;
}
@media (max-width: 1200px) { .grid-3 { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 760px) { .grid-3 { grid-template-columns: 1fr; } }

.plan-card {
  background: #fff; border-radius: 12px; box-shadow: 0 2px 14px rgba(70,90,130,0.06);
  padding: 18px; transition: transform 0.2s, box-shadow 0.2s;
}
.plan-card:hover { transform: translateY(-2px); box-shadow: 0 8px 22px rgba(70,90,130,0.1); }
.plan-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
.tag { font-size: 11px; padding: 3px 10px; border-radius: 10px; font-weight: 600; }
.tag.success { background: #e6f8ed; color: #16a34a; }
.tag.warning { background: #fef3e2; color: #d97706; }
.tag.default { background: #f0f2f7; color: #6b7688; }
.plan-subject { font-size: 11px; padding: 3px 10px; border-radius: 10px; font-weight: 600; }

.plan-title { margin: 0 0 12px; font-size: 14px; font-weight: 700; color: #1f2a44; line-height: 1.4; }
.plan-meta { display: flex; flex-direction: column; gap: 6px; margin-bottom: 14px; font-size: 12px; color: #8a93a5; }
.plan-meta div { display: flex; align-items: center; gap: 6px; }
.plan-meta svg { color: #c9d1e0; }

.plan-prog { margin-bottom: 14px; }
.prog-track { height: 6px; background: #f0f2f7; border-radius: 3px; overflow: hidden; }
.prog-fill { height: 100%; border-radius: 3px; transition: width 0.6s ease; }
.prog-text { font-size: 11px; color: #8a93a5; margin-top: 6px; }

.plan-actions { display: flex; gap: 6px; padding-top: 12px; border-top: 1px solid #f4f6fa; }
.op-btn {
  flex: 1; padding: 6px 0; border: 1px solid #e0e5ef; border-radius: 6px;
  background: #fff; font-size: 12px; color: #4a5568; cursor: pointer; transition: all 0.15s;
}
.op-btn:hover { border-color: #4f9cf9; color: #4f9cf9; }
</style>
