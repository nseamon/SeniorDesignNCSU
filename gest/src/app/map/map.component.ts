import { Component, AfterViewInit } from '@angular/core';
import * as L from 'leaflet/leaflet';
import { MarkerService } from '../_services/marker.service';

// Some of this functionality was created thanks to help from Chris Engelsma at https://alligator.io/angular/angular-and-leaflet-marker-service/

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.css']
})
export class MapComponent {
  private map: L.map;

  constructor(private markerService: MarkerService) { }

  /**
   * Calls angular after map view is initialized and creates threat markers
   */
  ngAfterViewInit(): void {
    this.initMap();
    this.markerService.makeThreatMarkers(this.map);
  }

  /**
   * Adds tiles to the map
   */
  private initMap(): void {
    this.map = L.map('map', {
      center: [ 0, 0 ],
      zoom: 3
    });
    const tiles = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}', {
      attribution: 'Tiles &copy; Esri &mdash; Source: Esri, DeLorme, NAVTEQ, USGS, Intermap, iPC, NRCAN, Esri Japan, METI, Esri China (Hong Kong), Esri (Thailand), TomTom, 2012'
    });
    
    tiles.addTo(this.map);
  }
}
