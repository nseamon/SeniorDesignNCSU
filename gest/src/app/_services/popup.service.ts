import { Injectable } from '@angular/core';
import * as L from '../../../leaflet/leaflet.js';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { ApiService } from '../_services/api.service';

@Injectable({
  providedIn: 'root'
})
export class PopupService {

  constructor(private API: ApiService) { 
  }

  /**
   * Creates the pop-up window for a marker and populates it with data
   * @param data to populate the pop-up
   * @param marker binded to this pop-up
   * @param map used to remove markers on dismiss button click
   */
  createThreatPopUp(data: any, marker: L.marker, map: L.map): string {
    // Pop-up object
    var popup = L.popup();
    // Outer-most container
    var content = L.DomUtil.create('div');
    // author
    L.DomUtil.create('div', '', content).innerHTML = 'Author: ' + data.raw.author;
    // text
    L.DomUtil.create('div', '', content).innerHTML = 'Text: ' + data.raw.raw_text;
    // source
    L.DomUtil.create('div', '', content).innerHTML = 'Source: ' + data.raw.source;
    // date
    L.DomUtil.create('div', '', content).innerHTML = 'Date: ' + data.raw.time;
    // If url exists add it to the popup content
    if (data.raw.url) {
      // url
      let url = L.DomUtil.create('a', '', content);
      url.innerHTML = data.raw.url;
      url.setAttribute('href', url.innerHTML);
    }
    // Button row
    var buttons = L.DomUtil.create('div', 'row', content);
    buttons.setAttribute('style', 'padding-top:10px');
    // send email button
    var emailBtn = L.DomUtil.create('button', '', buttons);
    // align the button
    emailBtn.setAttribute('style','margin-left:10px');
    emailBtn.innerHTML = 'Send Alert';
    L.DomEvent.on(emailBtn, 'click', () => {
      this.sendEmail(data);
    });
    // dismiss button
    var dismissBtn = L.DomUtil.create('button', '', buttons);
    dismissBtn.innerHTML = 'Dismiss';
    // align the button
    dismissBtn.setAttribute('style','margin-left:25px');
    L.DomEvent.on(dismissBtn, 'click', () => {
      this.deleteMarker(data.id, marker, map);
    });
    // add all content to the popup
    popup.setContent(content);
    return popup;
  }

  /**
   * Sends an email alert to Merck personnel
   */
  sendEmail(data: any) {
    let result = window.confirm("Send email alert for this sentiment?");
    if (result == true) {
      this.API.sendEmail({}, data).subscribe(res => {
        if (res['message'] == "Email sent") {
          alert("Email has been sent!");
        } else {
          alert("Error while sending email: " + res);
        }
      })
    }
  }

  /**
   * Deletes the marker from the map and removes the processed data from the database
   * @param id of processed data
   * @param marker to be deleted from map
   * @param map removes the marker
   */
  deleteMarker(id: number, marker: L.marker, map: L.map) {
    let result = window.confirm("Are you sure you want to delete this?");
    if (result == true) {
      map.removeLayer(marker);
      this.API.deleteRequest(id, {}).subscribe(res => {
        if (res['message'] == "Success") {
          alert("Marker has been deleted");
        } else {
          alert("Error while deleting marker: " + res);
        }
      });
    }
  }
}
