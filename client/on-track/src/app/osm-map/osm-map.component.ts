import { Component, OnInit, AfterViewInit, Input, Output, EventEmitter, ElementRef, Renderer2 } from '@angular/core';
import { Map, map, tileLayer, Marker, Polyline, LatLngExpression, Icon, Layer, LatLngTuple, CircleMarkerOptions, LatLng, circleMarker, CircleMarker, PointTuple} from 'leaflet';

import * as _ from "lodash";
import { MarkerTypeUrl, OSMTilesTemplate } from '../services/osm-map-enum';

@Component({
  selector: 'app-osm-map',
  templateUrl: './osm-map.component.html',
  styleUrls: ['./osm-map.component.less']
})
export class OsmMapComponent implements OnInit, AfterViewInit {

  constructor(private elRef: ElementRef, private renderer: Renderer2) {}
  static readonly OPEN_STREET_MAP_TILES: string = OSMTilesTemplate.ISRAEL_HIKING_HEBREW;
  static readonly ISRAEL_CENTER: LatLngTuple = [ 32.6000, 35.0000 ];
  static readonly MAP_ZOOM: number = 13;
  static readonly CIRCULAR_MARKER_CONFIG: CircleMarkerOptions = {radius: 4};
  
  @Input() mapId: string;
  @Input() mapCenter: LatLngTuple = OsmMapComponent.ISRAEL_CENTER;
  @Input() zoom: number = OsmMapComponent.MAP_ZOOM;
  
  @Output() clickOnMap = new EventEmitter<any>();
  
  map: Map;
  addedLayers: Layer[] = [];

  ngOnInit(): void {
    this.createDivElement(this.mapId)
  }

  ngAfterViewInit(): void { 
    this.initMap();
    this.map.on('click', (event) => this.onMapClick(event));
  }

  private initMap(): void {
    this.map = map(this.mapId, {
      center: this.mapCenter,
      zoom: this.zoom
    });
    const tiles = tileLayer(OsmMapComponent.OPEN_STREET_MAP_TILES, {
      maxZoom: 16,
      minZoom: 7,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    });

    tiles.addTo(this.map);

    navigator.geolocation.getCurrentPosition((position) => {
      const userMarker: Marker = this.addMarker([position.coords.latitude, position.coords.longitude], MarkerTypeUrl.USER, null, [41, 41])
      this.map.panTo(userMarker.getLatLng());
    });
  }

  private onMapClick(event: any) {
      this.clickOnMap.emit(event);
  }

  addMarker(latlng: LatLngExpression, markerTypeUrl=MarkerTypeUrl.CAR, label: string = null, iconSize: PointTuple=[41, 41]): Marker {
    const customIcon: Icon = new Icon({
      iconUrl: markerTypeUrl,
      iconSize: iconSize,
      iconAnchor: [12, 41],
      popupAnchor: [1, -34]
    });

    const marker: Marker = new Marker(latlng, { icon: customIcon }).addTo(this.map);
    if (!_.isNull(label)) {
      marker.bindPopup(label).openPopup();
    }
    this.addedLayers.push(marker);
    return marker;
  }

  addCircularMarkers(latLngTrack: LatLng[], circularMarkerConfig: CircleMarkerOptions = OsmMapComponent.CIRCULAR_MARKER_CONFIG): CircleMarker[] {
      const all_points: CircleMarker[] = latLngTrack.map((latLng: LatLng) => {
        const marker = circleMarker(latLng, circularMarkerConfig).addTo(this.map);
        marker.bindPopup(marker.getLatLng().toString()).openPopup();
        this.addedLayers.push(marker);
        return marker;
      }); 
      return all_points;
  }

  addRouteOnMap(coordinates: LatLngExpression[], color: string = 'blue', weight: number = 4): Polyline {
    const polyline = new Polyline(coordinates, {
      color: color,
      weight: weight,
      dashArray: '4 4'
    }).addTo(this.map);
    this.addedLayers.push(polyline);

    return polyline;
  }

  clearAll() {
    this.removeLayersFromMap(this.addedLayers)
  }

  removeLayersFromMap(layers: Layer[]) {
    layers.forEach(layer => {
      if (!_.isNil(layer)) {
        layer.remove();
      }
    });
  }

  private createDivElement(elementId: string) {
    const newDiv = this.renderer.createElement('div');
    this.renderer.setProperty(newDiv, 'id', elementId);
    this.renderer.appendChild(this.elRef.nativeElement.querySelector('#osm-map'), newDiv);
    this.renderer.setStyle(newDiv, 'height', '100%');
  }

}