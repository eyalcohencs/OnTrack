import { TestBed } from '@angular/core/testing';

import { OnTrackInterceptor } from './on-track.interceptor';

describe('OnTrackInterceptorInterceptor', () => {
  beforeEach(() => TestBed.configureTestingModule({
    providers: [
      OnTrackInterceptor
      ]
  }));

  it('should be created', () => {
    const interceptor: OnTrackInterceptor = TestBed.inject(OnTrackInterceptor);
    expect(interceptor).toBeTruthy();
  });
});
