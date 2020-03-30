import { ApiService } from '../api.service';
import { Component, OnInit } from '@angular/core';
import { DataService } from "../data.service";
import { HttpClient, HttpHeaders, HttpResponse } from '@angular/common/http';
import { ProcessedData } from '../processedData';

@Component({
  selector: 'app-home-page',
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.css']
})
export class HomePageComponent implements OnInit {

  testData: ProcessedData;
  storedThreats: Array<ProcessedData>;
  
  // variables for authentication
  token: string;
  headers: HttpHeaders;
  options: any;

  constructor(private dataService: DataService, private API: ApiService, private http: HttpClient) {
  }

  ngOnInit() {
    this.dataService.currentTestData.subscribe(data => this.testData = data)
    this.dataService.validToken.subscribe(data => this.token = data);

    this.headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + this.token
    });

    this.options = { headers: this.headers };
    this.getProcessedEntries();
  }


  getProcessedEntries() {
    this.API.getProcessedData(this.options)
    .subscribe( res => {
      var temp = JSON.parse(JSON.stringify(res));
      this.storedThreats = temp.map(function(a) {return a;});
    });
  }
}
