import { Component, ViewChild } from '@angular/core';
import { LatLng} from 'leaflet';
import { ApiService } from '../services/api-service/api-service.service';
import { OsmMapComponent } from '../osm-map/osm-map.component';
import { GeoPoint, GeoRoad, GeopointService } from '../services/geopoint-service/geopoint.service';
import { LoadingSpinnerService } from '../services/loading-spinner-service/loading-spinner.service';

// TODO - change name to manager-map
@Component({
  selector: 'app-all-data-map',
  templateUrl: './all-data-map.component.html',
  styleUrls: ['./all-data-map.component.less']
})
export class AllDataMapComponent {

  constructor(
    private apiService: ApiService,
    private geopointService: GeopointService,
    private loadingSpinnerService: LoadingSpinnerService) {}
  
  @ViewChild('osmAllMapComponent', { static: false }) osmMapComponent!: OsmMapComponent;

  // async ngAfterViewInit(): Promise<void> { 
  //   await this.initMap();
  // }

  private async initMap(): Promise<void> {
    try {
      this.loadingSpinnerService.show();
      const roads: GeoRoad[] = await this.apiService.getAllRelations();
      roads.forEach(road => {
        const segment = [road['source_geo_point'], road['target_geo_point']]
        const latLngSegment: LatLng[] = this.geopointService.convertGeoPointsToLatLng(segment);
        this.osmMapComponent.addRouteOnMap(latLngSegment, this.deterministicHexColor(road['track_id'].replace(/\D/g, '')), 6);
      });

      const points: GeoPoint[] = []; //await this.apiService.getAllPoints();
      const latLngTrack: LatLng[] = this.geopointService.convertGeoPointsToLatLng(points);
      this.osmMapComponent.addCircularMarkers(latLngTrack);

      this.loadingSpinnerService.hide();

    } catch (error) {
      this.loadingSpinnerService.hide();
      console.log(error);
    }
  }

  async loadAllTracks() {
    await this.initMap();
  }

  async loadAllPoints() {
    try {
      this.loadingSpinnerService.show();
      const points: GeoPoint[] = await this.apiService.getAllPoints();
      const latLngTrack: LatLng[] = this.geopointService.convertGeoPointsToLatLng(points);
      this.osmMapComponent.addCircularMarkers(latLngTrack);
      this.loadingSpinnerService.hide();
    } catch (error) {
      this.loadingSpinnerService.hide();
      console.log(error);
    }


  }

  private deterministicHexColor(base_number: string): string {
    const hexColor = '#' + (base_number).slice(0, 6)
    return hexColor;
  }

}
