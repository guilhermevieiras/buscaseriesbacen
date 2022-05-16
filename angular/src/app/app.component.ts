import { Component, OnInit } from '@angular/core';
import { SerieEntity } from './entity/serie-entity';
import { RestService } from './rest.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  title = 'angular';

  constructor(private restService: RestService) { }

  ngOnInit(): void {
    this.buscaSeriesAtivas()
    this.buscaSeriesDesativadas()
  }

  seriesAtivas!:Array<SerieEntity>
  seriesDesativadas!:Array<SerieEntity>

  erroMostrarTabelaSeries = false
  mostraTabelaSeries = false

  erroMostrarTabelaSeriesDesativadas = false
  mostraTabelaSeriesDesativadas = false

  erroMostrarTabelaSeriesRecentes = false
  mostraTabelaSeriesRecentes = false


  buscaSeriesAtivas(){
    this.restService.consultaSeriesPorStatus('Ativa').subscribe((resposta:Array<SerieEntity>) => {
      this.seriesAtivas = resposta;
      this.mostraTabelaSeries = true
      this.erroMostrarTabelaSeries = false
      console.log(resposta)
    }, (err) => {
      console.log('Não conseguiu consultar séries')
      console.log(err)
      this.erroMostrarTabelaSeries = true
      this.mostraTabelaSeries = false
    })
  }

  buscaSeriesDesativadas(){
    this.restService.consultaSeriesPorStatus('Desativada').subscribe((resposta:Array<SerieEntity>) => {
      this.seriesDesativadas = resposta;
      this.mostraTabelaSeriesDesativadas = true
      this.erroMostrarTabelaSeriesDesativadas = false
      console.log(resposta)
    }, (err) => {
      console.log('Não conseguiu consultar séries')
      console.log(err)
      this.erroMostrarTabelaSeriesDesativadas = true
      this.mostraTabelaSeriesDesativadas = false
    })
  }



}
