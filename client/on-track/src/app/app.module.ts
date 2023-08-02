import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { TrackMapComponent } from './track-map/track-map.component';
import { TrackCreationComponent } from './track-creation/track-creation.component';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { AllDataMapComponent } from './all-data-map/all-data-map.component';

@NgModule({
  declarations: [
    AppComponent,
    TrackMapComponent,
    TrackCreationComponent,
    AllDataMapComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
