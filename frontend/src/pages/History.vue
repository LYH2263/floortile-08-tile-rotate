<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([])
onMounted(async () => { items.value = (await getJSON('/api/runs')).items })
</script>
<template>
  <div class="page">
    <h1>测算记录</h1>
    <table class="tbl">
      <thead><tr><th>时间</th><th>房间</th><th>砖型</th><th>旋向</th><th>片数</th></tr></thead>
      <tbody>
        <tr v-for="r in items" :key="r.id">
          <td>{{ r.created_at?.slice(0, 19) }}</td>
          <td>{{ r.room_name }}</td>
          <td>{{ r.tile_name }}</td>
          <td>{{ (r.rotated ?? r.result?.rotated) ? '旋转90°' : '不旋转' }}</td>
          <td>{{ r.result?.order_count }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
