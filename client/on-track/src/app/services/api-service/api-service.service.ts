import { Injectable } from '@angular/core';
import { Observable, firstValueFrom } from 'rxjs';
import { environment } from 'src/enviroment';
import { HttpClient, HttpParams } from '@angular/common/http';

export interface GeoPoint {
    longitude: number;
    latitude: number;
    time?: Date
    altitude?: number;
    uuid?: string;
}

export interface BasePoints {
  start_lat: number;
  start_lng: number;
  end_lat: number;
  end_lng: number;
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

}
