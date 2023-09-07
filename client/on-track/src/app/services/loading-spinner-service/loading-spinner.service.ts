import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class LoadingSpinnerService {

  constructor() { }

  private isPresented = new BehaviorSubject<boolean>(false);
  public isPresented$ = this.isPresented.asObservable();

  show() {
    this.isPresented.next(true);
  }

  hide() {
    this.isPresented.next(false);
  }

}
