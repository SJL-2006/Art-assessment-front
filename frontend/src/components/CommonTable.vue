<template>
  <div class="common-table">
    <!-- 工具栏 -->
    <div v-if="$slots.toolbar || toolbar?.length" class="table-toolbar">
      <slot name="toolbar">
        <div class="toolbar-left">
          <input v-if="searchable" v-model="keyword" class="search-input" :placeholder="searchPlaceholder" />
          <select v-if="filterable" v-model="filterVal" class="filter-select">
            <option value="">全部</option>
            <option v-for="f in filterOptions" :key="f.value" :value="f.value">{{ f.label }}</option>
          </select>
        </div>
        <div class="toolbar-right">
          <button v-if="showAdd" class="btn-primary" @click="$emit('add')">
            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
              <path d="M12 5v14M5 12h14"/>
            </svg>
            {{ addText }}
          </button>
        </div>
      </slot>
    </div>

    <!-- 表格 -->
    <div class="table-wrap">
      <table class="table">
        <thead>
          <tr>
            <th v-for="col in columns" :key="col.key" :style="{ width: col.width || 'auto', textAlign: col.align || 'left' }">{{ col.label }}</th>
            <th v-if="showOp" style="width: 160px">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, ri) in filteredRows" :key="ri">
            <td v-for="col in columns" :key="col.key" :style="{ textAlign: col.align || 'left' }">
              <template v-if="col.slot">
                <slot :name="col.slot" :row="row" :col="col" :index="ri" />
              </template>
              <template v-else>
                <span v-if="col.type === 'tag'" :class="['tag', row[col.key]?.type || '']">{{ row[col.key]?.label ?? row[col.key] }}</span>
                <span v-else-if="col.type === 'boolean'" :class="['bool', row[col.key] ? 'yes' : 'no']">{{ row[col.key] ? '是' : '否' }}</span>
                <span v-else>{{ row[col.key] }}</span>
              </template>
            </td>
            <td v-if="showOp">
              <slot name="op" :row="row" :index="ri">
                <button class="op-link" @click="$emit('view', row)">查看</button>
                <button class="op-link" @click="$emit('edit', row)">编辑</button>
                <button class="op-link danger" @click="$emit('delete', row)">删除</button>
              </slot>
            </td>
          </tr>
          <tr v-if="filteredRows.length === 0">
            <td :colspan="columns.length + (showOp ? 1 : 0)" class="empty">暂无数据</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 分页 -->
    <div v-if="paged" class="pagination">
      <span class="page-info">共 {{ filteredRows.length }} 条</span>
      <button class="page-btn" :disabled="page <= 1" @click="page--">上一页</button>
      <span class="page-num">{{ page }}</span>
      <button class="page-btn" :disabled="page >= totalPages" @click="page++">下一页</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  columns: { type: Array, required: true },
  data: { type: Array, default: () => [] },
  showOp: { type: Boolean, default: true },
  searchable: { type: Boolean, default: true },
  searchPlaceholder: { type: String, default: '搜索...' },
  filterable: { type: Boolean, default: false },
  filterOptions: { type: Array, default: () => [] },
  showAdd: { type: Boolean, default: false },
  addText: { type: String, default: '新增' },
  paged: { type: Boolean, default: false },
  pageSize: { type: Number, default: 10 }
})

const keyword = ref('')
const filterVal = ref('')
const page = ref(1)

const filteredRows = computed(() => {
  let rows = props.data
  if (keyword.value) {
    const kw = keyword.value.toLowerCase()
    rows = rows.filter(r =>
      props.columns.some(c => String(r[c.key] ?? '').toLowerCase().includes(kw))
    )
  }
  if (filterVal.value) {
    rows = rows.filter(r => r.status === filterVal.value || r.state === filterVal.value)
  }
  if (props.paged) {
    const start = (page.value - 1) * props.pageSize
    return rows.slice(start, start + props.pageSize)
  }
  return rows
})

const totalPages = computed(() => {
  return Math.max(1, Math.ceil(props.data.length / props.pageSize))
})

watch([keyword, filterVal], () => { page.value = 1 })
</script>

<style scoped>
.common-table {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 14px rgba(70,90,130,0.06);
  overflow: hidden;
}
.table-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 18px;
  border-bottom: 1px solid #f0f2f7;
  gap: 12px;
  flex-wrap: wrap;
}
.toolbar-left, .toolbar-right { display: flex; gap: 10px; align-items: center; }
.search-input {
  padding: 7px 12px;
  border: 1px solid #e0e5ef;
  border-radius: 6px;
  font-size: 13px;
  width: 220px;
  outline: none;
  transition: border-color 0.15s;
}
.search-input:focus { border-color: #4f9cf9; }
.filter-select {
  padding: 7px 12px;
  border: 1px solid #e0e5ef;
  border-radius: 6px;
  font-size: 13px;
  outline: none;
  background: #fff;
}
.btn-primary {
  background: linear-gradient(95deg, #3f8ef7, #7b6cf0);
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 7px 14px;
  font-size: 13px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 5px;
}
.btn-primary:hover { opacity: 0.92; }

.table-wrap { overflow-x: auto; }
.table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}
.table thead th {
  background: #f7f9fc;
  color: #6b7688;
  font-weight: 600;
  padding: 12px 14px;
  text-align: left;
  border-bottom: 1px solid #eef1f6;
  white-space: nowrap;
}
.table tbody td {
  padding: 12px 14px;
  border-bottom: 1px solid #f4f6fa;
  color: #2b3445;
  white-space: nowrap;
}
.table tbody tr:hover td { background: #fafbfe; }
.table tbody tr:last-child td { border-bottom: none; }
.table .empty { text-align: center; color: #a8b0c0; padding: 40px 0; background: #fafbfe; }

.tag {
  display: inline-block;
  padding: 2px 9px;
  border-radius: 10px;
  font-size: 11px;
  font-weight: 500;
}
.tag.success { background: #e6f8ed; color: #16a34a; }
.tag.warning { background: #fef3e2; color: #d97706; }
.tag.danger { background: #fdecee; color: #ef4444; }
.tag.info { background: #eef4ff; color: #2f6fe4; }
.tag.default { background: #f0f2f7; color: #6b7688; }

.bool.yes { color: #16a34a; font-weight: 600; }
.bool.no { color: #a8b0c0; }

.op-link {
  background: none; border: none; cursor: pointer;
  color: #2f6fe4; font-size: 12px; padding: 2px 6px;
}
.op-link:hover { text-decoration: underline; }
.op-link.danger { color: #ef4444; }

.pagination {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 10px;
  padding: 12px 18px;
  border-top: 1px solid #f0f2f7;
  font-size: 12px;
  color: #6b7688;
}
.page-btn {
  padding: 5px 12px;
  border: 1px solid #e0e5ef;
  background: #fff;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  color: #4a5568;
}
.page-btn:hover:not(:disabled) { border-color: #4f9cf9; color: #4f9cf9; }
.page-btn:disabled { opacity: 0.4; cursor: not-allowed; }
.page-num { color: #2f6fe4; font-weight: 600; }
</style>
