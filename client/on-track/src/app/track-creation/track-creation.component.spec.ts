import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TrackCreationComponent } from './track-creation.component';

describe('TrackCreationComponent', () => {
  let component: TrackCreationComponent;
  let fixture: ComponentFixture<TrackCreationComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [TrackCreationComponent]
    });
    fixture = TestBed.createComponent(TrackCreationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
