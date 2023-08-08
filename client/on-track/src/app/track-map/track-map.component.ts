import { Component, ViewChild} from '@angular/core';
import { Marker, LatLng, Polyline} from 'leaflet';
import * as _ from "lodash";
import { ApiService } from '../services/api-service/api-service.service';
import { OsmMapComponent } from '../osm-map/osm-map.component';
import { GeopointService } from '../services/geopoint-service/geopoint.service';


@Component({
  selector: 'app-track-map',
  templateUrl: './track-map.component.html',
  styleUrls: ['./track-map.component.less']
})
export class TrackMapComponent {

  constructor(
    private apiService: ApiService,
    private geopointService: GeopointService) {}

  sourceMarker: Marker;
  targetMarker: Marker;
  routeLine: Polyline;

  sourceLat: number;
  sourceLng: number;
  targetLat: number;
  targetLng: number;

  @ViewChild('osmMapComponent', { static: false }) osmMapComponent!: OsmMapComponent;

  onMapClick(event: any) {
    const latlng: LatLng = event.latlng;
    if (!this.sourceMarker) {
      this.sourceMarker = this.osmMapComponent.addMarker(latlng, 'S');
      this.updateSourcePointInput(this.sourceMarker.getLatLng());
    } else if (!this.targetMarker) {
      this.targetMarker = this.osmMapComponent.addMarker(latlng, 'T');
      this.updateTargetPointInput(this.targetMarker.getLatLng());
    } else {
      this.clearUserSelectionFromMap();
      this.sourceMarker = this.osmMapComponent.addMarker(latlng, 'S');
      this.updateSourcePointInput(this.sourceMarker.getLatLng());
      this.updateTargetPointInput(null);
    }
  }

  private updateSourcePointInput(latlng: LatLng) {
    this.sourceLat = !_.isNull(latlng) ? latlng.lat : null;
    this.sourceLng = !_.isNull(latlng) ? latlng.lng : null;
  }

  private updateTargetPointInput(latlng: LatLng) {
    this.targetLat = !_.isNull(latlng) ? latlng.lat : null;
    this.targetLng = !_.isNull(latlng) ? latlng.lng : null;
  }

  async onComposeTrack() {
    this.osmMapComponent.removeLayersFromMap([this.routeLine]);
    this.routeLine = null;
    if (this.sourceMarker && this.targetMarker) {
      const sourceLatLng: LatLng = this.sourceMarker.getLatLng();
      const targetLatLng: LatLng = this.targetMarker.getLatLng();
      try {
        // TODO - create new type instead of any
        const result: any = await this.apiService.getRoute({
          start_lat: sourceLatLng.lat,
          start_lng: sourceLatLng.lng,
          end_lat: targetLatLng.lat,
          end_lng: targetLatLng.lng,
        });
        const track_points = result['points'];
        const track_roads = result['roads'];
        let latLngTrack: LatLng[] = this.geopointService.convertGeoPointsToLatLng(track_points);
        this.routeLine = this.osmMapComponent.addRouteOnMap(latLngTrack);
      } catch (error) {
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
