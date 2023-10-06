import { Injectable } from '@angular/core';
import { LatLng, Polyline } from 'leaflet';

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

export interface GeoCalculatedRoute {
  points: GeoPoint[];
  roads: GeoRoad[];
}

export interface GeoRoad {
  track_id: string;
  source_geo_point: GeoPoint;
  target_geo_point: GeoPoint;
  uuid: string;
}

/**
 * Service for handling GeoPoint, which is the represenation for point in the system.
 * It provides interfaces and utils methods.
 */
@Injectable({
  providedIn: 'root'
})
export class GeopointService {

  constructor() { }

  convertGeoPointsToLatLng(track: GeoPoint[]): LatLng[] {
      return track.map((geoPoint: GeoPoint) => new LatLng(geoPoint.latitude, geoPoint.longitude, geoPoint.altitude));
  }

  convertPolylineToGeoPoints(polyline: Polyline): GeoPoint[] {
     const latLngsPoints: LatLng[] = polyline.getLatLngs() as LatLng[];
     const geoPoints = latLngsPoints.map(
      (latLngPoint: LatLng) => {return {longitude: latLngPoint.lng, latitude: latLngPoint.lat, altitude: latLngPoint.alt}}
      );
      return geoPoints;
  }
}
