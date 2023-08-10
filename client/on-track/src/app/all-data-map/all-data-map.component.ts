import { Component, ViewChild } from '@angular/core';
import { LatLng} from 'leaflet';
import { ApiService } from '../services/api-service/api-service.service';
import { OsmMapComponent } from '../osm-map/osm-map.component';
import { GeoPoint, GeopointService } from '../services/geopoint-service/geopoint.service';

@Component({
  selector: 'app-all-data-map',
  templateUrl: './all-data-map.component.html',
  styleUrls: ['./all-data-map.component.less']
})
export class AllDataMapComponent {

  constructor(
    private apiService: ApiService,
    private geopointService: GeopointService) {}
  
  @ViewChild('osmAllMapComponent', { static: false }) osmMapComponent!: OsmMapComponent;

  async ngAfterViewInit(): Promise<void> { 
    await this.initMap();
  }

  private async initMap(): Promise<void> {
    try {
      // TODO - add type
      const roads: any[] = []; // await this.apiService.getAllRelations();
      roads.forEach(road => {
        const segment = [road['source_geo_point'], road['target_geo_point']]
        const latLngSegment: LatLng[] = this.geopointService.convertGeoPointsToLatLng(segment);
        this.osmMapComponent.addRouteOnMap(latLngSegment, this.deterministicHexColor(road['color']['color']));
      });
      
      const points: GeoPoint[] = []; //await this.apiService.getAllPoints();
      const latLngTrack: LatLng[] = this.geopointService.convertGeoPointsToLatLng(points);
      this.osmMapComponent.addCircularMarkers(latLngTrack);

    } catch (error) {
      console.log(error);
    }
  }

  private deterministicHexColor(number: number): string {
    const hexColor = '#' + (number / 13).toString().replace('.', '').slice(0, 6)
    return hexColor;
  }

}
