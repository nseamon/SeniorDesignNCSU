
import { environment } from '../environments/environment';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/internal/Observable';
import { ProcessedData } from './processedData';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(
    private http: HttpClient,
  ) { }

  private serverUrl = environment.serverUrl;
  
  getData(): Observable<ProcessedData> {
    // Has not been implemented on front-end yet
    return this.http.get<ProcessedData>(this.serverUrl + '/processedTextEntries');
  }

  // Make HTTP post request to backend API to process raw data
  processRawData(raw_text: string, source: string, time: string, lat: number, lon: number, author: string, options) {
    return this.http.post<ProcessedData>(this.serverUrl + '/instantProcessing', {
      raw_text,
      source,
      time,
      lat,
      lon,
      author
    },
      options
    );
  }

  // Make HTTP get request to backend API to processed data
  getProcessedData(options) {
    return this.http.get<ProcessedData>(this.serverUrl + '/processedTextEntries', options);
  }
}
