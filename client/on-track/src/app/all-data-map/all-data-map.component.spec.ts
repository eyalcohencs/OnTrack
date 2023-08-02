import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AllDataMapComponent } from './all-data-map.component';

describe('AllDataMapComponent', () => {
  let component: AllDataMapComponent;
  let fixture: ComponentFixture<AllDataMapComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [AllDataMapComponent]
    });
    fixture = TestBed.createComponent(AllDataMapComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
