import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../services/api-service/api-service.service';
import { User } from '../../services/user-enum';

/**
 * This component displays a table with all the users in the database.
 * This being use in manager page.
 */
@Component({
  selector: 'app-users-details',
  templateUrl: './users-details.component.html',
  styleUrls: ['./users-details.component.less']
})
export class UsersDetailsComponent implements OnInit{
  constructor(private apiService: ApiService) { }

  users_list: User[] = [];

  async ngOnInit(): Promise<void> {
    this.users_list = await this.apiService.getAllUserDetails();

  }
}
