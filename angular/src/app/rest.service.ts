import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

import { AppSettings } from './appSettings';

@Injectable({
  providedIn: 'root'
})
export class RestService {
  constructor(private http: HttpClient) { }

  consultarSeries(){
    console.log('consultarSeries');
    return this.http.get<Array<any>>(AppSettings.API_ENDPOINT + 'series')
  }

  consultaSeriesPorStatus(status: string){
    console.log('consultarSeriesPorStatus');
    let parametros = new HttpParams();
    parametros = parametros.append('status', status);
    return this.http.get<Array<any>>(AppSettings.API_ENDPOINT + 'series', {params: parametros})
  }

}
