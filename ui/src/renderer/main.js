import axios from 'axios'
import Vue from 'vue'
import App from './App'
import './assets/iconfont/icon.css'
import './assets/iconfont/iconfont.js'
import router from './router'
import store from './store'

if (!process.env.IS_WEB) Vue.use(require('vue-electron'))
Vue.http = Vue.prototype.$http = axios
Vue.config.productionTip = false

/* eslint-disable no-new */
// eslint-disable-next-line no-unused-vars
new Vue({
  components: { App },
  router,
  store,
  template: '<App/>'
}).$mount('#app')
