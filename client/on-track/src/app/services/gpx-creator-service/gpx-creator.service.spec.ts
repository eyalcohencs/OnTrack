import { TestBed } from '@angular/core/testing';

import { GpxCreatorService } from './gpx-creator.service';

describe('GpxCreatorService', () => {
  let service: GpxCreatorService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(GpxCreatorService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
