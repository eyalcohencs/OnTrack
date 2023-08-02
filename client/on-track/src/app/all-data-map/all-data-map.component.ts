import { Component } from '@angular/core';
import { Map, map, tileLayer, Marker, LatLng, Polyline, LatLngExpression, Icon, circleMarker} from 'leaflet';
import { ApiService, GeoPoint } from '../services/api-service/api-service.service';

// TODO - need to create MapComponent that component wil herit from it or composition
@Component({
  selector: 'app-all-data-map',
  templateUrl: './all-data-map.component.html',
  styleUrls: ['./all-data-map.component.less']
})
export class AllDataMapComponent {
  map: Map;
  routeLine: Polyline;

  constructor(private apiService: ApiService) {}

  async ngAfterViewInit(): Promise<void> { 
    await this.initMap();
  }

  private async initMap(): Promise<void> {
    this.map = map('all-data-map', {
      center: [ 32.0000, 35.0000 ],
      zoom: 9
    });
    const tiles = tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18,
      minZoom: 3,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    });

    tiles.addTo(this.map);

    try {
      const track = await this.apiService.getAllPoints();
      let latLngTrack: LatLng[] = this.convertGeoPointsToLatLng(track);
      // this.displayRouteOnMap(latLngTrack);
      const circuleMarkerOptions = {radius: 4};
      latLngTrack.forEach((latLng: LatLng) => {
        const marker = circleMarker(latLng, circuleMarkerOptions).addTo(this.map);
        marker.bindPopup(marker.getLatLng().toString()).openPopup();
      }); 
    } catch (error) {
      console.log(error);
    }

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


  displayRouteOnMap(coordinates: LatLngExpression[]) {
    if (this.routeLine) {
      this.map.removeLayer(this.routeLine);
    }

    this.routeLine = new Polyline(coordinates, {
      color: 'blue',
      weight: 5
    }).addTo(this.map);
  }

  private convertGeoPointsToLatLng(track: GeoPoint[]): LatLng[] {
      return track.map((geoPoint: GeoPoint) => new LatLng(geoPoint.latitude, geoPoint.longitude, geoPoint.altitude));
  }

}
