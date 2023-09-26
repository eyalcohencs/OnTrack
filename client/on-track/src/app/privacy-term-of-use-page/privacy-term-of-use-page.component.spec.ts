import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PrivacyTermOfUsePageComponent } from './privacy-term-of-use-page.component';

describe('PrivacyTermOfUsePageComponent', () => {
  let component: PrivacyTermOfUsePageComponent;
  let fixture: ComponentFixture<PrivacyTermOfUsePageComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [PrivacyTermOfUsePageComponent]
    });
    fixture = TestBed.createComponent(PrivacyTermOfUsePageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
