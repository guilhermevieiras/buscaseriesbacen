import { Component, OnInit } from '@angular/core';
import { SerieEntity } from './entity/serie-entity';
import { RestService } from './rest.service';

import { map } from 'rxjs/operators';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  title = 'angular';

  constructor(private restService: RestService) { }

  ngOnInit(): void {
    this.buscaSeriesAtivas().subscribe(() => {
      // Ordena as datas
      this.seriesRecentes = this.seriesAtivas.sort(function(a,b){
        // torna strings em datas, e subtrai elas.
        // com isso obtemos um valor positivos negativo, negativo ou zero.
        return new Date(b.inicio).getTime() - new Date(a.inicio).getTime();
      });
      this.seriesRecentes = this.seriesRecentes.slice(0, 30)
      this.mostraTabelaSeriesRecentes = true
      this.erroMostrarTabelaSeriesRecentes = false
    })
    this.buscaSeriesDesativadas()
  }

  seriesAtivas!:Array<SerieEntity>
  seriesDesativadas!:Array<SerieEntity>
  seriesRecentes!:Array<SerieEntity>

  erroMostrarTabelaSeries = false
  mostraTabelaSeries = false

  erroMostrarTabelaSeriesDesativadas = false
  mostraTabelaSeriesDesativadas = false

  erroMostrarTabelaSeriesRecentes = false
  mostraTabelaSeriesRecentes = false


  buscaSeriesAtivas(){
    return this.restService.consultaSeriesPorStatus('Ativa').pipe(map((resposta:Array<SerieEntity>) => {
      this.seriesAtivas = resposta;
      this.mostraTabelaSeries = true
      this.erroMostrarTabelaSeries = false
      console.log(resposta)
    }, (err) => {
      console.log('Não conseguiu consultar séries')
      console.log(err)
      this.erroMostrarTabelaSeries = true
      this.mostraTabelaSeries = false
      this.erroMostrarTabelaSeriesRecentes = true
      this.mostraTabelaSeriesRecentes = false
    }))
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
