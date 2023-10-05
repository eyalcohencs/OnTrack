import { Injectable } from '@angular/core';
import { Observable, Subscription, firstValueFrom } from 'rxjs';
import { environment } from 'src/environment';
import { HttpClient} from '@angular/common/http';
import { BasePoints, GeoCalculatedRoute, GeoPoint, GeoRoad } from '../geopoint-service/geopoint.service';
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

export enum TrackLoadingSource {
  SERVER = 'server',
  CLOUD = 'cloud'
}

export enum AuthenticationResponseCode {
  SUCCEED = 'succeed',
  USERNAME_ALREADY_EXIST = 'username_already_exists',
  USERNAME_INVALID = 'invalid_username',
  PASSWORD_INVALID = 'invalid_password',
  EMAIL_ALREADY_EXIST = 'email_already_exist',
  EMAIL_INVALID = 'invalid_email',
  FIRST_LAST_NAME_TOO_SHORT = 'first_last_name_too_short',
  UNKNOWN = 'unknown'
}

export interface AuthenticationResponse {
  is_created: boolean,
  auth_response_code: AuthenticationResponseCode,
  error: null | string
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

  public register(user: User): Observable<AuthenticationResponse> {
    const url: string = this.baseUrl + '/register';
    const data =  {
      username: user.username,
      password: user.password,
      first_name: user.first_name,
      last_name: user.last_name,
      email: user.email
    };
    
    return this.http.post<any>(url, data)
    
  }
  
  public async login(username: string, password: string): Promise<UserSession> {
    const url: string = this.baseUrl + '/login';
    const data: any = {username: username, password: password};
    let response: UserSession = await firstValueFrom(this.http.post<any>(url, data));
    return response;
  }

  public logout(): Observable<void> {
    const url: string = this.baseUrl + '/logout';
    const data = {};
    return this.http.post<void>(url, data);
  }

  /* Tracks API */

  public async getRoute(basePoint: BasePoints): Promise<GeoCalculatedRoute> {
    const url: string = this.baseUrl + '/get_route';
    const queryParams = {start_lat: basePoint.start_lat,
      start_lng: basePoint.start_lng,
      end_lat: basePoint.end_lat,
      end_lng: basePoint.end_lng};
    let response: GeoCalculatedRoute = await firstValueFrom(this.http.get<GeoCalculatedRoute>(url, {params: queryParams}));
    return response;
  }

  public async getAllPoints(): Promise<GeoPoint[]> {
    const url: string = this.baseUrl + '/get_all_points';
    let response = await firstValueFrom(this.http.get<GeoPoint[]>(url))
    return response;
  }

  public async getAllRoads(): Promise<GeoRoad[]> {
    try {
      const url: string = this.baseUrl + '/get_all_roads';
      let response: GeoRoad[] = await firstValueFrom(this.http.get<any[]>(url));
      return response;
    } catch (error) {
      console.error('Error' + error);
      return null;
    }
  }

  public async updateTracks(trackLoadingSource: TrackLoadingSource): Promise<void> {
    const url: string = this.baseUrl + '/start_update_graph_db';
    const data = {'loading_source': trackLoadingSource};
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
