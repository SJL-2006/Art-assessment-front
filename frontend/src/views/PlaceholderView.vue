<!-- 通用占位页：用于尚未实现的路由 -->
<template>
  <div class="wrap">
    <div class="card">
      <h2 class="title-splash">{{ $route.meta.title }}</h2>
      <p style="color:#8a93a5">该模块功能开发中，后续将按 Excel 的 "艺术测评系统功能设计.xlsx" 逐项实现。</p>
    </div>
  </div>
</template>

<script setup>
// 无逻辑，仅占位
</script>

<style scoped>
.wrap {
  max-width: 1000px;
  margin: 0 auto;
}
</style>
