import axios from 'axios';

export const API_URL = `http://127.0.0.1:8000`;

const $api = axios.create({
  withCredentials: true,
  baseURL: API_URL,
});

$api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    document.cookie = `token=${token}`;
  }
  return config;
});

export default $api;