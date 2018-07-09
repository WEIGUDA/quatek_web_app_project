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
} from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

Vue.use(BootstrapVue);

import vueMoment from 'vue-moment';
Vue.use(vueMoment);

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
);
Vue.component('font-awesome-icon', FontAwesomeIcon);

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount('#app');
