import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { DataService } from "../_services/data.service";
import { ApiService } from '../_services/api.service';
import { FormBuilder, FormGroup } from '@angular/forms';
import { HttpClient, HttpHeaders, HttpResponse, HttpEvent, HttpErrorResponse } from '@angular/common/http';

@Component({
  selector: 'app-input',
  templateUrl: './input.component.html',
  styleUrls: ['./input.component.css']
})
export class InputComponent implements OnInit {

  private testData: any;
  private rawInput: string;
  private success: string;
  private error: string;

  // raw data fields from twitter
  private author: string;
  private raw_text: string;
  private source: string;
  private time: string;
  private lat: number;
  private lon: number;
  private url: string;

  private fileToUpload: any;
  private uploadForm: FormGroup;

  constructor(private dataService: DataService, private API: ApiService, private http: HttpClient, private formBuilder: FormBuilder) { 
    
  }

  ngOnInit() {
    this.uploadForm = this.formBuilder.group({
      profile: ['']
    });
   }

  inputData() {
    
    
    /** CSV file there */
    const formData = new FormData();
    formData.append('file', this.uploadForm.get('profile').value);

    if (this.uploadForm.get('profile').value !== "") {
      const httpOptions = {
        headers: new HttpHeaders({
            //'Content-Type':  'multipart/form-data',
            //'token': localStorage.getItem('token')
        })
      };
      httpOptions.headers.append('Content-Type', 'multipart/form-data');
        
      this.http.post<any>("http://localhost:5000/csv", formData, httpOptions).subscribe(
        (res) => {
          this.success = res.message;
          this.error = undefined;
        },
        (err: HttpErrorResponse) => {
          this.error = err.error;
          this.success = undefined;
        }
      );
      return;
    }

    // parse the raw data
    this.parseData(this.rawInput);
    // call the api service
    this.API.processRawData(this.raw_text, this.source, this.time, this.lat, this.lon, this.author, this.url, {})
      .subscribe( res => {
        // Referenced code from https://stackoverflow.com/questions/43394144/angular-2-how-to-access-an-http-response-body
        let resStr = JSON.stringify(res);
        let resJSON = JSON.parse(resStr);
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
      this.url = json.url;
    }
  }

  changeListener(event) {
    
    if (event.target.files.length > 0) {
      const file = event.target.files[0];
      this.uploadForm.get('profile').setValue(file);
    }
     
  }
  onSubmit() {
    const formData = new FormData();
    formData.append('file', this.uploadForm.get('profile').value);

    this.http.post<any>("http://localhost:5000/csv", formData, {}).subscribe(
      (res) => this.success = res.message,
      (err) => this.error = err.message
    );
  }
}
