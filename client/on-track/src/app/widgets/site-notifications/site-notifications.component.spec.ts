import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SiteNotificationsComponent } from './site-notifications.component';

describe('SiteNotificationsComponent', () => {
  let component: SiteNotificationsComponent;
  let fixture: ComponentFixture<SiteNotificationsComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [SiteNotificationsComponent]
    });
    fixture = TestBed.createComponent(SiteNotificationsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
