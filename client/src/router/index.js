// This is where URLS are defined and mapped to components
import { createRouter, createWebHistory } from 'vue-router'
import Ping from '../components/Ping.vue'
import StockTracker from '../components/StockTracker.vue'
//import StockTrackerV2 from '../components/StockTrackerV2.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/ping',
      name: 'ping',
      component: Ping
    },
    {
      path: '/',
      name: 'stock tracker',
      component: StockTracker
      //component: StockTrackerV2
    },
  ]
})

export default router