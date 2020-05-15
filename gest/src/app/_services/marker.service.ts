import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { DataService } from "../_services/data.service";
import { ApiService } from '../_services/api.service';
import * as L from 'leaflet/leaflet';
import { PopupService } from './popup.service';
import * as Cluster from 'dist/leaflet.markercluster.js'


@Injectable({
  providedIn: 'root'
})
export class MarkerService {

  private storedThreats: Array<any>;

  constructor(private http: HttpClient, private API: ApiService, private dataService: DataService, private popupService: PopupService) {
  }

  /**
   * Creates threat markers on the given map
   * @param map to add markers to
   */
  makeThreatMarkers(map: L.map): void {
    var markers = new Cluster.MarkerClusterGroup();
    this.API.getProcessedData({}).subscribe((res: any) => {
      var temp = JSON.parse(JSON.stringify(res));
      this.storedThreats = temp.map(function(a) {return a;});
      for (const data of this.storedThreats) {
        const lat = data.raw.lat;
        const lon = data.raw.lon;
        var marker = L.marker([lat, lon]);
        marker.bindPopup(this.popupService.createThreatPopUp(data, marker, map));
        // add to marker cluster
        markers.addLayer(marker);
      }
    });
    map.addLayer(markers);
  }
}
