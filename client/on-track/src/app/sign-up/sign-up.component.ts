import { Component, Input } from '@angular/core';
import { ApiService, User } from '../services/api-service/api-service.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.less']
})
export class SignUpComponent {
  constructor(
    private apiService: ApiService,
    private router: Router
    ) {}
  
  user: User = {
    first_name: null,
    last_name: null,
    email: null,
    username: null,
    password: null
  };

  async register() {
    try {
      // TODO - Validate fields
      const result: any = await this.apiService.register(this.user);
      console.log('register compunent' + result);
      this.router.navigate(['/login'])

    } catch(e) {
      console.log(e)

    }
  }

}
