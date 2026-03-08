<template>
  <div ref="containerRef" class="virtual-list-container" @scroll="handleScroll">
    <div class="virtual-list-phantom" :style="{ height: `${totalHeight}px` }" />
    <div class="virtual-list-content" :style="{ transform: `translateY(${offsetY}px)` }">
      <div
        v-for="item in visibleItems"
        :key="item.key"
        class="virtual-list-item"
        :style="{ height: `${itemHeight}px` }"
      >
        <slot :item="item.data" :index="item.index" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch, nextTick } from 'vue'

const props = defineProps({
  items: {
    type: Array,
    default: () => []
  },
  itemHeight: {
    type: Number,
    default: 300
  },
  bufferSize: {
    type: Number,
    default: 5
  }
})

const containerRef = ref(null)
const scrollTop = ref(0)
const containerHeight = ref(0)

// 计算总高度
const totalHeight = computed(() => props.items.length * props.itemHeight)

// 计算可见区域的起始和结束索引
const visibleRange = computed(() => {
  const start = Math.floor(scrollTop.value / props.itemHeight)
  const visibleCount = Math.ceil(containerHeight.value / props.itemHeight)

  // 添加缓冲区
  const startIndex = Math.max(0, start - props.bufferSize)
  const endIndex = Math.min(props.items.length, start + visibleCount + props.bufferSize)

  return { startIndex, endIndex }
})

// 计算可见项
const visibleItems = computed(() => {
  const { startIndex, endIndex } = visibleRange.value
  return props.items.slice(startIndex, endIndex).map((item, index) => ({
    key: `${startIndex + index}-${item.id || index}`,
    data: item,
    index: startIndex + index
  }))
})

// 计算偏移量
const offsetY = computed(() => visibleRange.value.startIndex * props.itemHeight)

// 处理滚动事件
let scrollRafId = null
const handleScroll = () => {
  if (scrollRafId) return
  scrollRafId = requestAnimationFrame(() => {
    scrollRafId = null
    if (containerRef.value) {
      scrollTop.value = containerRef.value.scrollTop
      containerHeight.value = containerRef.value.clientHeight
    }
  })
}

// 监听 items 变化，重置滚动位置
watch(() => props.items.length, () => {
  nextTick(() => {
    if (containerRef.value) {
      containerHeight.value = containerRef.value.clientHeight
    }
  })
})

// 初始化容器高度
nextTick(() => {
  if (containerRef.value) {
    containerHeight.value = containerRef.value.clientHeight
  }
})
</script>

<style scoped>
.virtual-list-container {
  position: relative;
  overflow-y: auto;
  height: 100%;
}

.virtual-list-phantom {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
}

.virtual-list-content {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  will-change: transform;
}

.virtual-list-item {
  box-sizing: border-box;
}
</style>
