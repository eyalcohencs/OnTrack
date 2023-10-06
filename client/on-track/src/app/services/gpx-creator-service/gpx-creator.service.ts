import { Injectable } from '@angular/core';
import { Polyline } from 'leaflet';
import { GeoPoint, GeopointService } from '../geopoint-service/geopoint.service';
import { saveAs } from 'file-saver'

/**
 * Service for creating gpx file of the user track, and download ability.
 */
@Injectable({
  providedIn: 'root'
})
export class GpxCreatorService {

  constructor(private geopointService: GeopointService) { }

  static readonly DOWNLOAD_GPX_FILE_NAME = 'route.gpx';

  createGPXFile(createdRoute: Polyline) {
    console.log('onCreateGPXFile', createdRoute);
    const geoPoints: GeoPoint[] = this.geopointService.convertPolylineToGeoPoints(createdRoute);

    const gpxContent = this.createGPXContent(geoPoints);
    this.downloadGPXFile(gpxContent, GpxCreatorService.DOWNLOAD_GPX_FILE_NAME);
  }

  private createGPXContent(route: GeoPoint[]): string {
    let gpxContent: string = ``;
    const gpxHeader: string = 
    `<?xml version="1.0" encoding="UTF-8"?>
<gpx creator="On Track algorithm" version="1.0" xmlns="http://www.topografix.com/GPX/1/1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd http://www.garmin.com/xmlschemas/GpxExtensions/v3 http://www.garmin.com/xmlschemas/GpxExtensionsv3.xsd http://www.garmin.com/xmlschemas/TrackPointExtension/v1 http://www.garmin.com/xmlschemas/TrackPointExtensionv1.xsd">
  <metadata>
    <name>OnTrack</name>
  </metadata>
  <trk>
    <name>track</name>
    <trkseg>
    `;
    const gpxFooter: string = 
    `</trkseg>
  </trk>
</gpx>`;

    gpxContent += gpxHeader;
    route.forEach((point: GeoPoint) => gpxContent += `  <trkpt lat="${point.latitude}" lon="${point.longitude}">
        <ele>"${point.altitude}"</ele>
      </trkpt>
    `);
    gpxContent += gpxFooter;
    return gpxContent;
  }

  private downloadGPXFile(gpxContent: string, fileName: string) {
    const blob = new Blob([gpxContent], { type: 'text/xml;charset=utf-8' });
    saveAs(blob, fileName);
  }

}
