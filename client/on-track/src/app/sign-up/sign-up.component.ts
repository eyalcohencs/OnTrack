import { Component, Input } from '@angular/core';
import { ApiService } from '../services/api-service/api-service.service';
import { User } from '../services/user-enum';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';


@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.less']
})
export class SignUpComponent {
  constructor(
    private apiService: ApiService,
    private router: Router,
    private formGroup: FormBuilder
    ) {
        this.registrationForm = this.formGroup.group(
          {
            first_name: ['', [Validators.required, Validators.minLength(1)]],
            last_name: ['', [Validators.required, Validators.minLength(1)]],
            email: ['', [Validators.required, Validators.email, Validators.minLength(1)]],
            username: ['', [Validators.required, Validators.minLength(4), Validators.pattern(/^[a-zA-Z]+$/)]],
            password: ['', [Validators.required, Validators.minLength(4), Validators.pattern(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{4,}$/)]],
          }
        );
    }
  
  registerFailedWarning: boolean = false;

  registrationForm: FormGroup;
  
  user: User = {
    first_name: null,
    last_name: null,
    email: null,
    username: null,
    password: null
  };

  async register() {
    try {
      const result: any = await this.apiService.register(this.user);
      this.router.navigate(['/login'])
    } catch(e) {
      console.log(e)
      this.registerFailedWarning = true;
    }
  }

  redirectToLoginPage() {
    this.router.navigate(['/login']);
  }

}
