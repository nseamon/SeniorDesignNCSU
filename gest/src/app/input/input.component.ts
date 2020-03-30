import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { DataService } from "../data.service";
import { FormsModule } from '@angular/forms';
import { ApiService } from '../api.service';
import { ProcessedData } from '../processedData';
import { HttpClient, HttpHeaders, HttpResponse, HttpEvent, HttpErrorResponse } from '@angular/common/http';

@Component({
  selector: 'app-input',
  templateUrl: './input.component.html',
  styleUrls: ['./input.component.css']
})
export class InputComponent implements OnInit {

  testData: ProcessedData;
  rawInput: string;
  success: string;
  error: string;

  // raw data fields from twitter
  author: string;
  raw_text: string;
  source: string;
  time: string;
  lat: number;
  lon: number;

  // variables for authentication
  token: string;
  headers: HttpHeaders;
  options: any;

  constructor(private dataService: DataService, private API: ApiService, private http: HttpClient) { 
    
  }

  ngOnInit() {
    this.dataService.currentTestData.subscribe(data => this.testData = data);
    this.dataService.validToken.subscribe(data => this.token = data);
    console.log(this.token);
    this.headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + this.token
    });
    this.options = { headers: this.headers };
  }

  inputData() {
    // parse the raw data
    this.parseData(this.rawInput);
    // call the api service
    this.API.processRawData(this.raw_text, this.source, this.time, this.lat, this.lon, this.author, this.options)
      .subscribe( res => {
        // Referenced code from https://stackoverflow.com/questions/43394144/angular-2-how-to-access-an-http-response-body
        let resStr = JSON.stringify(res);
        let resJSON : ProcessedData = JSON.parse(resStr);
        this.dataService.changeTestData(resJSON);
        // set the response message
        this.error = undefined;
        if ('message' in res ){
          this.success = res['message'];
        } else {
          this.success = "Threatening sentiment in range of a Merck facility"
        }
        
      }, (error: HttpErrorResponse) => {
        this.success = undefined
        this.error = error.error;
      });
  }

  parseData(data: string) {
    if (data !== undefined) {
      const json = JSON.parse(data);
      this.author = json.author;
      this.raw_text = json.raw_text;
      this.source = json.source;
      this.time = json.time;
      this.lat = json.lat;
      this.lon = json.lon;
      // add source link here eventually
    }
  }
}
