import { Component, Input } from '@angular/core';
import { ApiService, AuthenticationResponseCode } from '../services/api-service/api-service.service';
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
  registrationFailedWarningText: string = null;

  registrationForm: FormGroup;
  
  user: User = {
    first_name: null,
    last_name: null,
    email: null,
    username: null,
    password: null
  };

  register() {
    this.registerFailedWarning = false;
    this.setRegistrationWarningText(null);

    this.apiService.register(this.user).subscribe({
      next: (response) => {
        this.redirectToLoginPage();
      },
      error: (error) => {
        this.registerFailedWarning = true;
        this.setRegistrationWarningText(error.error['auth_response_code']);
      }
     }).unsubscribe();
  }

  redirectToLoginPage() {
    this.router.navigate(['/login']);
  }

  private setRegistrationWarningText(responseCode: AuthenticationResponseCode) {
    switch(responseCode) {
      case AuthenticationResponseCode.EMAIL_ALREADY_EXIST:
        this.registrationFailedWarningText = 'email already exists!';
        break;
      case AuthenticationResponseCode.FIRST_LAST_NAME_TOO_SHORT:
        this.registrationFailedWarningText = 'first name or last name are too short'!;
        break;
      case AuthenticationResponseCode.PASSWORD_INVALID:
        this.registrationFailedWarningText = 'invalid password!'
        break;
      case AuthenticationResponseCode.EMAIL_INVALID:
        this.registrationFailedWarningText = 'invalid email!'
        break;
      case AuthenticationResponseCode.USERNAME_ALREADY_EXIST:
        this.registrationFailedWarningText = 'username already exists!'
        break;
      case AuthenticationResponseCode.USERNAME_INVALID:
        this.registrationFailedWarningText = 'invalid username!'
        break;
      case AuthenticationResponseCode.UNKNOWN:
        this.registrationFailedWarningText = 'Oops... there was a problem with the registration, please try again'
        break;
      default:
        this.registrationFailedWarningText = null;
    }

  }

}
