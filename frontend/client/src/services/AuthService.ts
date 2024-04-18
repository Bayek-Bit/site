import $api from '../http';
import { AxiosResponse } from 'axios';
import { AuthResponse } from '../models/response/AuthResponse';

export default class AuthService {
  static async login(email: string, password: string): Promise<AxiosResponse<AuthResponse>> {
    return $api.post<AuthResponse>('/auth/jwt/login', { email, password }); // => username
  }
  static async logout(): Promise<void> {
    return $api.post('/auth/jwt/logout');
  }
}
