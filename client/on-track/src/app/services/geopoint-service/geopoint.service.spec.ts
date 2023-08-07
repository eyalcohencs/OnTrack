import { TestBed } from '@angular/core/testing';

import { GeopointService } from '../geopoint.service';

describe('GeopointService', () => {
  let service: GeopointService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(GeopointService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
