import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    lastFailedUpload: [],
  },
  getters: {
    getLastFailedUpload(state) {
      for (let upload of state.lastFailedUpload) {
        upload[0] = JSON.parse(upload[0]);
      }
      return state.lastFailedUpload;
    },
  },
  mutations: {
    setLastFailedUpload(state, newFailedUpload) {
      state.lastFailedUpload = newFailedUpload;
    },
  },
  actions: {},
});
