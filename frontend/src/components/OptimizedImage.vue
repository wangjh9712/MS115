<template>
  <div class="optimized-image-wrapper" :style="wrapperStyle">
    <div v-if="!loaded && !error" class="image-skeleton" />
    <img
      v-show="loaded"
      :src="optimizedSrc"
      :alt="alt"
      :loading="loading"
      :fetchpriority="fetchpriority"
      decoding="async"
      @load="handleLoad"
      @error="handleError"
    />
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  src: {
    type: String,
    default: ''
  },
  alt: {
    type: String,
    default: ''
  },
  width: {
    type: [Number, String],
    default: null
  },
  height: {
    type: [Number, String],
    default: null
  },
  loading: {
    type: String,
    default: 'lazy'
  },
  fetchpriority: {
    type: String,
    default: 'auto'
  },
  quality: {
    type: Number,
    default: 80
  }
})

const emit = defineEmits(['load', 'error'])

const loaded = ref(false)
const error = ref(false)

// TMDB 图片优化处理
const optimizedSrc = computed(() => {
  if (!props.src) return ''

  // 如果是 TMDB 图片，使用更小的尺寸
  if (props.src.includes('image.tmdb.org')) {
    // 根据设备像素比选择合适的尺寸
    const dpr = window.devicePixelRatio || 1
    const targetWidth = props.width ? Math.round(props.width * dpr) : 500

    // 选择合适的 TMDB 尺寸
    let size = 'w500'
    if (targetWidth <= 200) size = 'w200'
    else if (targetWidth <= 300) size = 'w300'
    else if (targetWidth <= 400) size = 'w400'
    else if (targetWidth <= 500) size = 'w500'
    else size = 'w780'

    return props.src.replace(/w\d+/, size)
  }

  return props.src
})

const wrapperStyle = computed(() => ({
  width: props.width ? `${props.width}px` : '100%',
  height: props.height ? `${props.height}px` : 'auto',
  aspectRatio: props.width && props.height ? `${props.width}/${props.height}` : '2/3'
}))

const handleLoad = () => {
  loaded.value = true
  emit('load')
}

const handleError = () => {
  error.value = true
  emit('error')
}
</script>

<style scoped>
.optimized-image-wrapper {
  position: relative;
  overflow: hidden;
  background: var(--ms-bg-elevated);
}

.image-skeleton {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    110deg,
    rgba(78, 145, 221, 0.2) 18%,
    rgba(142, 199, 255, 0.36) 34%,
    rgba(78, 145, 221, 0.2) 52%
  );
  background-size: 220% 100%;
  animation: shimmer 1.2s ease-in-out infinite;
}

img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: opacity 0.2s ease;
}

@keyframes shimmer {
  0% {
    background-position: 120% 50%;
  }
  100% {
    background-position: -120% 50%;
  }
}
</style>
