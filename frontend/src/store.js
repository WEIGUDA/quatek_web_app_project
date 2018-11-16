import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    lastFailedUpload: [],
    jwt_token: localStorage.getItem('jwt_token') || '',
  },

  getters: {
    getLastFailedUpload(state) {
      for (let upload of state.lastFailedUpload) {
        upload[0] = JSON.parse(upload[0]);
      }
      return state.lastFailedUpload;
    },

    getJwtToken(state) {
      if (state.jwt_token) {
        let base64Url = state.jwt_token.split('.')[1];
        let base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        let exp_date = new Date(JSON.parse(window.atob(base64)).exp * 1000);
        //如果过期
        if (exp_date < new Date()) {
          state.jwt_token = '';
          localStorage.setItem('jwt_token', '');
        }

        return state.jwt_token;
      }
      return '';
    },
  },

  mutations: {
    setLastFailedUpload(state, newFailedUpload) {
      state.lastFailedUpload = newFailedUpload;
    },

    setJwtToken(state, new_token) {
      state.jwt_token = new_token;
      localStorage.setItem('jwt_token', new_token);
    },

    resetJwtToken(state) {
      state.jwt_token = '';
      localStorage.setItem('jwt_token', '');
    },
  },

  actions: {},
});
