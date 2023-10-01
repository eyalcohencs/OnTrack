import { Component, OnInit } from '@angular/core';
import { interval } from 'rxjs';
import { ApiService } from 'src/app/services/api-service/api-service.service';

@Component({
  selector: 'app-site-notifications',
  templateUrl: './site-notifications.component.html',
  styleUrls: ['./site-notifications.component.less']
})
export class SiteNotificationsComponent implements OnInit{
  constructor(private apiService: ApiService) {}

  showHealthMessage: boolean = false;
  
  ngOnInit(): void {
    this.presentHealthMessage();
    // Send a health check request
    interval(60000).subscribe(() => {
      this.presentHealthMessage();
    });
  }

  presentHealthMessage() {
    this.apiService.healthCheck().then((data)=>{
      this.showHealthMessage = false;
    }).catch((error)=>{
      this.showHealthMessage = true;
    });
    
  }
}
