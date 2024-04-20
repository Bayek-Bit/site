import { makeAutoObservable } from 'mobx';
import { IUser } from '../models/IUser';
import AuthService from '../services/AuthService';
import axios from 'axios';
import { AuthResponse } from '../models/response/AuthResponse';
import { API_URL } from '../http';

export default class Store {
  user = {} as IUser;
  isAuth = false;

  constructor() {
    makeAutoObservable(this);
  }

  setAuth(bool: boolean) {
    this.isAuth = bool;
  }

  setUser(user: IUser) {
    this.user = user;
  }

  async login(username: string, password: string) {
    try {
      const res = await AuthService.login(username, password);
      console.log(res);
      // localStorage.setItem('token', res.data.accessToken);
      this.setAuth(true);
      this.setUser(res.data.user);
    } catch (e: any) {
      console.log(e.res?.data?.message);
    }
  }

  async logout() {
    try {
      const res = await AuthService.logout();
      console.log(res);
      // localStorage.removeItem('bonds');
      this.setAuth(false);
      this.setUser({} as IUser);
    } catch (e: any) {
      console.log(e.res?.data?.message);
    }
  }
  async checkAuth() {
    try {
      const res = await axios.get<AuthResponse>(`${API_URL}/refresh`, { withCredentials: true });
      console.log(res);
      // localStorage.setItem('token', res.data.accessToken);
      this.setAuth(true);
      this.setUser(res.data.user);
    } catch (e: any) {
      console.log(e.res?.data?.message);
    }
  }
}
