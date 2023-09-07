from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from comunidadeimpressionadora.models import Usuario
from flask_login import current_user
from comunidadeimpressionadora.models import CadastrarProjetoVendas




class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField('Confirmação da Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar Conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado. Cadastre-se com outro e-mail ou faça login para continuar')


class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Lembrar Dados de Acesso')
    botao_submit_login = SubmitField('Fazer Login')


class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    foto_perfil = FileField('Atualizar Foto de Perfil', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    curso_pgr = BooleanField('PGR')
    curso_pcmso = BooleanField('PCMSO')
    curso_seguro = BooleanField('Seguro')
    curso_contrato = BooleanField('Contrato Parceiro')
    curso_cnh = BooleanField('CNH')
    curso_fichaepi = BooleanField('Ficha EPI')
    curso_aso = BooleanField('ASO')
    curso_nr01 = BooleanField('NR 01-OS')
    curso_nr06 = BooleanField('NR 06 - TREI EPI')
    curso_nr07 = BooleanField('NR 07 - 1º SOCORROS')
    curso_nr10 = BooleanField('NR 10 - INST ELET')
    curso_nr18 = BooleanField('NR 18 - INTEGRACÃO')
    curso_nr18A = BooleanField('NR 18 - PTA')
    curso_nr23 = BooleanField('NR 23 - BRIGADISTA')
    curso_nr33 = BooleanField('NR 33 - ESP CONF')
    curso_nr35 = BooleanField('NR 35 - TRABALHO')
    curso_nr35A = BooleanField('NR 35 - TRABALHO+RESGATE EM ALTURA')
    habilitacaogetesseg         = BooleanField('GE Tesseg')
    habilitacaogelm             = BooleanField('GE LM TESSEG')
    habilitacaogecamacari       = BooleanField('GE CAMAÇARI')
    habilitacaoomega            = BooleanField( 'ÔMEGA')
    habilitacaovestas           = BooleanField('VESTAS')
    habilitacaocubico           = BooleanField('CÚBICO')
    habilitacaostatkraft        = BooleanField('STATKRAFT')
    habilitacaoobrasoft         = BooleanField('OBRA SOFT')

    botao_submit_editarperfil = SubmitField('Confirmar Edição')

    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Já existe um usuário com esse e-mail. Cadastre outro e-mail')


class FormCriarPost(FlaskForm):
    titulo = StringField('Título do Post', validators=[DataRequired(), Length(2, 140)])
    corpo = TextAreaField('Escreva seu Post Aqui', validators=[DataRequired()])
    botao_submit = SubmitField('Criar Post')

class FormCadastroVendas(FlaskForm):
    mbes            = StringField('Cliente:', validators=[DataRequired(), Length(2, 20)])
    datacontrato    = StringField('Site', validators=[DataRequired()])
    vendedor        = StringField('Contato/Tell:', validators=[DataRequired()])

    cliente         = StringField('2º gerent local:')
    datacm          = StringField('tel2:')
    numorcamento    = StringField('Email 2:')

    email           = StringField('3º gerente local:')
    dataesquad      = StringField('3º Tel:')
    solorcamento    = StringField('email 3:')

    telefone        = StringField('Previsão de entrega')
    prazofixo       = StringField('Quantidade de repetidora:')
    envorcamento    = StringField('Quantidade de terminais:')

    medcmprevisto   = StringField('Programação de Início Atividade:')
    guiacmgerado = StringField('Fim de Atividade em Campo:')
    medesquadprevisto = StringField('Início de atividade em Campo:')

    statusprojeto = StringField('Status do Projeto:', validators=[DataRequired()])
    datapedidoperfil = StringField('Gestor Responsável:')
    guiaesquadgerado = StringField('Equipe Responsável:')

    datapedidovidro = StringField('yy')
    medcmrealizado = StringField('xx')
    endereco                    = TextAreaField('Endereço:')
    crm                         = TextAreaField('Observação de Vendas:'                        )
    observacaocompra            = TextAreaField('Observações da área de compras:')
    observacaoinstalacao        = TextAreaField('Observação da área de instalaçao:')
    observacaoprojeto           = TextAreaField('Observação da área de projetos:')
    observacaoproducao          = TextAreaField('Observação da área de despacho')
    medesquadrealizado          = StringField('Data de Medição Esquadrias realizado:')
    datapedidoacessorio         = StringField('Data do Pedido do acessorio:')
    valorprojeto                = StringField('Valor do Projeto:')
    reserva1                    = StringField('Data Prevista de Entrega da Obra:')
    reserva2                    = StringField('Reserva 2:')
    reserva3                    = TextAreaField('Reserva 3:')
    reserva4                    = TextAreaField('Reserva 4:')
    detalhe3_prevenda           = BooleanField('Pré Venda')
    detalhe3_aprovado                   = BooleanField('Orçamento Aprovado')
    detalhe3_perdido                    = BooleanField('Orçamento Reprovado')
    detalhe4_marcelosilva               = BooleanField('Marcelo Silva')
    detalhe4_marciocampos               = BooleanField('Márcio Campos')
    detalhe1_geovany                    = BooleanField('Geovany')
    detalhe1_wellington                 = BooleanField('Wellington')
    detalhe1_nelson                     = BooleanField('Nelson')
    detalhe1_rogerio                    = BooleanField('Rogério')
    detalhe1_jesse                      = BooleanField('Jessé')
    detalhe1_fernando                   = BooleanField('Fernando')
    detalhe1_douglas                    = BooleanField('Douglas')
    detalhe1_thiago                     = BooleanField('Thiago')
    detalhe1_valdir                     = BooleanField('Valdir')
    detalhe1_valdinei = BooleanField('Equipe Valdinei')
    detalhe2_corretiva                  = BooleanField('Corretiva')
    detalhe2_preventiva                 = BooleanField('Preventiva')
    detalhe2_implantacao                = BooleanField('Implantação')
    detalhe2_fornecimento               = BooleanField('Fornecimento')
    detalhe2_curtaduracao               = BooleanField('Curta Duração')
    detalhe2_substituicao               = BooleanField('Substituição')
    detalhe4_elisio           = BooleanField('Elísio')
    detalhe4_amaury                  = BooleanField('Amaury Junior')
    detalhe4_claudemir         = BooleanField('Claudenir')
    detalhe4_araujo                     = BooleanField('Araújo')
    botao_submit_criarprojeto           = SubmitField('Criar Projeto')
    botao_submit_1_Medição = SubmitField('Programado')
    botao_submit_2_Medição = SubmitField('Concluídos')
    botao_submit_producaocm = SubmitField('Corretivas')
    botao_submit_producaoesquad = SubmitField('Pré-Venda')
    botao_submit_guiafabricacao = SubmitField('Preventivas')
    botao_submit_produzido = SubmitField('Amaury Junior')
    botao_submit_retrabalho = SubmitField('Claudenir')
    botao_submit_eminstalacao = SubmitField('Elísio')
    botao_submit_import = SubmitField('Araújo')
    botao_submit_export = SubmitField('Marcelo')
    botao_submit_pendente = SubmitField('Campos')
    botao_submit_curtaduracao = SubmitField ('Curta Duração')
    botao_submit_substituicao = SubmitField('Substituição')

    #def validate_mbes(self,mbes):
        #mbes = CadastrarProjetoVendas.query.filter_by(mbes=mbes.data). first()
        #if mbes:
            #raise ValidationError('MBES já cadastrado, cadastre outro MBES')
