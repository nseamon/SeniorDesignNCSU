
import { environment } from '../../environments/environment';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/internal/Observable';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private http: HttpClient) { }

  /** AWS EC2 Server  */
  private serverUrl = environment.serverUrl;

  /**
   * Make HTTP post request to backend API to process raw data
   * @param raw_text input text
   * @param source of threat
   * @param time threat was identified
   * @param lat latitude location of threat
   * @param lon longitude location of threat
   * @param author of threat
   * @param options contains the user session token
   */
  processRawData(raw_text: string, source: string, time: string, lat: number, lon: number, author: string, url: string, options: any) {
    return this.http.post<any>(this.serverUrl + '/instantProcessing', {
      "raw_text": raw_text,
      "source": source,
      "time": time,
      "lat": lat,
      "lon": lon,
      "author": author,
      "url": url
    },
      options
    );
  }

  /**
   * Make HTTP GET request to backend API to processed data
   * @param options contains user session token
   */
  getProcessedData(options: any) {
    return this.http.get<any>(this.serverUrl + '/processedTextEntries', options);
  }

  /**
   * Make HTTP DELETE request to remove the processed entry from the database
   * @param id of the processed entry
   * @param options contains user session token
   */
  deleteRequest(id:number, options: any) {
    return this.http.delete<any>(this.serverUrl + '/deleteProcessedTextEntry?id=' + id, options);
  }

  /**
   * Make HTTP POST request to backend API to logout
   * @param username of the user to log out
   */
  logout(username: string) {
    return this.http.post<any>(this.serverUrl + '/logout', { username });
  }

  /**
   * Sends the email alert to Merck personnel
   * @param options contains user session token
   */

  sendEmail(options: any, data: any) {
    return this.http.post<any>(this.serverUrl + '/email', {
      "raw_text": data.raw.raw_text,
      "author": data.raw.author,
      "source": data.raw.source,
      "time": data.raw.time
    }, options);
  }

  /**
   * Upload csv file for instant processing
   * @param options contains user session token
   * @param body is the csv file
   */
  uploadCSV(options: any, file: any) {
    return this.http.post<any>(this.serverUrl + '/csv', {"file": file}, options);
  }

  getTextEntry(min: number, max: number) {
    return this.http.get<any>(this.serverUrl + "/processedTextEntries?min=" + min + "&max=" + max, {});
  }
}
