from flask import render_template, redirect, url_for, flash, request, abort
from comunidadeimpressionadora import app, database, bcrypt
from comunidadeimpressionadora.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost, FormCadastroVendas
from comunidadeimpressionadora.models import Usuario, Post, CadastrarProjetoVendas
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image
import pandas as pd






@app.route('/')
@login_required
def home():
    projetos = CadastrarProjetoVendas.query.all()
    return render_template('home.html', projetos=projetos)


@app.route('/usuarios')
@login_required
def usuarios():
    form = FormEditarPerfil()
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and usuario.senha == form_login.senha.data:
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'Login feito com sucesso no e-mail: {form_login.email.data}', 'alert-success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
        else:
            flash(f'Falha no Login. E-mail ou Senha Incorretos', 'alert-danger')
    return render_template('login.html', form_login=form_login,)


@app.route('/criarconta', methods=['GET', 'POST'])
@login_required
def criarconta():
    form_criarconta = FormCriarConta()
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        usuario = Usuario.query.filter_by(email=form_criarconta.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_criarconta.senha.data):
            login_user(usuario, remember=form_criarconta.lembrar_dados.data)
            flash(f'Cadastro feito com sucesso no e-mail: {form_criarconta.email.data}', 'alert-success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        #senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data)
        usuario = Usuario( username=form_criarconta.username.data, email=form_criarconta.email.data, senha=form_criarconta.senha.data)
        database.session.add(usuario)
        database.session.commit()
        flash(f'Conta criada para o e-mail: {form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criarconta.html', form_criarconta=form_criarconta)


def lista_detalhe(form_cadastrovendas):
    lista_detalhe = []
    for campo in form_cadastrovendas:
        if 'detalhe' in campo.name:
            if campo.data:
                lista_detalhe.append(campo.label.text)
    return ';'.join(lista_detalhe)



@app.route('/cadastrarprojetovendas', methods=['GET', 'POST'])
@login_required
def cadastrarprojetovendas():
    form_cadastrovendas = FormCadastroVendas()
    if  form_cadastrovendas.validate_on_submit() and 'botao_submit_criarprojeto' in request.form:
        projetos=CadastrarProjetoVendas(mbes=form_cadastrovendas.mbes.data,
                                        vendedor            =form_cadastrovendas.vendedor.data,
                                        cliente             =form_cadastrovendas.cliente.data,
                                        endereco            =form_cadastrovendas.endereco.data,
                                        email               =form_cadastrovendas.email.data,
                                        telefone            =form_cadastrovendas.telefone.data,
                                        datacm              =form_cadastrovendas.datacm.data,
                                        dataesquad          =form_cadastrovendas.dataesquad.data,
                                        datacontrato        =form_cadastrovendas.datacontrato.data,
                                        prazofixo           =form_cadastrovendas.prazofixo.data,
                                        crm                 =form_cadastrovendas.crm.data,
                                        observacaocompra    =form_cadastrovendas.observacaocompra.data,
                                        observacaoinstalacao=form_cadastrovendas.observacaoinstalacao.data,
                                        observacaoprojeto   =form_cadastrovendas.observacaoprojeto.data,
                                        observacaoproducao  =form_cadastrovendas.observacaoproducao.data,
                                        numorcamento        =form_cadastrovendas.numorcamento.data,
                                        solorcamento        =form_cadastrovendas.solorcamento.data,
                                        envorcamento        =form_cadastrovendas.envorcamento.data,
                                        medcmprevisto       =form_cadastrovendas.medcmprevisto.data,
                                        medcmrealizado      =form_cadastrovendas.medcmrealizado.data,
                                        medesquadprevisto   =form_cadastrovendas.medesquadprevisto.data,
                                        medesquadrealizado  =form_cadastrovendas.medesquadrealizado.data,
                                        guiacmgerado        =form_cadastrovendas.guiacmgerado.data,
                                        guiaesquadgerado    =form_cadastrovendas.guiaesquadgerado.data,
                                        datapedidovidro     =form_cadastrovendas.datapedidovidro.data,
                                        datapedidoperfil    =form_cadastrovendas.datapedidoperfil.data,
                                        datapedidoacessorio =form_cadastrovendas.datapedidoacessorio.data,
                                        statusprojeto       =form_cadastrovendas.statusprojeto.data,
                                        valorprojeto        =form_cadastrovendas.valorprojeto.data,
                                        reserva1            =form_cadastrovendas.reserva1.data,
                                        reserva2            =form_cadastrovendas.reserva2.data,
                                        reserva3            =form_cadastrovendas.reserva3.data,
                                        reserva4            =form_cadastrovendas.reserva4.data)
        projetos.detalhes = lista_detalhe(form_cadastrovendas)
        database.session.add(projetos)
        database.session.commit()
        flash(f'Cadastro feito com sucesso para o MBES: {form_cadastrovendas.mbes.data}', 'alert-success')
        return redirect(url_for('home'))
    return render_template('cadastrarprojetovendas.html',form_cadastrovendas=form_cadastrovendas)





@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout Feito com Sucesso', 'alert-success')
    return redirect(url_for('home'))


@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', foto_perfil=foto_perfil)


@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post Criado com Sucesso', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criarpost.html', form=form)


def salvar_imagem(imagem):
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    tamanho = (400, 400)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo


def atualizar_cursos(form):
    lista_cursos = []
    for campo in form:
        if 'curso_' in campo.name:
            if campo.data:
                lista_cursos.append(campo.label.text)
        if 'habilitacao' in campo.name:
            if campo.data:
                lista_cursos.append(campo.label.text)
    return ';'.join(lista_cursos)


@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        current_user.senha = form.senha.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        current_user.cursos = atualizar_cursos(form)
        database.session.commit()
        flash('Perfil atualizado com Sucesso', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == "GET":
        form.email.data = current_user.email
        form.username.data = current_user.username
        form.senha.data = current_user.senha
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)


@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form = FormCriarPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash('Post Atualizado com Sucesso', 'alert-success')
            return redirect(url_for('home'))
    else:
        form = None
    return render_template('post.html', post=post, form=form)


@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post Excluído com Sucesso', 'alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403)

@app.route('/exibirprojetos', methods=['GET', 'POST'])
@login_required
def exibir_projeto():
    projetos = CadastrarProjetoVendas.query.all()
    xyz=""
    medicao = 0
    medicao1 = 0
    medicao2 = 0
    medicao3 = 0
    medicao4 = 0
    medicao5 = 0
    medicao6 = 0
    medicao7 = 0
    medicao8 = 0
    medicao9 = 0
    medicao10 = 0
    medicao11 = 0
    medicao12 = 0
    medicao13 = 0
    for projeto in projetos:
        if projeto.statusprojeto == 'Programado':
            medicao = medicao + 1
        if projeto.statusprojeto == 'Concluído':
            medicao1 = medicao1 + 1
        for detalhe in projeto.detalhes.split(';'):
            if 'Corretiva' in detalhe and projeto.statusprojeto != 'Concluído':
                medicao2 = medicao2 + 1
        if projeto.statusprojeto == 'xxx':
            medicao4 = medicao4 + 1
        for detalhe in projeto.detalhes.split(';'):
            if 'Preventiva' in detalhe and projeto.statusprojeto != 'Concluído':
                medicao5 = medicao5 + 1
        for detalhe in projeto.detalhes.split(';'):
            if 'Amaury Junior' in detalhe and projeto.statusprojeto != 'Concluído':
                medicao6 = medicao6 + 1
        for detalhe in projeto.detalhes.split(';'):
            if 'Claudenir' in detalhe and projeto.statusprojeto != 'Concluído':
                medicao7 = medicao7 + 1

        for detalhe in projeto.detalhes.split(';'):
            if 'Pré Venda' in detalhe and projeto.statusprojeto != 'Concluído':
                medicao3 = medicao3 + 1

        for detalhe in projeto.detalhes.split(';'):
            if 'Elísio' in detalhe and projeto.statusprojeto != 'Concluído':
                medicao8 = medicao8 + 1

        for detalhe in projeto.detalhes.split(';'):
            if 'Araújo' in detalhe and projeto.statusprojeto != 'Concluído':
                medicao9 = medicao9 + 1

        for detalhe in projeto.detalhes.split(';'):
            if 'Marcelo' in detalhe and projeto.statusprojeto != 'Concluído':
                medicao10 = medicao10 + 1

        for detalhe in projeto.detalhes.split(';'):
            if 'Campos' in detalhe and projeto.statusprojeto != 'Concluído':
                medicao11 = medicao11 + 1

        for detalhe in projeto.detalhes.split(';'):
            if 'Curta Duração' in detalhe and projeto.statusprojeto != 'Concluído':
                medicao12 = medicao12 + 1

        for detalhe in projeto.detalhes.split(';'):
            if 'Substituição' in detalhe and projeto.statusprojeto != 'Concluído':
                medicao13 = medicao13 + 1



    form_cadastrovendas = FormCadastroVendas()
    if 'botao_submit_1_Medição' in request.form:
        projetos = CadastrarProjetoVendas.query.filter_by(statusprojeto='Programado')
        xyz='Programado'
    if 'botao_submit_2_Medição' in request.form:
        projetos = CadastrarProjetoVendas.query.filter_by(statusprojeto='Concluído')
        xyz = 'Concluído'
    if 'botao_submit_producaocm' in request.form:
        projetos = CadastrarProjetoVendas.query.all()
        xyz = 'Corretiva'
    if 'botao_submit_producaoesquad' in request.form:
        projetos = CadastrarProjetoVendas.query.all()
        xyz = 'Projetos em Pré-Venda'
    if 'botao_submit_guiafabricacao' in request.form:
        projetos = CadastrarProjetoVendas.query.all()
        xyz = 'Preventiva'
    if 'botao_submit_retrabalho' in request.form:
        projetos = CadastrarProjetoVendas.query.all()
        xyz = 'Claudenir'
    if 'botao_submit_pendente' in request.form:
        projetos = CadastrarProjetoVendas.query.all()
        xyz="Pintura Especial"
    if 'botao_submit_eminstalacao' in request.form:
        projetos = CadastrarProjetoVendas.query.all()
        xyz = 'Elísio'
    if 'botao_submit_produzido' in request.form:
        projetos = CadastrarProjetoVendas.query.all()
        xyz = 'Amaury Junior'
    if 'botao_submit_import' in request.form:
        projetos = CadastrarProjetoVendas.query.all()
        xyz = 'Araújo'
    if 'botao_submit_export' in request.form:
        projetos = CadastrarProjetoVendas.query.all()
        xyz = 'Marcelo'
    if 'botao_submit_pendente' in request.form:
        projetos = CadastrarProjetoVendas.query.all()
        xyz = 'Campos'
    if 'botao_submit_curtaduracao' in request.form:
        projetos = CadastrarProjetoVendas.query.all()
        xyz = 'Curta Duração'
    if 'botao_submit_substituicao' in request.form:
        xyz = 'Substituição'


    return render_template('exibir_projeto.html', form_cadastrovendas=form_cadastrovendas, projetos=projetos
                           , xyz=xyz, medicao=medicao, medicao1=medicao1,medicao2=medicao2,medicao3=medicao3,
                           medicao4=medicao4, medicao5=medicao5, medicao6=medicao6, medicao7=medicao7, medicao8=medicao8,
                           medicao9=medicao9, medicao10=medicao10, medicao11=medicao11, medicao12=medicao12, medicao13=medicao13)


@app.route('/editarprojeto/<id_mbes>', methods=['GET', 'POST'])
@login_required
def editar_projeto(id_mbes):
    editarprojeto=CadastrarProjetoVendas.query.get(id_mbes)
    form_cadastrovendas=FormCadastroVendas()
    if request.method =='GET':
        form_cadastrovendas.mbes.data=editarprojeto.mbes
        form_cadastrovendas.cliente.data = editarprojeto.cliente
        form_cadastrovendas.email.data = editarprojeto.email
        form_cadastrovendas.telefone.data = editarprojeto.telefone
        form_cadastrovendas.datacontrato.data = editarprojeto.datacontrato
        form_cadastrovendas.datacm.data = editarprojeto.datacm
        form_cadastrovendas.dataesquad.data = editarprojeto.dataesquad
        form_cadastrovendas.prazofixo.data = editarprojeto.prazofixo
        form_cadastrovendas.vendedor.data = editarprojeto.vendedor
        form_cadastrovendas.crm.data = editarprojeto.crm
        form_cadastrovendas.observacaocompra.data = editarprojeto.observacaocompra
        form_cadastrovendas.observacaoinstalacao.data = editarprojeto.observacaoinstalacao
        form_cadastrovendas.observacaoprojeto.data = editarprojeto.observacaoprojeto
        form_cadastrovendas.observacaoproducao.data = editarprojeto.observacaoproducao
        form_cadastrovendas.endereco.data = editarprojeto.endereco
        form_cadastrovendas.numorcamento.data = editarprojeto.numorcamento
        form_cadastrovendas.reserva1.data = editarprojeto.reserva1
        form_cadastrovendas.solorcamento.data = editarprojeto.solorcamento
        form_cadastrovendas.envorcamento.data = editarprojeto.envorcamento
        form_cadastrovendas.medcmprevisto.data = editarprojeto.medcmprevisto
        form_cadastrovendas.medcmrealizado.data = editarprojeto.medcmrealizado
        form_cadastrovendas.medesquadprevisto.data = editarprojeto.medesquadprevisto
        form_cadastrovendas.medesquadrealizado.data = editarprojeto.medesquadrealizado
        form_cadastrovendas.guiacmgerado.data = editarprojeto.guiacmgerado
        form_cadastrovendas.guiaesquadgerado.data = editarprojeto.guiaesquadgerado
        form_cadastrovendas.datapedidovidro.data = editarprojeto.datapedidovidro
        form_cadastrovendas.datapedidoperfil.data = editarprojeto.datapedidoperfil
        form_cadastrovendas.datapedidoacessorio.data = editarprojeto.datapedidoacessorio
        form_cadastrovendas.statusprojeto.data = editarprojeto.statusprojeto
        form_cadastrovendas.valorprojeto.data = editarprojeto.valorprojeto
        form_cadastrovendas.reserva1.data = editarprojeto.reserva1
        form_cadastrovendas.reserva2.data = editarprojeto.reserva2
        form_cadastrovendas.reserva3.data = editarprojeto.reserva3
        form_cadastrovendas.reserva4.data = editarprojeto.reserva4
        for campo in form_cadastrovendas:
            if 'detalhe' in campo.name:
                if campo.label.text in editarprojeto.detalhes:
                    campo.data = True
    elif request.method =='POST':
        editarprojeto.mbes                  =form_cadastrovendas.mbes.data
        editarprojeto.cliente               =form_cadastrovendas.cliente.data
        editarprojeto.email                 =form_cadastrovendas.email.data
        editarprojeto.telefone              =form_cadastrovendas.telefone.data
        editarprojeto.datacontrato          =form_cadastrovendas.datacontrato.data
        editarprojeto.datacm                =form_cadastrovendas.datacm.data
        editarprojeto.dataesquad            =form_cadastrovendas.dataesquad.data
        editarprojeto.prazofixo             =form_cadastrovendas.prazofixo.data
        editarprojeto.vendedor              =form_cadastrovendas.vendedor.data
        editarprojeto.crm                   =form_cadastrovendas.crm.data
        editarprojeto.observacaocompra      = form_cadastrovendas.observacaocompra.data
        editarprojeto.observacaoinstalacao  = form_cadastrovendas.observacaoinstalacao.data
        editarprojeto.observacaoprojeto     = form_cadastrovendas.observacaoprojeto.data
        editarprojeto.observacaoproducao    =form_cadastrovendas.observacaoproducao.data
        editarprojeto.endereco              =form_cadastrovendas.endereco.data
        editarprojeto.numorcamento          =form_cadastrovendas.numorcamento.data
        editarprojeto.solorcamento          =form_cadastrovendas.solorcamento.data
        editarprojeto.envorcamento          =form_cadastrovendas.envorcamento.data
        editarprojeto.medcmprevisto         =form_cadastrovendas.medcmprevisto.data
        editarprojeto.medcmrealizado        =form_cadastrovendas.medcmrealizado.data
        editarprojeto.medesquadprevisto     =form_cadastrovendas.medesquadprevisto.data
        editarprojeto.medesquadrealizado    =form_cadastrovendas.medesquadrealizado.data
        editarprojeto.guiacmgerado          =form_cadastrovendas.guiacmgerado.data
        editarprojeto.guiaesquadgerado      =form_cadastrovendas.guiaesquadgerado.data
        editarprojeto.datapedidovidro       =form_cadastrovendas.datapedidovidro.data
        editarprojeto.datapedidoperfil      =form_cadastrovendas.datapedidoperfil.data
        editarprojeto.datapedidoacessorio   =form_cadastrovendas.datapedidoacessorio.data
        editarprojeto.statusprojeto         =form_cadastrovendas.statusprojeto.data
        editarprojeto.valorprojeto          =form_cadastrovendas.valorprojeto.data
        editarprojeto.reserva1              =form_cadastrovendas.reserva1.data
        editarprojeto.reserva2              =form_cadastrovendas.reserva2.data
        editarprojeto.reserva3              =form_cadastrovendas.reserva3.data
        editarprojeto.reserva4              =form_cadastrovendas.reserva4.data
        if lista_detalhe(form_cadastrovendas):
            editarprojeto.detalhes = lista_detalhe(form_cadastrovendas)
            database.session.commit()
            flash('Projeto atualizado com sucesso', 'alert-success')
        else:
            flash('Campos Status Comercial e Detalhes do Projeto estão vazios ', 'alert-danger')

        return redirect(url_for('exibir_projeto'))
    return render_template('editar_projeto.html', editarprojeto=editarprojeto, form_cadastrovendas=form_cadastrovendas)


