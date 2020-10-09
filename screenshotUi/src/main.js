import ElementUI from "element-ui";
import "element-ui/lib/theme-chalk/index.css";
import Vue from "vue";
import App from "./App";
import "./assets/iconfont/icon.css";
import "./assets/iconfont/iconfont.js";
import router from "./router";

Vue.use(ElementUI);
/* eslint-disable no-new */
// eslint-disable-next-line no-unused-vars
new Vue({
  components: { App },
  router,
  template: "<App/>",
}).$mount("#app");
