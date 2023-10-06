import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

/**
 * The service control the displaying of loading spinner widget and its state.
 */
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
