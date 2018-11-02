import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    lastFailedUpload: [],
    jwt_token: '',
  },
  getters: {
    getLastFailedUpload(state) {
      for (let upload of state.lastFailedUpload) {
        upload[0] = JSON.parse(upload[0]);
      }
      return state.lastFailedUpload;
    },
    getJwtToken(state) {
      return state.jwt_token;
    },
  },
  mutations: {
    setLastFailedUpload(state, newFailedUpload) {
      state.lastFailedUpload = newFailedUpload;
    },
    setJwtToken(state, new_token) {
      state.jwt_token = new_token;
    },
    resetJwtToken(state) {
      state.jwt_token = '';
    },
  },
  actions: {},
});
