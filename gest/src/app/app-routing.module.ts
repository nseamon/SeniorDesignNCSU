import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { HomePageComponent } from './home-page/home-page.component';
import { InputComponent } from './input/input.component';
import { MapComponent } from './map/map.component';


const routes: Routes = [
{ path: '', component: LoginComponent },
{ path: 'login', component: LoginComponent},
{ path: 'input', component: InputComponent},
{ path: 'home', component: HomePageComponent},
{ path: 'map', component: MapComponent}];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
