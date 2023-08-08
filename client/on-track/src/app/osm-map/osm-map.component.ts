import { Component, OnInit, AfterViewInit, Input, Output, EventEmitter, ElementRef, Renderer2 } from '@angular/core';
import { Map, map, tileLayer, Marker, Polyline, LatLngExpression, Icon, Layer, LatLngTuple, CircleMarkerOptions, LatLng, circleMarker, CircleMarker} from 'leaflet';

import * as _ from "lodash";

@Component({
  selector: 'app-osm-map',
  templateUrl: './osm-map.component.html',
  styleUrls: ['./osm-map.component.less']
})
export class OsmMapComponent implements OnInit, AfterViewInit {

  constructor(private elRef: ElementRef, private renderer: Renderer2) {}
  
  // static readonly OPEN_STREET_MAP_TILES: string = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
  // static readonly OPEN_STREET_MAP_TILES: string = 'http://IsraelHiking.OSM.org.il/OverlayTiles/{z}/{x}/{y}.png';
  // static readonly OPEN_STREET_MAP_TILES: string = `https://israelhiking.osm.org.il/Hebrew/mtbTiles/{z}/{x}/{y}.png`;
  static readonly OPEN_STREET_MAP_TILES: string = `https://israelhiking.osm.org.il/Hebrew/Tiles/{z}/{x}/{y}.png`;
  static readonly ISRAEL_CENTER: LatLngTuple = [ 32.6000, 35.0000 ];
  static readonly MAP_ZOOM: number = 11;
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
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>' // todod - check if need to be removed
    });

    tiles.addTo(this.map);
  }

  private onMapClick(event: any) {
      this.clickOnMap.emit(event);
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

  addRouteOnMap(coordinates: LatLngExpression[], color: string = 'blue', weight: number = 5): Polyline {
    const polyline = new Polyline(coordinates, {
      color: color,
      weight: weight
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