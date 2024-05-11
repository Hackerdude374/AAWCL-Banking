import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CardmanagementComponent } from './cardmanagement.component';

describe('CardmanagementComponent', () => {
  let component: CardmanagementComponent;
  let fixture: ComponentFixture<CardmanagementComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CardmanagementComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CardmanagementComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
