import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { ApiService } from '../api-service/api-service.service';
import { User } from '../user-enum';

/**
 * The service keep the state of the current user.
 * It serve different component that consume the user details.
 */
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

  getUser(): User {
    return this.userSubject.getValue();
  }

}
