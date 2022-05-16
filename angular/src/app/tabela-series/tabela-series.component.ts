import { AfterViewInit, Component, Input, OnInit, ViewChild } from '@angular/core';
import { MatPaginator, PageEvent } from '@angular/material/paginator';
import { MatTableDataSource } from '@angular/material/table';
import { SerieEntity } from '../entity/serie-entity';

@Component({
  selector: 'app-tabela-series',
  templateUrl: './tabela-series.component.html',
  styleUrls: ['./tabela-series.component.scss']
})
export class TabelaSeriesComponent implements OnInit, AfterViewInit {
  @ViewChild(MatPaginator, {static: false}) paginator!: MatPaginator;
  @Input('titulo') titulo!: string;
  @Input('series') series!: Array<SerieEntity>;

  //constructor(private restService: RestService) { }
  constructor(){ }

  ngOnInit(): void {
    setTimeout(() => this.atualizaPaginacao());
    this.mostraTabelaSeries = true
  }

  ngAfterViewInit() {
    this.tabelaSeries.paginator = this.paginator;
  }

  totalRows = 0;
  pageSize = 100;
  currentPage = 0;

  tabelaSeries: MatTableDataSource<SerieEntity> = new MatTableDataSource()
  colunas: string[] = ['codigo', 'nome', 'unidade', 'periodicidade', 'inicio', 'ultimovalor', 'fonte', 'especial']
  mostraTabelaSeries = false

  atualizaPaginacao(){
    this.mostraTabelaSeries = false
    let base = this.currentPage * this.pageSize
    this.tabelaSeries.data = this.series.slice(base, base + this.pageSize)
    setTimeout(() => {
      this.paginator.pageIndex = this.currentPage;
      this.paginator.length = this.series.length;
    });
    this.mostraTabelaSeries = true
  }

  pageChanged(event: PageEvent) {
    console.log({ event });
    this.pageSize = event.pageSize;
    this.currentPage = event.pageIndex;
    this.atualizaPaginacao();
  }
  

}
