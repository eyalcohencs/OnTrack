import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-track-creation',
  templateUrl: './track-creation.component.html',
  styleUrls: ['./track-creation.component.less']
})
export class TrackCreationComponent {
    @Input() sourceLat: number = 0;
    @Input() sourceLng: number = 0;
    @Input() targetLat: number = 0;
    @Input() targetLng: number = 0;

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

}
