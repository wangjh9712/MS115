<template>
  <el-config-provider :locale="zhCn">
    <el-container class="app-container">
      <el-aside width="240px" class="app-aside">
        <div class="logo">
          <div class="logo-icon">
            <el-icon :size="24"><VideoCamera /></el-icon>
          </div>
          <div class="logo-text">
            <span class="logo-title">MediaSync</span>
            <span class="logo-badge">115</span>
          </div>
        </div>
        <el-menu
          :default-active="activeMenu"
          router
        >
          <el-sub-menu index="/explore">
            <template #title>
              <el-icon><Search /></el-icon>
              <span>探索</span>
            </template>
            <el-menu-item index="/explore/douban">豆瓣榜单</el-menu-item>
            <el-menu-item index="/explore/tmdb">TMDB榜单</el-menu-item>
          </el-sub-menu>
          <el-menu-item index="/subscriptions">
            <el-icon><Star /></el-icon>
            <span>订阅</span>
          </el-menu-item>
          <el-menu-item index="/downloads">
            <el-icon><Download /></el-icon>
            <span>离线下载</span>
          </el-menu-item>
          <el-menu-item index="/logs">
            <el-icon><Document /></el-icon>
            <span>日志</span>
          </el-menu-item>
          <el-menu-item index="/settings">
            <el-icon><Setting /></el-icon>
            <span>设置</span>
          </el-menu-item>
          <el-menu-item index="/scheduler">
            <el-icon><Clock /></el-icon>
            <span>调度中心</span>
          </el-menu-item>
          <el-menu-item index="/workflow">
            <el-icon><Connection /></el-icon>
            <span>工作流</span>
          </el-menu-item>
        </el-menu>
        <div class="aside-footer">
          <div class="version-info">
            <span>v1.0.0</span>
          </div>
        </div>
      </el-aside>
      <el-main class="app-main">
        <router-view v-slot="{ Component }">
          <transition name="page-fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </el-main>
    </el-container>
  </el-config-provider>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'

const route = useRoute()
const activeMenu = computed(() => {
  if (route.path.startsWith('/explore/tmdb')) return '/explore/tmdb'
  if (route.path.startsWith('/explore/douban')) return '/explore/douban'
  return route.path
})
</script>

<style lang="scss">
html, body, #app {
  margin: 0;
  padding: 0;
  height: 100%;
  background: linear-gradient(135deg, #0a0a14 0%, #0f0f1f 50%, #0a0a14 100%);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.app-container {
  height: 100%;
}

.app-aside {
  background: linear-gradient(180deg, rgba(18, 18, 31, 0.95) 0%, rgba(12, 12, 22, 0.98) 100%);
  border-right: 1px solid rgba(255, 255, 255, 0.06);
  display: flex;
  flex-direction: column;
  position: relative;
  
  // 装饰性光效
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 200px;
    background: radial-gradient(ellipse at 50% 0%, rgba(99, 102, 241, 0.08) 0%, transparent 70%);
    pointer-events: none;
  }

  .logo {
    height: 72px;
    display: flex;
    align-items: center;
    padding: 0 20px;
    gap: 12px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    position: relative;
    
    .logo-icon {
      width: 42px;
      height: 42px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
      border-radius: 12px;
      color: #fff;
      box-shadow: 0 4px 12px rgba(99, 102, 241, 0.35);
    }
    
    .logo-text {
      display: flex;
      align-items: baseline;
      gap: 6px;
      
      .logo-title {
        font-size: 20px;
        font-weight: 700;
        background: linear-gradient(135deg, #f0f0f5 0%, #a8a8b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.5px;
      }
      
      .logo-badge {
        font-size: 12px;
        font-weight: 700;
        padding: 2px 6px;
        background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);
        color: #0a0a14;
        border-radius: 4px;
      }
    }
  }

  .el-menu {
    flex: 1;
    border-right: none;
    background: transparent;
    padding: 16px 0;
  }
  
  .aside-footer {
    padding: 16px 20px;
    border-top: 1px solid rgba(255, 255, 255, 0.06);
    
    .version-info {
      display: flex;
      align-items: center;
      justify-content: center;
      
      span {
        font-size: 12px;
        color: #4a4a5a;
        font-weight: 500;
      }
    }
  }
}

.app-main {
  background: linear-gradient(135deg, #0a0a14 0%, #0f0f1f 50%, #0a0a14 100%);
  padding: 24px 32px;
  overflow-y: auto;
  position: relative;
  
  // 背景装饰
  &::before {
    content: '';
    position: fixed;
    top: -50%;
    right: -20%;
    width: 60%;
    height: 100%;
    background: radial-gradient(ellipse, rgba(99, 102, 241, 0.03) 0%, transparent 60%);
    pointer-events: none;
  }
  
  &::after {
    content: '';
    position: fixed;
    bottom: -30%;
    left: -10%;
    width: 50%;
    height: 80%;
    background: radial-gradient(ellipse, rgba(139, 92, 246, 0.03) 0%, transparent 60%);
    pointer-events: none;
  }
}

// 页面切换动画
.page-fade-enter-active,
.page-fade-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}

.page-fade-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.page-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
