# buscaseriesbacen
Busca Series Ativas e Desativadas via web scraping e monta uma lista destas no Angular




## Instalar Python
OBS: É recomendado o Python 3.10v ou superior

## Para instalar todas as dependências do Python basta executar o seguinte comando na pasta .\buscaseriesbacen
```python
pip install requisitos.txt
```
Então executar o comando para rodar os scripts de web scrapping e subir o servidor Flask na pasta .\buscaseriesbacen\python
```
py flaskServer.py
```


## Instalar Angular
Instalação do Angular
```angular
npm install -g @angular/cli
```
OBS: é preciso instalar o nodejs antes que deve ser baixado e instalado
Na pasta do projeto .\buscaseriesbacen\angular executar o comando:
```angular
npm install
```
Então executar o comando para subir o servidor do Angular
```python
ng serve
```
Acessar o servidor via o endereço
```
http://localhost:4200/
```

## Alternativamente o projeto pode ser instalado via makefile (funciona em Linux e MacOS) executando o seguinte comando na pasta na pasta .\buscaseriesbacen
```
make
```
