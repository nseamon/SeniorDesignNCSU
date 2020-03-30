import { Component, OnInit } from '@angular/core';

import { HttpClient, HttpResponse, HttpErrorResponse } from '@angular/common/http';
import { DataService } from "../data.service";
import { environment } from '../../environments/environment';
import { Router, ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  newUsername: string;
  newPassword: string;
  newEmail: string;
  verifyKey: string;

  username: string;
  password: string;
  tokenString: string;

  loginError: string;
  registerMsg: string;

  // Default URL for EC2 API
  private serverUrl = environment.serverUrl;

  constructor(private http: HttpClient, private dataService: DataService, private router: Router) { }

  ngOnInit() {


  }

  login() {
    this.http.post<any>(this.serverUrl + '/login', { username: this.username, password: this.password }).subscribe(data => {
      console.log(data);
      this.tokenString = data.token;
      // clear the login error message if the user previously triggered it
      this.loginError = undefined;
      // pass the token into the data stream
      this.dataService.updateToken(this.tokenString);
      // if the data was valid then navigate to the input page
      this.router.navigate(['/input']);
    }, (error: HttpErrorResponse) => {
      this.loginError = error.error;
    })
  }

  createAccount() {
    this.http.post<any>(this.serverUrl + '/createAccount', { email: this.newEmail, username: this.newUsername, password: this.newPassword, secret_code: this.verifyKey }).subscribe(res => {
      this.registerMsg = res;
    }, (error: HttpErrorResponse) => {
      this.registerMsg = error.error;
    })
  }
}
