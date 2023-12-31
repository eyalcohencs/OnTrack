import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TrackMapComponent } from './track-map/track-map.component';
import { LoginPageComponent } from './login-page/login-page.component';
import { ManagerPageComponent } from './manager-page/manager-page.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { SignUpComponent } from './sign-up/sign-up.component';
import { authGuard, loginGuard, managerGuard } from './auth.guard';
import { PrivacyTermOfUsePageComponent } from './privacy-term-of-use-page/privacy-term-of-use-page.component';

const routes: Routes = [
  {path: 'track-map', component: TrackMapComponent, canActivate: [authGuard]},
  {path: 'login', component: LoginPageComponent, canActivate: [loginGuard]},
  {path: 'register', component: SignUpComponent, canActivate: [loginGuard]},
  {path: 'manager-page', component: ManagerPageComponent, canActivate: [authGuard, managerGuard]},
  {path: 'privacy-and-terms-of-use', component: PrivacyTermOfUsePageComponent},
  {path: '',   redirectTo: '/track-map', pathMatch: 'full'},
  {path: '**', component: PageNotFoundComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
