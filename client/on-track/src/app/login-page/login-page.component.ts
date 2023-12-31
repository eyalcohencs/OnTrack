import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthenticationService } from '../services/authentication-service/authentication.service';

/**
 * This components present the user loging page.
 */
@Component({
  selector: 'app-login-page',
  templateUrl: './login-page.component.html',
  styleUrls: ['./login-page.component.less']
})
export class LoginPageComponent {
  
  constructor(
    private router: Router, 
    private authService: AuthenticationService,
    ) {}
  
  username: string = null;
  password: string = null;

  loginFailedWarning: boolean = false;

  async login() {
    const isLoggedIn: boolean = await this.authService.login(this.username, this.password);
    if (isLoggedIn) {
      this.router.navigate(['/track-map']);
    } else {
      this.loginFailedWarning = true;
    }
  }
}
