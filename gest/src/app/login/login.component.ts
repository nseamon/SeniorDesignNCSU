import { Component, OnInit } from '@angular/core';

import { HttpClient, HttpResponse, HttpErrorResponse } from '@angular/common/http';
import { DataService } from "../_services/data.service";
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
  repeatPassword: string;
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
      this.tokenString = data.token;
      // clear the login error message if the user previously triggered it
      this.loginError = undefined;
      // pass the token into the data stream
      this.dataService.updateToken(this.tokenString);
      localStorage.setItem('token', this.tokenString);
      localStorage.setItem('username', this.username);
      // if the data was valid then navigate to the input page
      this.router.navigate(['/input']);
    }, (error: HttpErrorResponse) => {
      this.loginError = error.error;
    })
  }

  createAccount() {
    let err = false;
    if (this.newUsername == "") {
      alert("Missing username");
      err = true;
    }
    if (this.newEmail == "") {
      alert("Missing email");
      err = true;
    }
    if (this.verifyKey == "") {
      alert("Missing verification key");
      err = true;
    }
    if (this.newPassword == "") {
      alert("Missing password");
      err = true;
    }
    if (this.newPassword !== this.repeatPassword) {
      alert("Passwords do not match");
      err = true;
    }
    if (err == false) {
      this.http.post<any>(this.serverUrl + '/createAccount', { email: this.newEmail, username: this.newUsername, password: this.newPassword, secret_code: this.verifyKey }).subscribe(res => {
        alert(res);
      }, (error: HttpErrorResponse) => {
        alert(error.error);
      })
    }
  }

  flipcard() {
    
    var card = document.querySelector('.card');
    card.classList.toggle('is-flipped');
    var front = document.querySelector('.card__face.card__face--front');
    front.classList.toggle('hide');
    //var illustration = document.querySelector('.illustration');
    //illustration.classList.toggle('hidden');
  }

}
