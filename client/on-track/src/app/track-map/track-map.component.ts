import { Component, ViewChild} from '@angular/core';
import { Marker, LatLng, Polyline} from 'leaflet';
import * as _ from "lodash";
import { ApiService } from '../services/api-service/api-service.service';
import { OsmMapComponent } from '../osm-map/osm-map.component';
import { GeoCalculatedRoute, GeopointService } from '../services/geopoint-service/geopoint.service';
import { LoadingSpinnerService } from '../services/loading-spinner-service/loading-spinner.service';
import { MarkerTypeUrl } from '../services/osm-map-enum';


@Component({
  selector: 'app-track-map',
  templateUrl: './track-map.component.html',
  styleUrls: ['./track-map.component.less']
})
export class TrackMapComponent {

  constructor(
    private apiService: ApiService,
    private geopointService: GeopointService,
    private loadingSpinnerService: LoadingSpinnerService) {}

  sourceMarker: Marker;
  targetMarker: Marker;
  routeLine: Polyline;

  sourceLat: number;
  sourceLng: number;
  targetLat: number;
  targetLng: number;

  // trackColor: string = '#234522';
  // trackColor: string = '#312249';
  trackColor: string = '#EC20F2';

  @ViewChild('osmMapComponent', { static: false }) osmMapComponent!: OsmMapComponent;

  onMapClick(event: any) {
    const latlng: LatLng = event.latlng;
    if (!this.sourceMarker) {
      this.sourceMarker = this.osmMapComponent.addMarker(latlng, MarkerTypeUrl.CAR);
      this.updateSourcePointInput(this.sourceMarker.getLatLng());
    } else if (!this.targetMarker) {
      this.targetMarker = this.osmMapComponent.addMarker(latlng, MarkerTypeUrl.ROAD);
      this.updateTargetPointInput(this.targetMarker.getLatLng());
    } else {
      this.clearUserSelectionFromMap();
      this.sourceMarker = this.osmMapComponent.addMarker(latlng,  MarkerTypeUrl.CAR);
      this.updateSourcePointInput(this.sourceMarker.getLatLng());
      this.updateTargetPointInput(null);
    }
  }

  private updateSourcePointInput(latlng: LatLng) {
    this.sourceLat = !_.isNull(latlng) ? Number(latlng.lat.toFixed(3)) : null;
    this.sourceLng = !_.isNull(latlng) ? Number(latlng.lng.toFixed(3)) : null;
  }

  private updateTargetPointInput(latlng: LatLng) {
    this.targetLat = !_.isNull(latlng) ? Number(latlng.lat.toFixed(3)) : null;
    this.targetLng = !_.isNull(latlng) ? Number(latlng.lng.toFixed(3)) : null;
  }

  async onComposeTrack() {
    this.loadingSpinnerService.show();

    this.osmMapComponent.removeLayersFromMap([this.routeLine]);
    this.routeLine = null;
    if (this.sourceMarker && this.targetMarker) {
      const sourceLatLng: LatLng = this.sourceMarker.getLatLng();
      const targetLatLng: LatLng = this.targetMarker.getLatLng();
      try {
        const result: GeoCalculatedRoute = await this.apiService.getRoute({
          start_lat: sourceLatLng.lat,
          start_lng: sourceLatLng.lng,
          end_lat: targetLatLng.lat,
          end_lng: targetLatLng.lng,
        });
        const track_points = result['points'];
        const track_roads = result['roads'];
        let latLngTrack: LatLng[] = this.geopointService.convertGeoPointsToLatLng(track_points);
        this.routeLine = this.osmMapComponent.addRouteOnMap(latLngTrack, this.trackColor);
        this.loadingSpinnerService.hide();
      } catch (error) {
        this.loadingSpinnerService.hide();
        console.log(error);
      }
    }
  }

  onClearAll() {
    this.osmMapComponent.clearAll();
    this.clearMarkersData();
    this.updateSourcePointInput(null)
    this.updateTargetPointInput(null)
  }

  private clearMarkersData() {
    this.sourceMarker = this.targetMarker = null;
    this.routeLine = null;
  }

  private clearUserSelectionFromMap() {
    this.osmMapComponent.removeLayersFromMap([this.sourceMarker, this.targetMarker]);
    this.clearMarkersData()
  }

}
