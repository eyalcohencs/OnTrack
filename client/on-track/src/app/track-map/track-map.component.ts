import { Component, OnInit, AfterViewInit} from '@angular/core';
import { Map, map, tileLayer, Marker, LatLng, Polyline, LatLngExpression, Icon} from 'leaflet';
import * as _ from "lodash";
import { ApiService, GeoPoint } from '../services/api-service/api-service.service';


@Component({
  selector: 'app-track-map',
  templateUrl: './track-map.component.html',
  styleUrls: ['./track-map.component.less']
})
export class TrackMapComponent implements OnInit {
  map: Map;
  sourceMarker: Marker | null;
  targetMarker: Marker | null;
  routeLine: Polyline;

  sourceLat: number;
  sourceLng: number;
  targetLat: number;
  targetLng: number;

  constructor(private apiService: ApiService) {}

  ngOnInit() {}

  ngAfterViewInit(): void { 
    this.initMap();
    this.map.on('click', (event) => this.onMapClick(event));
  }

  private initMap(): void {
    this.map = map('map', {
      center: [ 32.0000, 35.0000 ],
      zoom: 9
    });
    const tiles = tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18,
      minZoom: 3,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    });

    tiles.addTo(this.map);

  }

  onMapClick(event: any) {
    const latlng: LatLng = event.latlng;

    if (!this.sourceMarker) {
      this.sourceMarker = this.addMarker(latlng, 'S');
      this.updateSourcePointInput(this.sourceMarker.getLatLng());
    } else if (!this.targetMarker) {
      this.targetMarker = this.addMarker(latlng, 'T');
      this.updateTargetPointInput(this.sourceMarker.getLatLng());
    } else {
      this.clearMapData();
      this.sourceMarker = this.addMarker(latlng, 'S');
      this.updateSourcePointInput(this.sourceMarker.getLatLng());
      this.updateTargetPointInput(null);

    }
  }

  updateSourcePointInput(latlng: LatLng) {
    this.sourceLat = latlng.lat;
    this.sourceLng = latlng.lng;
  }

  updateTargetPointInput(latlng: LatLng) {
    this.targetLat = !_.isNull(latlng) ? latlng.lat : null;
    this.targetLng = !_.isNull(latlng) ? latlng.lng : null;
  }


  addMarker(latlng: LatLngExpression, label: string): Marker {
    const customIcon: Icon = new Icon({
      iconUrl: 'assets/marker-icon.png',
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34]
    });

    const marker: Marker = new Marker(latlng, { icon: customIcon }).addTo(this.map);
    marker.bindPopup(label).openPopup();

    return marker;
  }

  async onComposeTrack() {
    if (this.sourceMarker && this.targetMarker) {
      const sourceLatLng: LatLng = this.sourceMarker.getLatLng();
      const targetLatLng: LatLng = this.targetMarker.getLatLng();
      try {
        const track = await this.apiService.getRoute({
          start_lat: sourceLatLng.lat,
          start_lng: sourceLatLng.lng,
          end_lat: targetLatLng.lat,
          end_lng: targetLatLng.lng,
        });
        let latLngTrack: LatLng[] = this.convertGeoPointsToLatLng(track);
        this.displayRouteOnMap(latLngTrack);
      } catch (error) {
        console.log(error);
      }
    }
  }

  private convertGeoPointsToLatLng(track: GeoPoint[]): LatLng[] {
      return track.map((geoPoint: GeoPoint) => new LatLng(geoPoint.latitude, geoPoint.longitude, geoPoint.altitude));
  }

  displayRouteOnMap(coordinates: LatLngExpression[]) {
    if (this.routeLine) {
      this.map.removeLayer(this.routeLine);
    }

    this.routeLine = new Polyline(coordinates, {
      color: 'blue',
      weight: 5
    }).addTo(this.map);
  }

  onClearAll() {
    this.clearMapData();
    this.map.removeLayer(this.routeLine);
  }

  clearMapData() {
    if (this.sourceMarker) {
      this.map.removeLayer(this.sourceMarker);
      this.sourceMarker = null;
    }

    if (this.targetMarker) {
      this.map.removeLayer(this.targetMarker);
      this.targetMarker = null;
    }
  }
}
