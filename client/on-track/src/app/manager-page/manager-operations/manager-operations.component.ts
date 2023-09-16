import { Component } from '@angular/core';
import { ApiService } from 'src/app/services/api-service/api-service.service';

@Component({
  selector: 'app-manager-operations',
  templateUrl: './manager-operations.component.html',
  styleUrls: ['./manager-operations.component.less']
})
export class ManagerOperationsComponent {
  constructor(private apiService: ApiService) {}
  
  updateTracks() {
    this.apiService.updateTracks();
  }
}
