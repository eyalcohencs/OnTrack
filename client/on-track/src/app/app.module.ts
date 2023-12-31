import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { TrackMapComponent } from './track-map/track-map.component';
import { TrackCreationComponent } from './track-creation/track-creation.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HTTP_INTERCEPTORS, HttpClientModule } from '@angular/common/http';
import { AllDataMapComponent } from './all-data-map/all-data-map.component';
import { OsmMapComponent } from './osm-map/osm-map.component';
import { FileSaverModule } from 'ngx-filesaver';
import { ManagerPageComponent } from './manager-page/manager-page.component';
import { LoginPageComponent } from './login-page/login-page.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { SignUpComponent } from './sign-up/sign-up.component';
import { OnTrackInterceptor } from './on-track.interceptor';
import { LoadingSpinnerComponent } from './widgets/loading-spinner/loading-spinner.component';
import { UsersDetailsComponent } from './manager-page/users-details/users-details.component';
import { FaIconLibrary, FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { faSquare, faSquareCheck} from '@fortawesome/free-regular-svg-icons';
import { ManagerOperationsComponent } from './manager-page/manager-operations/manager-operations.component';
import { PrivacyTermOfUsePageComponent } from './privacy-term-of-use-page/privacy-term-of-use-page.component';
import { SiteNotificationsComponent } from './widgets/site-notifications/site-notifications.component'

@NgModule({
  declarations: [
    AppComponent,
    TrackMapComponent,
    TrackCreationComponent,
    AllDataMapComponent,
    OsmMapComponent,
    ManagerPageComponent,
    LoginPageComponent,
    PageNotFoundComponent,
    SignUpComponent,
    LoadingSpinnerComponent,
    UsersDetailsComponent,
    ManagerOperationsComponent,
    PrivacyTermOfUsePageComponent,
    SiteNotificationsComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    FileSaverModule,
    FontAwesomeModule
  ],
  providers: [{
    provide: HTTP_INTERCEPTORS,
    useClass: OnTrackInterceptor,
    multi: true
  }],
  bootstrap: [AppComponent]
})
export class AppModule { 
  constructor(library: FaIconLibrary) {
    library.addIcons(faSquare, faSquareCheck)
  }
}
