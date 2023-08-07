import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Polyline } from 'leaflet';
import { GpxCreatorService } from '../services/gpx-creator-service/gpx-creator.service';

@Component({
  selector: 'app-track-creation',
  templateUrl: './track-creation.component.html',
  styleUrls: ['./track-creation.component.less']
})
export class TrackCreationComponent {

  constructor(private gpxCreatorService: GpxCreatorService) {}
  @Input() sourceLat: number;
  @Input() sourceLng: number;
  @Input() targetLat: number;
  @Input() targetLng: number;
  @Input() createdRoute: Polyline; 

  @Output() composeTrack = new EventEmitter<{ source: number[], target: number[] }>();
  @Output() clearAll = new EventEmitter<void>();

  onComposeTrack() {
    const source = [this.sourceLat, this.sourceLng];
    const target = [this.targetLat, this.targetLng];
    this.composeTrack.emit({ source, target });
  }

  onClearAll() {
    this.clearAll.emit();
    this.sourceLat = this.sourceLng = this.targetLat = this.targetLng = null;
  }

  onCreateGPXFile() {
    this.gpxCreatorService.createGPXFile(this.createdRoute);

  }

}
