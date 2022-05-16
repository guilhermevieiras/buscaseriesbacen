# pip install flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class SeriesModel(db.Model):
    __tablename__ = 'series'
    codigo = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String())
    unidade = db.Column(db.String())
    periodicidade = db.Column(db.String())
    inicio = db.Column(db.Date())
    ultimovalor = db.Column(db.String())
    fonte = db.Column(db.String())
    especial = db.Column(db.String())
    status = db.Column(db.String())
    
    
    def  __init__(self, codigo, nome, unidade, periocidade, inicio, ultimovalor, fonte, especial, status):
        self.codigo = codigo
        self.nome = nome
        self.unidade = unidade
        self.periodicidade = periocidade
        self.inicio = inicio
        self.ultimovalor = ultimovalor
        self.fonte = fonte
        self.especial = especial
        self.status = status
        
        
    def json(self):
        return {
            'codigo': self.codigo,
            'nome': self.nome,
            'unidade': self.unidade,
            'periodicidade': self.periodicidade,
            'inicio': self.inicio.strftime("%Y-%m-%d"),
            'ultimovalor': self.ultimovalor,
            'fonte': self.fonte,
            'especial': self.especial,
            'status': self.status
        }