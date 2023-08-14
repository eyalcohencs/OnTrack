import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TrackMapComponent } from './track-map/track-map.component';
import { LoginPageComponent } from './login-page/login-page.component';
import { ManagerPageComponent } from './manager-page/manager-page.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { SignUpComponent } from './sign-up/sign-up.component';

const routes: Routes = [
  {path: 'track-map', component: TrackMapComponent},
  {path: 'login', component: LoginPageComponent},
  {path: 'register', component: SignUpComponent},
  {path: 'manager-page', component: ManagerPageComponent},
  {path: '',   redirectTo: '/track-map', pathMatch: 'full'},
  {path: '**', component: PageNotFoundComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
