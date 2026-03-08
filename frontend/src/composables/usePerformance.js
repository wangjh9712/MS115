import { ref, onMounted, onUnmounted } from 'vue'

/**
 * 防抖函数
 * @param {Function} fn - 要执行的函数
 * @param {number} delay - 延迟时间（毫秒）
 * @returns {Function}
 */
export function useDebounce(fn, delay = 300) {
  let timer = null

  const debouncedFn = (...args) => {
    if (timer) clearTimeout(timer)
    timer = setTimeout(() => {
      fn(...args)
    }, delay)
  }

  const cancel = () => {
    if (timer) {
      clearTimeout(timer)
      timer = null
    }
  }

  return { debouncedFn, cancel }
}

/**
 * 节流函数
 * @param {Function} fn - 要执行的函数
 * @param {number} limit - 限制时间（毫秒）
 * @returns {Function}
 */
export function useThrottle(fn, limit = 100) {
  let inThrottle = false
  let lastFn = null
  let lastTime = 0

  const throttledFn = (...args) => {
    const now = Date.now()

    if (!inThrottle) {
      fn(...args)
      lastTime = now
      inThrottle = true
      setTimeout(() => {
        inThrottle = false
        if (lastFn) {
          lastFn()
          lastFn = null
        }
      }, limit)
    } else {
      lastFn = () => fn(...args)
    }
  }

  return throttledFn
}

/**
 * 使用 Intersection Observer 进行懒加载
 * @param {Object} options - 配置选项
 * @returns {Object}
 */
export function useIntersectionObserver(options = {}) {
  const { threshold = 0.1, rootMargin = '50px' } = options
  const isVisible = ref(false)
  const targetRef = ref(null)
  let observer = null

  onMounted(() => {
    if (!targetRef.value) return

    observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          isVisible.value = true
          // 一旦可见就停止观察
          observer?.unobserve(targetRef.value)
        }
      },
      { threshold, rootMargin }
    )

    observer.observe(targetRef.value)
  })

  onUnmounted(() => {
    if (observer && targetRef.value) {
      observer.unobserve(targetRef.value)
      observer = null
    }
  })

  return { targetRef, isVisible }
}

/**
 * 使用 requestAnimationFrame 优化滚动
 * @param {Function} callback - 回调函数
 * @returns {Object}
 */
export function useRafScroll(callback) {
  let rafId = null
  let lastScrollTop = 0

  const handleScroll = (event) => {
    if (rafId) return

    rafId = requestAnimationFrame(() => {
      rafId = null
      const scrollTop = event.target.scrollTop
      const scrollDelta = scrollTop - lastScrollTop
      lastScrollTop = scrollTop

      callback({
        scrollTop,
        scrollDelta,
        event
      })
    })
  }

  const cancel = () => {
    if (rafId) {
      cancelAnimationFrame(rafId)
      rafId = null
    }
  }

  return { handleScroll, cancel }
}

/**
 * 图片预加载
 * @param {string[]} urls - 图片 URL 数组
 * @returns {Promise}
 */
export function preloadImages(urls) {
  return Promise.all(
    urls.map(url => {
      return new Promise((resolve, reject) => {
        const img = new Image()
        img.onload = resolve
        img.onerror = reject
        img.src = url
      })
    })
  )
}

/**
 * 使用 Web Worker 进行耗时计算
 * @param {Function} fn - 要在 Worker 中执行的函数
 * @returns {Function}
 */
export function useWebWorker(fn) {
  const workerScript = `
    self.onmessage = function(e) {
      const result = (${fn.toString()})(e.data);
      self.postMessage(result);
    }
  `
  const blob = new Blob([workerScript], { type: 'application/javascript' })
  const worker = new Worker(URL.createObjectURL(blob))

  const run = (data) => {
    return new Promise((resolve) => {
      worker.onmessage = (e) => resolve(e.data)
      worker.postMessage(data)
    })
  }

  const terminate = () => {
    worker.terminate()
  }

  return { run, terminate }
}
