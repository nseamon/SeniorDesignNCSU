import { Injectable } from '@angular/core';
import {BehaviorSubject} from 'rxjs/internal/BehaviorSubject';

@Injectable({
  providedIn: 'root'
})
export class DataService {

  // Initial state of BehaviorSubject, an undefined ProcessedData object
  private temp: any;
  // user token for authentication
  private token: string;

  private testData = new BehaviorSubject<any>(this.temp);
  currentTestData = this.testData.asObservable();

  private verifiedToken = new BehaviorSubject<string>("default value");
  validToken = this.verifiedToken.asObservable();

  constructor() { 
  
  }

  changeTestData(data: any) {
    this.testData.next(data);
  }

  updateToken(token: string) {
    this.verifiedToken.next(token);
  }
}
