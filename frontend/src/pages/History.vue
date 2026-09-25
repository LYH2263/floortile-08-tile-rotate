<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([])
const expanded = ref(null)
onMounted(async () => { items.value = (await getJSON('/api/runs')).items })

function orientOf(r) {
  // 旧记录可能没有旋向字段，按正向铺展示（与改造前同参一致）
  return r.result?.rotated === true
}
async function toggle(r) {
  expanded.value = expanded.value === r.id ? null : r.id
}
</script>
<template>
  <div class="page">
    <h1>测算记录</h1>
    <table class="tbl">
      <thead><tr><th>时间</th><th>房间</th><th>砖型</th><th>片数</th><th>旋向</th><th></th></tr></thead>
      <tbody>
        <template v-for="r in items" :key="r.id">
          <tr>
            <td>{{ r.created_at?.slice(0, 19) }}</td>
            <td>{{ r.room_name }}</td>
            <td>{{ r.tile_name }}</td>
            <td>{{ r.result?.order_count }}</td>
            <td>{{ orientOf(r) ? '旋转 90°' : '正向铺' }}</td>
            <td><button class="link-btn" @click="toggle(r)">{{ expanded === r.id ? '收起' : '详情' }}</button></td>
          </tr>
          <tr v-if="expanded === r.id" class="detail-row">
            <td colspan="6">
              <ul>
                <li>当时旋向：<strong>{{ orientOf(r) ? '旋转 90° 铺' : '正向铺（不旋转）' }}</strong></li>
                <li>下单片数（order）：{{ r.result?.order_count }}，净用量：{{ r.result?.raw_count }}，损耗：{{ r.result?.waste_pct }}%</li>
                <li v-if="r.result?.layout">
                  当时网格（layout）：{{ r.result.layout.cols }} 列 × {{ r.result.layout.rows }} 行，共 {{ r.result.layout.grid_count }} 块
                </li>
                <li v-if="r.note">备注：{{ r.note }}</li>
              </ul>
            </td>
          </tr>
        </template>
      </tbody>
    </table>
  </div>
</template>
