<template>
  <Teleport to="body">
    <div class="toast-host">
      <TransitionGroup name="toast">
        <div v-for="item in toasts" :key="item.id" class="toast-item" :class="item.type">
          <AppIcon :name="iconOf(item.type)" :size="16" />
          <span>{{ item.message }}</span>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup>
import AppIcon from './AppIcon.vue'
import { toasts } from '../data/toast'

function iconOf(type) {
  if (type === 'error') return 'x-circle'
  if (type === 'info') return 'info'
  if (type === 'warning') return 'warning'
  return 'check-circle'
}
</script>

<style scoped>
.toast-host {
  position: fixed;
  top: 16px;
  left: 50%;
  z-index: 120;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  pointer-events: none;
}
.toast-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 9px 14px;
  border-radius: 6px;
  background: #fff;
  border: 1px solid #f0f0f0;
  box-shadow: 0 5px 16px rgba(0, 0, 0, 0.08);
  font-size: 13px;
  color: #1f2329;
  white-space: nowrap;
}
.toast-item.success {
  border-color: #c8ebd2;
  color: #1a9c3f;
}
.toast-item.error {
  border-color: #f7cfcd;
  color: #e0352f;
}
.toast-item.info {
  border-color: #c9e0ff;
  color: #1677ff;
}
.toast-item.warning {
  border-color: #f5e0b8;
  color: #b86800;
}
.toast-enter-active,
.toast-leave-active {
  transition: all 0.24s ease;
}
.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
