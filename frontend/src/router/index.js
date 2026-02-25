import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    redirect: '/explore/douban'
  },
  {
    path: '/search',
    redirect: '/explore/douban'
  },
  {
    path: '/explore/:source(douban|tmdb)',
    name: 'Search',
    component: () => import('@/views/Search.vue')
  },
  {
    path: '/explore/section/:key',
    redirect: to => `/explore/douban/section/${encodeURIComponent(to.params.key)}`
  },
  {
    path: '/explore/:source(douban|tmdb)/section/:key',
    name: 'ExploreSection',
    component: () => import('@/views/ExploreSection.vue')
  },
  {
    path: '/subscriptions',
    name: 'Subscriptions',
    component: () => import('@/views/Subscriptions.vue')
  },
  {
    path: '/downloads',
    name: 'Downloads',
    component: () => import('@/views/Downloads.vue')
  },
  {
    path: '/subscription-logs',
    redirect: '/logs'
  },
  {
    path: '/logs',
    name: 'Logs',
    component: () => import('@/views/Logs.vue')
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('@/views/Settings.vue')
  },
  {
    path: '/scheduler',
    name: 'Scheduler',
    component: () => import('@/views/Scheduler.vue')
  },
  {
    path: '/workflow',
    name: 'Workflow',
    component: () => import('@/views/Workflow.vue')
  },
  {
    path: '/movie/:id',
    name: 'MovieDetail',
    component: () => import('@/views/MovieDetail.vue')
  },
  {
    path: '/tv/:id',
    name: 'TvDetail',
    component: () => import('@/views/TvDetail.vue')
  },
  {
    path: '/douban/:mediaType(movie|tv)/:id',
    name: 'DoubanDetail',
    component: () => import('@/views/DoubanDetail.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
