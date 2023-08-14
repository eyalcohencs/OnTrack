import { Injectable } from '@angular/core';
import { firstValueFrom } from 'rxjs';
import { environment } from 'src/enviroment';
import { HttpClient, HttpParams } from '@angular/common/http';
import { BasePoints, GeoPoint } from '../geopoint-service/geopoint.service';

export interface LoginDetails {
  username: string;
  password: string;
}

export interface User {
  first_name: string,
  last_name: string,
  email: string,
  username: string;
  password?: string;  // TOdo - remove password
}

export interface UserSession extends User {  // TODO - rename to UserSession?
  id: string,
  token: string
}


@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private http: HttpClient) { }

  private baseUrl = environment.apiBaseUrl;

  public async getRoute(basePoint: BasePoints): Promise<GeoPoint[]> {
    const url: string = this.baseUrl + '/get_route';

    let queryParams: HttpParams = new HttpParams().appendAll(
      {start_lat: basePoint.start_lat,
        start_lng: basePoint.start_lng,
        end_lat: basePoint.end_lat,
        end_lng: basePoint.end_lng});

    let response = await firstValueFrom(this.http.get<GeoPoint[]>(url,{params:queryParams}));
    return response;
  }

  public async getAllPoints(): Promise<GeoPoint[]> {
    const url: string = this.baseUrl + '/get_all_points';
    let response = await firstValueFrom(this.http.get<GeoPoint[]>(url))
    return response;
  }
  // TODO - change type
  public async getAllRelations(): Promise<any[]> {
    const url: string = this.baseUrl + '/get_all_relations';
    let response = await firstValueFrom(this.http.get<any[]>(url))
    return response;
  }

  public async register(user: User): Promise<boolean> {
    const url: string = this.baseUrl + '/register';
    try {
      const result: {is_created: boolean} = await firstValueFrom(this.http.post<any>(url, {
        username: user.username,
        password: user.password,
        first_name: user.first_name,
        last_name: user.last_name,
        email: user.email
      }));
      // TODO - change te way to know that 201 user was created - passing dict doesn't seems to be the right way
      console.log('register api' + result);
      return result['is_created'];
    } catch(e) {
      console.log(e);
      return false;
    }
    
  }
  

  public async login(username: string, password: string): Promise<UserSession> {
    const url: string = this.baseUrl + '/login';
    let response: UserSession = await firstValueFrom(this.http.post<any>(url, {
      username: username,
      password: password}))
    return response;
  }


  public async logout(): Promise<boolean> {
    const url: string = this.baseUrl + '/logout';
    let response: boolean = await firstValueFrom(this.http.post<any>(url, {}))
    return response;
  }

}
