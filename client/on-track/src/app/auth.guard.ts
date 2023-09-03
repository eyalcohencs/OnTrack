import { Injectable, inject } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivateFn, Router, RouterStateSnapshot } from '@angular/router';
import { AuthenticationService } from './services/authentication-service/authentication.service';
import { UserStateService } from './services/user-state-service/user-state.service';
import { User, UserType } from './services/user-enum';
import * as _ from 'lodash';

export const authGuard: CanActivateFn = (
  route: ActivatedRouteSnapshot,
  state: RouterStateSnapshot
  ) => {
  const authService = inject(AuthenticationService);
  const router = inject(Router);
  
  if (authService.isLoggedIn()) {
    return true;
  } else {
    console.log('You are not logged in!')
    router.navigate(['login']);
    return false;  // TODO - is it necessary?
  }
}

export const loginGuard: CanActivateFn = (
  route: ActivatedRouteSnapshot,
  state: RouterStateSnapshot
  ) => {
  const authService = inject(AuthenticationService);
  const router = inject(Router);
  
  if (authService.isLoggedIn()) {
    console.log('You are already logged in!')
    router.navigate(['track-map']);
    return false; // TODO - is it necessary?
  } else {
    return true;
  }
}

export const managerGuard: CanActivateFn = async (
  route: ActivatedRouteSnapshot,
  state: RouterStateSnapshot
  ) => {
  const authService = inject(AuthenticationService);
  const router = inject(Router);
  const userStateService = inject(UserStateService);
  await userStateService.fetchUserData();
  const user: User = userStateService.getUser();
  if (!_.isNull(user) &&  user.user_type == UserType.SYSTEM) {
    return true;
  } else {
    console.log('You are not allowed to enter this page!');
    router.navigate(['/track-map']);
    return false;
  }
  
}
