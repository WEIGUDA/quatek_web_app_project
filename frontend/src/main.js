import Vue from "vue";
import App from "./App.vue";
import { router } from "./router";
import store from "./store";
import "./registerServiceWorker";

import BootstrapVue from "bootstrap-vue";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";

import { library } from "@fortawesome/fontawesome-svg-core";
import {
  faCircle,
  faShoePrints,
  faHandPaper,
  faUpload,
  faDownload,
  faUserPlus,
  faTrashAlt,
  faPencilAlt,
  faCaretSquareLeft,
  faCaretSquareRight,
  faSearch,
  faEnvelope,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import vueMoment from "vue-moment";
import Datetime from "vue-datetime";
import "vue-datetime/dist/vue-datetime.css";
import axios from "axios";
import { IP_ADDRESS, PORT } from "@/config";
import Vuetify from "vuetify";
// import 'vuetify/dist/vuetify.min.css';
import "material-design-icons-iconfont/dist/material-design-icons.css";
import "@mdi/font/css/materialdesignicons.css";
import WebFontLoader from "webfontloader";
import VueSocketIO from "vue-socket.io";

Vue.use(BootstrapVue);
Vue.use(vueMoment);
Vue.use(Datetime);
Vue.use(Vuetify, {
  iconfont: "mdi", // 'md' || 'mdi' || 'fa' || 'fa4'
});

axios.defaults.baseURL = `http://${IP_ADDRESS}:${PORT}`;
console.log("backend: " + `http://${IP_ADDRESS}:${PORT}`);

// const jwt = localStorage.getItem('jwt');
// Vue.http.headers.common['Authorization'] = `Bear ${jwt}`;

library.add(
  faCircle,
  faShoePrints,
  faHandPaper,
  faUpload,
  faDownload,
  faUserPlus,
  faPencilAlt,
  faTrashAlt,
  faCaretSquareLeft,
  faCaretSquareRight,
  faSearch,
  faEnvelope,
);

Vue.component("font-awesome-icon", FontAwesomeIcon);

Vue.config.productionTip = false;

Vue.use(
  new VueSocketIO({
    // debug: process.env.NODE_ENV === "production" ? false : true,
    debug: true,
    connection: `http://${IP_ADDRESS}:${PORT}`,
    vuex: {
      store,
      actionPrefix: "SOCKETIO_",
      mutationPrefix: "SOCKETIO_",
    },
  }),
);

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount("#app");
