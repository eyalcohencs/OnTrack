import { Component } from '@angular/core';
import { ApiService, UserSession } from '../services/api-service/api-service.service';
import { Route, Router } from '@angular/router';

@Component({
  selector: 'app-login-page',
  templateUrl: './login-page.component.html',
  styleUrls: ['./login-page.component.less']
})
export class LoginPageComponent {
  constructor(
    private apiService: ApiService,
    private router: Router
    ) {}
  
  username: string = null;
  password: string = null;

  async login() {
    try {
      // TODO - Validate fields
      const user: UserSession = await this.apiService.login(this.username, this.password);
      // TODO - add session manager service with RXJS
      localStorage.setItem('token', user.token);
      console.log('user is login ' + user);
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
