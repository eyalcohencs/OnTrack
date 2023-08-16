import { Component, OnInit, OnDestroy } from '@angular/core';
import { UserStateService } from './services/user-state-service/user-state.service';
import { Subscription } from 'rxjs';
import { User } from './services/api-service/api-service.service';
import * as _ from 'lodash';
import { AuthenticationService } from './services/authentication-service/authentication.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.less']
})
export class AppComponent implements OnInit, OnDestroy {
  constructor(
    private userStateService: UserStateService,
    private authService: AuthenticationService,
    private router: Router
    ) {}
  
  title = 'on-track';
  
  helloText: string = '';

  private userStateSubscription: Subscription;

  ngOnInit(): void {
    if (this.authService.isLoggedIn()) {  // TODO - make it observable
      this.userStateSubscription = this.userStateService.user$.subscribe(
        (user: User) => {
          if (!_.isNull(user)) {
            this.helloText = 'hello, ' + user.first_name + ' ' + user.last_name;
          }
        });
      this.userStateService.fetchUserData();
    }
    
  }

  async logout(): Promise<void> {
    const isLoggedOut: boolean = await this.authService.logout();
    this.router.navigate(['/login'])
  }

  ngOnDestroy() {
    this.userStateSubscription.unsubscribe();
  }

}
