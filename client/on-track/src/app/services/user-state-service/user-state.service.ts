import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { ApiService, User } from '../api-service/api-service.service';

@Injectable({
  providedIn: 'root'
})
export class UserStateService {

  constructor(private apiService: ApiService) { }
  
  private userSubject: BehaviorSubject<User> = new BehaviorSubject<User>(null);
  public user$: Observable<User> = this.userSubject.asObservable();
  
  setUser(user: User): void {
    this.userSubject.next(user);
  }

  async fetchUserData() {
    const user: User = await this.apiService.getUserDetails();
    this.setUser(user);
  }

}
