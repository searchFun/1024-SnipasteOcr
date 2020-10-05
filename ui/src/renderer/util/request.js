import axios from "axios";

axios.defaults.baseURL = "http://localhost:5000";
axios.defaults.headers["Content-Type"] = "application/json;charset=UTF-8";
// axios.defaults.withCredentials = true

export default {
  get: (url, params = {}) => {
    return new Promise((resolve, reject) => {
      axios
        .get(url, {
          params: params
        })
        .then((response) => {
          resolve(response.data);
        })
        .catch((err) => {
          reject(err);
        });
    });
  },
  post: (url, data = {}) => {
    return new Promise((resolve, reject) => {
      axios
        .post(url, data)
        .then((response) => {
          resolve(response.data);
        })
        .catch((err) => {
          reject(err);
        });
    });
  },
  del: (url, params = {}) => {
    return new Promise((resolve, reject) => {
      axios
        .delete(url, {
          params: params
        })
        .then((response) => {
          resolve(response.data);
        })
        .catch((err) => {
          reject(err);
        });
    });
  },
  patch: (url, data = {}) => {
    return new Promise((resolve, reject) => {
      axios
        .patch(url, data)
        .then((response) => {
          resolve(response.data);
        })
        .catch((err) => {
          reject(err);
        });
    });
  },
  put: (url, data = {}) => {
    return new Promise((resolve, reject) => {
      axios
        .put(url, data)
        .then((response) => {
          resolve(response.data);
        })
        .catch((err) => {
          reject(err);
        });
    });
  }
};
