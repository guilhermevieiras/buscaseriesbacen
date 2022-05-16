import { Component, Input, OnInit, ViewChild } from '@angular/core';
import { MatPaginator } from '@angular/material/paginator';
import { MatTableDataSource } from '@angular/material/table';
import { SerieEntity } from '../entity/serie-entity';
import { RestService } from '../rest.service';

@Component({
  selector: 'app-tabela-series',
  templateUrl: './tabela-series.component.html',
  styleUrls: ['./tabela-series.component.scss']
})
export class TabelaSeriesComponent implements OnInit {
  @ViewChild(MatPaginator, {static: false}) paginator: MatPaginator;
  @Input('titulo') titulo: string;
  @Input('series') series: Array<SerieEntity>;

  //constructor(private restService: RestService) { }
  constructor(){ }

  ngOnInit(): void {
    this.tabelaSeries.data = this.series;
    setTimeout(() => this.tabelaSeries.paginator = this.paginator);
    this.mostraTabelaSeries = true
  }

  tabelaSeries: MatTableDataSource<SerieEntity> = new MatTableDataSource()
  colunas: string[] = ['codigo', 'nome', 'unidade', 'periodicidade', 'inicio', 'ultimovalor', 'fonte', 'especial',  'status']
  erroMostrarTabelaSeries = false
  mostraTabelaSeries = false

  // buscaSeries(){
  //   this.restService.consultarSeries().subscribe((resposta:Array<SerieEntity>) => {
  //     this.tabelaSeries.data = resposta;
  //     setTimeout(() => this.tabelaSeries.paginator = this.paginator);
  //     this.mostraTabelaSeries = true
  //     this.erroMostrarTabelaSeries = false
  //   }, (err) => {
  //     console.log('Não conseguiu consultar séries')
  //     console.log(err)
  //     this.erroMostrarTabelaSeries = true
  //   })
  //}
  

}
