import time

# pip install flask
from flask import Flask, request

# pip install flask_restful
from flask_restful import Api, Resource

# pip install flask_sqlalchemy
from sqlalchemy import orm, Table, Column, Integer, String, Date
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from models import SeriesModel, db
from carregaDadosBacen import executaBuscaSeries

BANCO_LOCAL_SQLALCHEMY = 'sqlite:///database.db'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = BANCO_LOCAL_SQLALCHEMY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
db.init_app(app)


# Criação do View que prove os serviços para salvar os dados no banco usando o ORM do SQLAlchemy
class SeriesView(Resource):
    def get(self):
        args = request.args
        status = args['status']
        print(status)
        series = db.session.query(SeriesModel).filter_by(status=status)
        print(series)
        return list(s.json() for s in series)
    
    def salvaSeries(self, series):
        db.session.add_all(series)
        db.session.commit()
        db.session.flush()
     
# Resolvendo problema de CORS de conflito na requisção entre o Flask e o Angular   
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

# Salva dados das séries encontradas antes que a instância de banco de dados gerenciada pelo Flask esteja disponível
def inicializa_banco_antes_servidor(series):
    base = declarative_base()
    engine = create_engine(BANCO_LOCAL_SQLALCHEMY)
    base.metadata.bind = engine
    session = orm.scoped_session(orm.sessionmaker())(bind=engine)
    Table('series', base.metadata,
        Column('codigo', Integer, primary_key=True),
        Column('nome', String),
        Column('unidade', String),
        Column('periodicidade', String),
        Column('inicio', Date),
        Column('ultimovalor', String), 
        Column('fonte', String),
        Column('especial', String),
        Column('status', String))
    base.metadata.create_all()
    for serie in series:
        session.merge(serie, load=True)
    session.commit()
    session.flush()
    session.close()
    

def coleta_dados():
    print('coleta_dados')
    series = executaBuscaSeries()
    inicializa_banco_antes_servidor(series)
    
        
        
api.add_resource(SeriesView, '/series')

if __name__ == '__main__':
    
    # Inicializa coleta de dados de séries via web scrapping
    start = time.time()
    try:
        coleta_dados()
    except Exception as e:
        print('não foi possível executar a coleta de novos dados pelo erro:', str(e))
    end = time.time()
    print('tempo decorrido para atualização da base:', end - start)
    
    # Inicializa servidor Flask rest 
    app.run(debug=True, use_reloader=False)

        