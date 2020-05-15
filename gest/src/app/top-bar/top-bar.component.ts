import { Component, OnInit } from '@angular/core';
import { ApiService } from '../_services/api.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-top-bar',
  templateUrl: './top-bar.component.html',
  styleUrls: ['./top-bar.component.css']
})
export class TopBarComponent implements OnInit {

  constructor(private API: ApiService, private router: Router) {
  }

  ngOnInit() {
  }

  /**
   * Navigates to map if user is logged in
   */
  navMap() {
    const username = localStorage.getItem('username');
    const token = localStorage.getItem('token');
    if (username && token) {
      this.router.navigate(['/map'])
    }
  }

  /**
   * Navigates to input page if user is logged in
   */
  navInput() {
    const username = localStorage.getItem('username');
    const token = localStorage.getItem('token');
    if (username && token) {
      this.router.navigate(['/input'])
    }
  }

  /**
   * Navigates to home page if user is logged in
   */
  navHome() {
    const username = localStorage.getItem('username');
    const token = localStorage.getItem('token');
    if (username && token) {
      this.router.navigate(['/home'])
    }
  }

  /**
   * Logs the user out of the system
   */
  logout() {
    const username = localStorage.getItem('username');
    const token = localStorage.getItem('token');
    // user must be logged in already
    if (username && token) {
      this.API.logout(username).subscribe( (res) => {
        if (res == "User successfully logged out") {
          localStorage.removeItem('username');
          localStorage.removeItem('token');
          this.router.navigate(['/login']);
          alert("You have been successfully logged out");
        } else {
          alert(res);
        }
      })
    }
  }
}
