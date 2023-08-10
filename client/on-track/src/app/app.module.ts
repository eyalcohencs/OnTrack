import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { TrackMapComponent } from './track-map/track-map.component';
import { TrackCreationComponent } from './track-creation/track-creation.component';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { AllDataMapComponent } from './all-data-map/all-data-map.component';
import { OsmMapComponent } from './osm-map/osm-map.component';
import { FileSaverModule } from 'ngx-filesaver';
import { ManagerPageComponent } from './manager-page/manager-page.component';
import { LoginPageComponent } from './login-page/login-page.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';


@NgModule({
  declarations: [
    AppComponent,
    TrackMapComponent,
    TrackCreationComponent,
    AllDataMapComponent,
    OsmMapComponent,
    ManagerPageComponent,
    LoginPageComponent,
    PageNotFoundComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule,
    FileSaverModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
