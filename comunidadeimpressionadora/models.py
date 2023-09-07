from comunidadeimpressionadora import database, login_manager
from datetime import datetime
from flask_login import UserMixin



@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))


class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, default='default.jpg')
    posts = database.relationship('Post', backref='autor', lazy=True)
    cursos = database.Column(database.String, nullable=False, default='Não Informado')

    def contar_posts(self):
        return len(self.posts)


class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.Text, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)

class CadastrarProjetoVendas(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    mbes                = database.Column(database.String)
    vendedor            = database.Column(database.String)
    endereco            = database.Column(database.Text)
    cliente             = database.Column(database.Text)
    email               = database.Column(database.Text)
    telefone            = database.Column(database.Text)
    datacm              = database.Column(database.Text)
    dataesquad          = database.Column(database.Text)
    datacontrato        = database.Column(database.Text)
    prazofixo           = database.Column(database.Text)
    crm                 = database.Column(database.Text)
    observacaocompra    = database.Column(database.Text)
    observacaoinstalacao= database.Column(database.Text)
    observacaoprojeto   = database.Column(database.Text)
    observacaoproducao  = database.Column(database.Text)
    numorcamento        = database.Column(database.Text)
    solorcamento        = database.Column(database.Text)
    envorcamento        = database.Column(database.Text)
    medcmprevisto       = database.Column(database.Text)
    medcmrealizado      = database.Column(database.Text)
    medesquadprevisto   = database.Column(database.Text)
    medesquadrealizado  = database.Column(database.Text)
    guiacmgerado        = database.Column(database.Text)
    guiaesquadgerado    = database.Column(database.Text)
    datapedidovidro     = database.Column(database.Text)
    datapedidoperfil    = database.Column(database.Text)
    datapedidoacessorio = database.Column(database.Text)
    statusprojeto       = database.Column(database.Text)
    valorprojeto        = database.Column(database.Text)
    reserva1            = database.Column(database.Text)
    reserva2            = database.Column(database.Text)
    reserva3            = database.Column(database.Text)
    reserva4            = database.Column(database.Text)
    detalhes            = database.Column(database.String)
    data_criacao        = database.Column(database.DateTime, default=datetime.utcnow)




