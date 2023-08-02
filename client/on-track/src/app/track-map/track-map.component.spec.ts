import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TrackMapComponent } from './track-map.component';

describe('TrackMapComponent', () => {
  let component: TrackMapComponent;
  let fixture: ComponentFixture<TrackMapComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [TrackMapComponent]
    });
    fixture = TestBed.createComponent(TrackMapComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
