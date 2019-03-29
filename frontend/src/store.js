import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";
const jwtDecode = require("jwt-decode");
import { router } from "./router";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    lastFailedUpload: [],
    jwt_token: localStorage.getItem("jwt_token") || "",
    all_cards: [],
    logs: []
  },

  getters: {
    getLastFailedUpload(state) {
      for (let upload of state.lastFailedUpload) {
        upload[0] = JSON.parse(upload[0]);
      }
      return state.lastFailedUpload;
    },

    // 获取 jwt_token
    get_jwt_token(state) {
      return state.jwt_token;
    },

    // 获取解码后的 jwt_token 信息
    get_jwt_token_decoded(state) {
      if (state.jwt_token) {
        return jwtDecode(state.jwt_token);
      }
      return null;
    },

    // 是否登录
    is_authenticated(state) {
      if (state.jwt_token) {
        return true;
      } else {
        return false;
      }
    },
    // 获取实时 logs
    get_logs(state) {
      return state.logs.slice(0, 100);
    }
  },

  mutations: {
    setLastFailedUpload(state, newFailedUpload) {
      state.lastFailedUpload = newFailedUpload;
    },

    setJwtToken(state, new_token) {
      state.jwt_token = new_token;
      localStorage.setItem("jwt_token", new_token);
    },

    resetJwtToken(state) {
      state.jwt_token = "";
      localStorage.setItem("jwt_token", "");
    },

    // 初始化 jwt_token, 并设定 localStorage 和 axios headers
    set_jwt_token(state, jwt_token) {
      state.jwt_token = jwt_token;
      localStorage.setItem("jwt_token", jwt_token);
      axios.defaults.headers.common["Authorization"] = `Bearer ${jwt_token}`;
    },

    // 根据 jwt_woken, 设定 localStorage 和 axios headers
    set_jwt_token_to_localStorage_and_axios_headers(state) {
      localStorage.setItem("jwt_token", state.jwt_token);
      axios.defaults.headers.common["Authorization"] = `Bearer ${
        state.jwt_token
      }`;
    },

    // 删除 jwt_woken, localStorage 和 axios headers
    delete_jwt_token(state) {
      state.jwt_token = "";
      localStorage.setItem("jwt_token", "");
      delete axios.defaults.headers.common["Authorization"];
    },

    // 将 socketio 发送来的 logs 加到 logs 中:
    unshift_to_logs(state, payload) {
      payload.mc_logs.forEach(log => {
        state.logs.unshift(log);
      });
    }
  },

  actions: {
    // 初始化 jwt_token, 并检测 jwt_token 是否过期
    init_jwt_token({ getters, commit }) {
      let jwt_token_decoded = getters.get_jwt_token_decoded;
      // A 如果 jwt_token 存在
      if (jwt_token_decoded) {
        let jwt_token_exp = new Date(jwt_token_decoded.exp * 1000);
        // a. 如果 jwt_token 过期, 调用 delete_jwt_token 删除 state, localStorage, 和 axios headers 中的 jwt_token:
        if (jwt_token_exp < new Date()) {
          commit("delete_jwt_token");
        }
        // b. 如果没过期, 则调用 set_jwt_token_to_localStorage_and_axios_headers, 根据 jwt_woken, 设定 localStorage 和 axios headers
        else {
          commit("set_jwt_token_to_localStorage_and_axios_headers");
        }
      }
      // B. 如果 jwt_token 不存在, 为确保万一, 删除 localStorage 和 axios header 中的 jwt_token
      else {
        commit("delete_jwt_token");
      }
    },

    // 登录
    login({ commit }, user) {
      return new Promise((resolve, reject) => {
        axios
          .post("/login", user)
          .then(resp => {
            const jwt_token = resp.data.access_token;
            commit("set_jwt_token", jwt_token);
            router.push({ name: "Index" });
            resolve(resp);
          })
          .catch(err => {
            commit("delete_jwt_token");
            reject(err);
          });
      });
    },

    // 注册
    register({ commit }, user) {
      return new Promise((resolve, reject) => {
        axios
          .post("/register", user)
          .then(resp => {
            const jwt_token = resp.data.access_token;
            commit("set_jwt_token", jwt_token);
            router.push({ name: "Index" });
            resolve(resp);
          })
          .catch(err => {
            commit("delete_jwt_token");
            reject(err);
          });
      });
    },

    // 登出
    logout({ commit }) {
      commit("delete_jwt_token");
      router.push({ name: "Index" });
    },

    // socketio event send_all_cards_data_to_frontend_from_tasks
    SOCKETIO_send_all_cards_data_to_frontend_from_tasks({ commit }, message) {
      console.log(
        "got message from send_all_cards_data_to_frontend_from_tasks: ",
        message
      );
      commit("unshift_to_logs", { mc_logs: message });
    }
  }
});
