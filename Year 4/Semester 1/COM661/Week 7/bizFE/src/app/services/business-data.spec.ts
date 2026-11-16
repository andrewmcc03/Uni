import { TestBed } from '@angular/core/testing';
import { BusinessData } from './business-data';

describe('BusinessData', () => {
  let service: BusinessData;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(BusinessData);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
