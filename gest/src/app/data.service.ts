import { Injectable } from '@angular/core';
import {BehaviorSubject} from 'rxjs/internal/BehaviorSubject';
import { ProcessedData } from './processedData';

@Injectable({
  providedIn: 'root'
})
export class DataService {

  // Initial state of BehaviorSubject, an undefined ProcessedData object
  private temp: ProcessedData;
  // user token for authentication
  private token: string;

  private testData = new BehaviorSubject<ProcessedData>(this.temp);
  currentTestData = this.testData.asObservable();

  private verifiedToken = new BehaviorSubject<string>("default value");
  validToken = this.verifiedToken.asObservable();

  constructor() { 
  
  }

  changeTestData(data: ProcessedData) {
    this.testData.next(data);
  }

  updateToken(token: string) {
    this.verifiedToken.next(token);
  }
}
