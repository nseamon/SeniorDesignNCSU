import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { TopBarComponent } from './top-bar/top-bar.component';
import { LoginComponent } from './login/login.component';
import { HomePageComponent } from './home-page/home-page.component';
import { InputComponent } from './input/input.component';
import { FormsModule } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { MapComponent } from './map/map.component';
import { PopupService } from './_services/popup.service';
import { MarkerService } from './_services/marker.service';
import { DataService } from './_services/data.service';
import { ApiService } from './_services/api.service';
import { AuthInterceptor } from './_helpers/auth-interceptor';


@NgModule({
  declarations: [
    AppComponent,
    TopBarComponent,
    LoginComponent,
    HomePageComponent,
    InputComponent,
    MapComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule
  ],
  providers: [
    PopupService,
    MarkerService,
    DataService,
    ApiService,
    { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
