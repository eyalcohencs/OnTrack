import { Injectable } from '@angular/core';
import jwt_decode, { JwtPayload } from "jwt-decode";
import { CookieService } from 'ngx-cookie-service';
import { ApiService, UserSession } from '../api-service/api-service.service';
import { UserStateService } from '../user-state-service/user-state.service';
import { firstValueFrom } from 'rxjs';

/**
 * The service handles user authentication.
 * It provides methods for logging in, logging out and user status.
 */
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
  /**
   * Log in user based on his provided username and password.
   * @param username - The user's username.
   * @param password - The user's password.
   * @returns true if loggin succeded and false otherwise.
   */
  async login(username: string, password: string): Promise<boolean> {
    try {
      const userSession: UserSession = await this.apiService.login(username, password);
      // TODO - should I need to add session manager state service with RXJS?
      this.cookieService.set('username', userSession.username);
      this.cookieService.set('token', userSession.token);
      this.userStateService.setUser(userSession.user);
      return true;
    } catch(e) {
      console.log('Error while login: ' + e);
      return false;
    }
  }

  /**
   * Log out the user, remove the session tokens from the cockie.
   */
  async logout(): Promise<void> {
    try {
      await firstValueFrom(this.apiService.logout());
      this.cookieService.deleteAll();
      this.userStateService.setUser(null);
    } catch(e) {
      console.log('Error while logout: ' + e);
      throw e;
    }
  }

}
