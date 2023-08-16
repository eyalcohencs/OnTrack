import { Injectable } from '@angular/core';
import jwt_decode, { JwtPayload } from "jwt-decode";
import { CookieService } from 'ngx-cookie-service';

@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {

  constructor(private cookieService: CookieService) { }

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

}
