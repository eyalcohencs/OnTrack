import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor,
  HttpHeaders
} from '@angular/common/http';
import { Observable } from 'rxjs';
import { CookieService } from 'ngx-cookie-service';

@Injectable()
export class OnTrackInterceptor implements HttpInterceptor {

  constructor(private cookieService: CookieService) {}

  intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    const commonOptions: any = {
      withCredentials: true,
      headers: new HttpHeaders({Authorization: `Bearer ${this.cookieService.get('token')}`})
    }
    const modifiedRequest: HttpRequest<any> = request.clone(commonOptions);
    return next.handle(modifiedRequest);
  }

}
