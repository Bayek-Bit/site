import $api from '../http';
import { AxiosResponse } from 'axios';
import { AuthResponse } from '../models/response/AuthResponse';

export default class AuthService {
  static async login(username: string, password: string): Promise<AxiosResponse<AuthResponse>> {
    const queryString = `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`;
    return $api.post<AuthResponse>('/auth/jwt/login', queryString, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      }
    });
  }
  static async logout(): Promise<void> {
    return $api.post('/auth/jwt/logout');
  }
}
