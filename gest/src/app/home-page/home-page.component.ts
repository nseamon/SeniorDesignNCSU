import { ApiService } from '../_services/api.service';
import { Component, OnInit } from '@angular/core';
import { DataService } from "../_services/data.service";
import { HttpClient, HttpHeaders, HttpResponse } from '@angular/common/http';

@Component({
  selector: 'app-home-page',
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.css']
})
export class HomePageComponent implements OnInit {

  private testData: any;
  private storedThreats: Array<any>;
  
  constructor(private dataService: DataService, private API: ApiService, private http: HttpClient) {
  }

  ngOnInit() {
    this.dataService.currentTestData.subscribe(data => this.testData = data)
    this.getProcessedEntries();
  }


  getProcessedEntries() {
    this.API.getProcessedData({})
    .subscribe( res => {
      var temp = JSON.parse(JSON.stringify(res));
      this.storedThreats = temp.map(function(a) {return a;});
    });
  }

  deleteEntry(event) {
    var target = event.target || event.srcElement || event.currentTarget;
    var idAttr = target.attributes.id;
    var value = idAttr.nodeValue;
    let result = window.confirm("Do you want to delete this?");
    if (result == true) {
        this.API.deleteRequest(value, {})
      .subscribe(res => {
        if (res['message'] == "Success") {
          alert("Card has been deleted");
        } else {
          alert("Error deleting card");
        }
      });
      var myobj = document.getElementById('card-' + value);
      myobj.remove();
    }
  }

  sendEmail(event) {
    var target = event.target || event.srcElement || event.currentTarget;
    var idAttr = target.attributes.id;
    var value = idAttr.nodeValue;
    this.API.getTextEntry(value, value).subscribe( (res) => {
      this.API.sendEmail({}, res[0]).subscribe( (response) => {
        if (response['message'] == "Email sent") {
          alert("Email has been sent!");
        } else {
          alert("Error while sending email: " + response);
        }
      });
    });
  }
}
