<template>
  <div class="region-cascade">
    <select
      v-if="role === 'city'"
      class="c-select"
      :value="districtId"
      @change="onDistrictChange($event.target.value)"
    >
      <option value="">全部区县</option>
      <option v-for="d in districts" :key="d.id" :value="d.id">{{ d.name }}</option>
    </select>
    <select
      v-if="role !== 'school'"
      class="c-select"
      :value="schoolId"
      @change="$emit('update:schoolId', $event.target.value)"
    >
      <option value="">全部学校</option>
      <option v-for="s in schoolOptions" :key="s.id" :value="s.id">{{ s.name }}</option>
    </select>
  </div>
</template>

<script setup>
import { computed, watch } from 'vue'
import { DISTRICT_ID, districts, schools, schoolsOfDistrict } from '../data/consoleData'

const props = defineProps({
  role: { type: String, default: 'school' },
  districtId: { type: String, default: '' },
  schoolId: { type: String, default: '' }
})
const emit = defineEmits(['update:districtId', 'update:schoolId'])

const schoolOptions = computed(() => {
  if (props.role === 'city') {
    return props.districtId ? schoolsOfDistrict(props.districtId) : schools
  }
  return schoolsOfDistrict(DISTRICT_ID)
})

function onDistrictChange(value) {
  emit('update:districtId', value)
}

watch(
  () => props.districtId,
  () => {
    if (props.schoolId && !schoolOptions.value.some(s => s.id === props.schoolId)) {
      emit('update:schoolId', '')
    }
  }
)
</script>

<style scoped>
.region-cascade {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}
.region-cascade .c-select {
  width: auto;
  min-width: 132px;
}
</style>
