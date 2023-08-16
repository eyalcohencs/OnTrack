import { Injectable } from '@angular/core';
import jwt_decode, { JwtPayload } from "jwt-decode";
import { CookieService } from 'ngx-cookie-service';
import { ApiService, UserSession } from '../api-service/api-service.service';
import { UserStateService } from '../user-state-service/user-state.service';

@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {

  constructor(
    private apiService: ApiService,
    private cookieService: CookieService,
    private userStateService: UserStateService) { }

  isLoggedIn(): boolean {
    const token = this.cookieService.get('token');
    if (token) {
      const tokenData: JwtPayload = jwt_decode(token);
      const now = new Date(Date.now())
      const expirationDate = new Date(tokenData.exp * 1000);
      return expirationDate > now;
    }
    return false;
  }

  // TODO - handle errors and typing
  async login(username: string, password: string): Promise<boolean> {
    try {
      const userSession: UserSession = await this.apiService.login(username, password);
      // TODO - should I need to add session manager state service with RXJS
      this.cookieService.set('username', userSession.username);
      this.cookieService.set('token', userSession.token);
      this.userStateService.setUser(userSession.user);
      return true;
    } catch(e) {
      return false;
    }
  }

  // TODO - handle errors and typing
  async logout(): Promise<boolean> {
    try {
      const result: {is_logged_out: boolean} = await this.apiService.logout();
      if (result.is_logged_out) {
        this.cookieService.deleteAll();
        this.userStateService.setUser(null);
        return true;
      } else {
        return false;
      }
    } catch(e) {
      return false;
    }

  }

}