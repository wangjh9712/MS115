/**
 * 性能监控工具
 */

// 核心 Web Vitals 指标
export function measureWebVitals() {
  // Largest Contentful Paint (LCP)
  if ('PerformanceObserver' in window) {
    const lcpObserver = new PerformanceObserver((list) => {
      const entries = list.getEntries()
      const lastEntry = entries[entries.length - 1]
      console.log('[Performance] LCP:', Math.round(lastEntry.startTime), 'ms')
    })
    lcpObserver.observe({ entryTypes: ['largest-contentful-paint'] })
  }

  // First Input Delay (FID) / Interaction to Next Paint (INP)
  if ('PerformanceObserver' in window) {
    const fidObserver = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        const delay = entry.processingStart - entry.startTime
        console.log('[Performance] FID:', Math.round(delay), 'ms')
      }
    })
    fidObserver.observe({ entryTypes: ['first-input'] })
  }

  // Cumulative Layout Shift (CLS)
  if ('PerformanceObserver' in window) {
    let clsValue = 0
    const clsObserver = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        if (!entry.hadRecentInput) {
          clsValue += entry.value
        }
      }
      console.log('[Performance] CLS:', clsValue.toFixed(4))
    })
    clsObserver.observe({ entryTypes: ['layout-shift'] })
  }

  // Time to First Byte (TTFB)
  window.addEventListener('load', () => {
    const navigation = performance.getEntriesByType('navigation')[0]
    if (navigation) {
      console.log('[Performance] TTFB:', Math.round(navigation.responseStart), 'ms')
      console.log('[Performance] DOM Ready:', Math.round(navigation.domContentLoadedEventEnd), 'ms')
      console.log('[Performance] Load Complete:', Math.round(navigation.loadEventEnd), 'ms')
    }
  })
}

/**
 * 测量资源加载性能
 */
export function measureResourceLoading() {
  if ('PerformanceObserver' in window) {
    const resourceObserver = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        // 只记录慢资源 (>500ms)
        if (entry.duration > 500) {
          console.log(
            `[Performance] Slow Resource: ${entry.name.split('/').pop()}`,
            `took ${Math.round(entry.duration)}ms`
          )
        }
      }
    })
    resourceObserver.observe({ entryTypes: ['resource'] })
  }
}

/**
 * 测量 API 请求性能
 */
export function measureApiPerformance(apiName, duration) {
  console.log(`[Performance] API ${apiName}: ${Math.round(duration)}ms`)

  // 慢请求警告
  if (duration > 3000) {
    console.warn(`[Performance] Slow API detected: ${apiName} took ${Math.round(duration)}ms`)
  }
}

/**
 * 初始化性能监控
 */
export function initPerformanceMonitor() {
  if (process.env.NODE_ENV === 'development') {
    measureWebVitals()
    measureResourceLoading()
  }
}

/**
 * 长任务监控
 */
export function monitorLongTasks() {
  if ('PerformanceObserver' in window) {
    const longTaskObserver = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        console.warn(
          `[Performance] Long Task detected:`,
          `duration: ${Math.round(entry.duration)}ms`,
          `startTime: ${Math.round(entry.startTime)}ms`
        )
      }
    })
    longTaskObserver.observe({ entryTypes: ['longtask'] })
  }
}

/**
 * 内存使用监控
 */
export function monitorMemoryUsage() {
  if (performance.memory) {
    setInterval(() => {
      const memory = performance.memory
      const usedMB = Math.round(memory.usedJSHeapSize / 1048576)
      const totalMB = Math.round(memory.totalJSHeapSize / 1048576)
      const limitMB = Math.round(memory.jsHeapSizeLimit / 1048576)

      // 内存使用超过 80% 时警告
      if (usedMB / limitMB > 0.8) {
        console.warn(`[Performance] High memory usage: ${usedMB}MB / ${limitMB}MB`)
      }
    }, 30000) // 每 30 秒检查一次
  }
}
