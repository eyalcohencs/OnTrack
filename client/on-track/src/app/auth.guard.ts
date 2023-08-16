import { Injectable, inject } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivateFn, Router, RouterStateSnapshot } from '@angular/router';
import { AuthenticationService } from './services/authentication-service/authentication.service';

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
