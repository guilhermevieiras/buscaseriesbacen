import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TabelaSeriesComponent } from './tabela-series.component';

describe('TabelaSeriesComponent', () => {
  let component: TabelaSeriesComponent;
  let fixture: ComponentFixture<TabelaSeriesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TabelaSeriesComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(TabelaSeriesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
