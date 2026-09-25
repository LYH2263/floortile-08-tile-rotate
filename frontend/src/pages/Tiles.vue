<script setup>
import { computed, onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([])
const settings = ref({})
const defaultRotated = computed(() =>
  ['1', 'true', 'yes', 'on'].includes(String(settings.value.default_rotate).toLowerCase())
)
onMounted(async () => {
  items.value = (await getJSON('/api/tiles')).items
  settings.value = await getJSON('/api/settings')
})
</script>
<template>
  <div class="page">
    <h1>砖型库</h1>
    <p>默认旋向偏好：{{ defaultRotated ? '旋转90°' : '不旋转' }}（未指定旋向的测算按此执行）</p>
    <div class="tile-cards">
      <div v-for="t in items" :key="t.id" class="tile-card" :class="{ dirty: t.data_quality === 'dirty' }">
        <strong>{{ t.name }}</strong>
        <span>{{ t.tile_l }} × {{ t.tile_w }} m</span>
        <em v-if="t.data_quality === 'dirty'">无效规格</em>
      </div>
    </div>
  </div>
</template>
