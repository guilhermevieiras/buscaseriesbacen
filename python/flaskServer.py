import requests
import os
from datetime import date, datetime
import threading


# pip install flask
from flask import Flask, request

# pip install flask_restful
from flask_restful import Api, Resource, reqparse


from sqlalchemy import orm, Table, Column, Integer, String, Date
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


# pip install Flask-Script
#from flask_script import Manager

from models import SeriesModel, db
from carregaDadosBacen import executaBuscaSeries


app = Flask(__name__)
BANCO_LOCAL_SQLALCHEMY = 'sqlite:///database.db'


app.config['SQLALCHEMY_DATABASE_URI'] = BANCO_LOCAL_SQLALCHEMY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)
db.init_app(app)


class SeriesView(Resource):
    def get(self):
        series = SeriesModel.query.all()
        print(series)
        return list(s.json() for s in series)
    def salvaSeries(self, series):
        db.session.add_all(series)
        db.session.commit()
        db.session.flush()
        
        
# def inicializa_banco(series):
#     db.create_all()
#     SeriesView().salvaSeries(series)


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
    #session.
    session.add_all(series)
    #session.commit()
    session.merge()
    session.flush()
    session.close()
    

def coleta_dados():
    print('coleta_dados')
    series = executaBuscaSeries()
    # serie1 = SeriesModel(1, '', '', '', date.today(), '', '', '', '')
    # serie2 = SeriesModel(2, '', '', '', date.today(), '', '', '', '')
    # series = [serie1, serie2]
    inicializa_banco_antes_servidor(series)
    
        
        
api.add_resource(SeriesView, '/series')


# def do_something():
#   print('MyFlaskApp is starting up!')

# class MyFlaskApp(Flask):
#   def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
#     # if not self.debug or os.getenv('WERKZEUG_RUN_MAIN') == 'true':
#     #   with self.app_context():
#     #     do_something()
#     super(MyFlaskApp, self).run(host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)

# app = MyFlaskApp(__name__)
# app.run()


# def teste():
#     print('teste..........................................................')
    

# def inicializa_app():
#     app.run(debug=True, use_reloader=False)
    


if __name__ == '__main__':
    # first_thread = threading.Thread(target=inicializa_app)
    # second_thread = threading.Thread(target=coleta_dados)
    # first_thread.start()
    # second_thread.start()
    coleta_dados()
    app.run(debug=True, use_reloader=False)

        