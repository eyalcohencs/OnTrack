import { Injectable } from '@angular/core';
import { firstValueFrom } from 'rxjs';
import { environment } from 'src/environment';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { BasePoints, GeoCalculatedRoute, GeoPoint } from '../geopoint-service/geopoint.service';
import { CookieService } from 'ngx-cookie-service';
import { User } from '../user-enum';

export interface LoginDetails {
  username: string;
  password: string;
}

export interface UserSession {
  username: string,
  token: string,
  user: User
}


@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(
    private http: HttpClient,
    private cookieService: CookieService) { }
  
  private baseUrl = environment.apiBaseUrl + environment.apiVersion;
  // private baseUrlUpdateGraphService = environment.apiBaseUrlUpdateGraphService;

  /* Authentication API */

  public async register(user: User): Promise<boolean> {
    const url: string = this.baseUrl + '/register';
    try {
      const data =  {
        username: user.username,
        password: user.password,
        first_name: user.first_name,
        last_name: user.last_name,
        email: user.email
      };
      const result: {is_created: boolean} = await firstValueFrom(this.http.post<any>(url, data));
      // TODO - change the way to know that 201 user was created - passing dict doesn't seems to be the right way
      console.log('register api' + result);
      return result['is_created'];
    } catch(e) {
      console.log(e);
      return false;
    }
    
  }
  
  public async login(username: string, password: string): Promise<UserSession> {
    const url: string = this.baseUrl + '/login';
    const data: any = {username: username, password: password};
    let response: UserSession = await firstValueFrom(this.http.post<any>(url, data));
    return response;
  }

  // TODO - handle typing
  public async logout(): Promise<{is_logged_out: boolean}> {
    const url: string = this.baseUrl + '/logout';
    const data = {};
    let response: {is_logged_out: boolean} = await firstValueFrom(this.http.post<any>(url, data))
    return response;
  }

  /* Tracks API */

  // TODO - fix any typing
  public async getRoute(basePoint: BasePoints): Promise<GeoCalculatedRoute> {
    const url: string = this.baseUrl + '/get_route';
    const queryParams = {start_lat: basePoint.start_lat,
      start_lng: basePoint.start_lng,
      end_lat: basePoint.end_lat,
      end_lng: basePoint.end_lng};
    let response: any = await firstValueFrom(this.http.get<GeoCalculatedRoute>(url, {params: queryParams}));
    return response;
  }

  public async getAllPoints(): Promise<GeoPoint[]> {
    const url: string = this.baseUrl + '/get_all_points';
    let response = await firstValueFrom(this.http.get<GeoPoint[]>(url))
    return response;
  }

  // TODO - change type
  public async getAllRelations(): Promise<any[]> {
    try {
      const url: string = this.baseUrl + '/get_all_relations';
      let response = await firstValueFrom(this.http.get<any[]>(url));
      return response;
    } catch (error) {
      console.error('Error' + error);
      return null;
    }
  }

  public async updateTracks(): Promise<void> {
    const url: string = this.baseUrl + '/start_update_graph_db';
    const data = {};
    let response: void = await firstValueFrom(this.http.post<any>(url, data))
    return response;
  }

  /* Users API */

  public async getUserDetails(): Promise<User> {
    const url: string = this.baseUrl + '/get_user_details';
    let response: any = await firstValueFrom(this.http.get<any[]>(url));
    return response;
  }

  public async getAllUserDetails(): Promise<User[]> {
    const url: string = this.baseUrl + '/get_all_users';
    let response: any = await firstValueFrom(this.http.get<any[]>(url));
    return response;
  }

  /* Health check API */

  public async healthCheck(): Promise<void> {
    const url: string = environment.apiBaseUrl  + '/status';
    let response: any = await firstValueFrom(this.http.get<any[]>(url));
    return response;
  }


}
