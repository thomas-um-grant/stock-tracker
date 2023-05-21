// The app entry point, which loads and initializes Vue along with the root component
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/main.css';

const app = createApp(App)

app.use(router)

app.mount('#app')
