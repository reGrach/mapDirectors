import Axios from 'axios';
import Vue from 'vue';

Axios.defaults.baseURL = 'http://localhost:8888';
Axios.defaults.headers.common.Accept = 'application/json';
Axios.interceptors.response.use(
  response => response,
  (error) => {
    return Promise.reject(error);
  });

// Bind Axios to Vue.
Vue.$http = Axios;
Object.defineProperty(Vue.prototype, '$http', {
  get() {
    return Axios;
  },
});
