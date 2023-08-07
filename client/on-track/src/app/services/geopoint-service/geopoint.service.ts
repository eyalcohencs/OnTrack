import { Injectable } from '@angular/core';
import { LatLng } from 'leaflet';

export interface GeoPoint {
  longitude: number;
  latitude: number;
  time?: Date
  altitude?: number;
  uuid?: string;
}

export interface BasePoints {
start_lat: number;
start_lng: number;
end_lat: number;
end_lng: number;
}

@Injectable({
  providedIn: 'root'
})
export class GeopointService {

  constructor() { }

  convertGeoPointsToLatLng(track: GeoPoint[]): LatLng[] {
      return track.map((geoPoint: GeoPoint) => new LatLng(geoPoint.latitude, geoPoint.longitude, geoPoint.altitude));
  }
}
