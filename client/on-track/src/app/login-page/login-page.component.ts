import { Component, OnInit } from '@angular/core';
import { ApiService, UserSession } from '../services/api-service/api-service.service';
import { Router } from '@angular/router';
import { CookieService } from 'ngx-cookie-service';

@Component({
  selector: 'app-login-page',
  templateUrl: './login-page.component.html',
  styleUrls: ['./login-page.component.less']
})
export class LoginPageComponent implements OnInit{
  constructor(
    private apiService: ApiService,
    private router: Router, 
    private cookieService: CookieService
    ) {}
  
  username: string = null;
  password: string = null;

  ngOnInit() {
    // TODO - should be handle in auth guard
    // Validate if user is logged in
    const username: string = this.cookieService.get('username');
    
  }

  async login() {
    try {
      // TODO - Validate fields
      const user: UserSession = await this.apiService.login(this.username, this.password);
      // TODO - add session manager service with RXJS
      this.cookieService.set('username', user.username);
      // this.cookieService.set('user_id', user.user_id);
      this.cookieService.set('token', user.token);
      this.router.navigate(['/track-map']);
    }
    catch (error) {
      console.log(error);
    }
  }

  // TODO - move to service
  async logout() {
    try {
      const isLoggedOut: boolean = await this.apiService.logout();
      this.cookieService.set('token', null)
      this.cookieService.set('username', null)
      if (isLoggedOut) {
        this.router.navigate(['/login'])
      }
    }
    // todo - add typing for the error
    catch(e) {
      console.log(e);
    }
  }

}
