import Vue from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import './registerServiceWorker';

import BootstrapVue from 'bootstrap-vue';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';

import { library } from '@fortawesome/fontawesome-svg-core';
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
} from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import vueMoment from 'vue-moment';
import Datetime from 'vue-datetime';
import 'vue-datetime/dist/vue-datetime.css';
import VueResource from 'vue-resource';

Vue.use(BootstrapVue);
Vue.use(vueMoment);
Vue.use(Datetime);
Vue.use(VueResource);
const IP_ADDRESS = location.hostname;
const PORT = '5000';
Vue.http.options.root = `http://${IP_ADDRESS}:${PORT}`;
console.log('backend: ' + `http://${IP_ADDRESS}:${PORT}`);

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
Vue.component('font-awesome-icon', FontAwesomeIcon);

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount('#app');
