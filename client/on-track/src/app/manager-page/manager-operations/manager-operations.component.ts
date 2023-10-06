import { Component } from '@angular/core';
import { ApiService, TrackLoadingSource } from 'src/app/services/api-service/api-service.service';

/**
 * This component present the operations that the system user can do in the site.
 * For instance, loading new tracks to the system.
 */

@Component({
  selector: 'app-manager-operations',
  templateUrl: './manager-operations.component.html',
  styleUrls: ['./manager-operations.component.less']
})
export class ManagerOperationsComponent {
  constructor(private apiService: ApiService) {}

  TrackLoadingSource = TrackLoadingSource;
  
  updateTracks(trackLoadingSource: TrackLoadingSource) {
    this.apiService.updateTracks(trackLoadingSource);
  }
}
