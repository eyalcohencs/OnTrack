import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthenticationService } from '../services/authentication-service/authentication.service';
import { UserStateService } from '../services/user-state-service/user-state.service';
import { Subscription } from 'rxjs';
// import { User } from '../services/api-service/api-service.service';

@Component({
  selector: 'app-login-page',
  templateUrl: './login-page.component.html',
  styleUrls: ['./login-page.component.less']
})
export class LoginPageComponent implements OnInit{
  constructor(
    private router: Router, 
    private authService: AuthenticationService,
    // private userStateService: UserStateService
    ) {}
  
  username: string = null;
  password: string = null;

  // private userStateSubscription: Subscription;

  ngOnInit() {
    // TODO - should be handle in auth guard
    // Validate if user is logged in
    // const username: string = this.cookieService.get('username');
    // this.userStateSubscription = this.userStateService.user$.subscribe(
    //   (user: User) => {

    //   }
    // );
  }

  async login() {
    // TODO - Validate fields this.username and this.password
    const isLoggedIn: boolean = await this.authService.login(this.username, this.password);
    if (isLoggedIn) {
      this.router.navigate(['/track-map']);
    } else {
      // TODO - handle failed login
      console.log('Login failed');
    }
  }

  async logout() {
    const isLoggedOut: boolean = await this.authService.logout();
    if (isLoggedOut) {
      this.router.navigate(['/login'])
    } else {
      // TODO - handle failed login
      console.log('Logout failed');
    }
  }

}
