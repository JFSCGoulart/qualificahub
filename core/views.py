from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib import messages
from . import services, config, banco
from .decorators import requer_login, requer_coordenador, requer_professor_ou_coordenador


# ============ PÚBLICAS ============
def home(request):
    return render(request, "core/menu.html")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        senha = request.POST.get("senha", "")
        usuario, msg = services.fazer_login(email, senha)
        if usuario:
            auth_login(request, usuario)
            messages.success(request, f"Bem-vindo(a), {usuario.first_name}!")
            return redirect("home")
        messages.error(request, msg)
    return render(request, "core/login.html")


def logout_view(request):
    auth_logout(request)
    messages.info(request, "Sessão encerrada.")
    return redirect("home")


def cadastro_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        nome = request.POST.get("nome", "").strip()
        email = request.POST.get("email", "").strip()
        senha = request.POST.get("senha", "")
        turma = request.POST.get("turma", "").strip()
        tipo = request.POST.get("tipo", "publico")
        sucesso, msg, _ = services.cadastrar_usuario(nome, email, senha, turma, tipo)
        if sucesso:
            messages.success(request, msg)
            return redirect("login")
        messages.error(request, msg)
    return render(request, "core/cadastro.html", {"tipos": config.TIPOS_AUTOCADASTRO})


def buscar_publico_view(request):
    termo = request.GET.get("termo", "").strip()
    resultados = services.buscar_projetos(termo=termo if termo else None)
    return render(request, "core/buscar_publico.html",
                  {"resultados": resultados, "termo": termo})


def ranking_view(request):
    ranking = services.obter_ranking(10)
    return render(request, "core/ranking.html", {"ranking": ranking})


def ver_salas_view(request):
    agrupadas = services.listar_salas_agrupadas()
    return render(request, "core/ver_salas.html",
                  {"salas": agrupadas, "andares": config.ANDARES})


# ============ PROJETOS ============
@requer_professor_ou_coordenador
def cadastrar_projeto_view(request):
    if request.method == "POST":
        sucesso, msg = services.cadastrar_projeto(
            request.POST.get("titulo"), request.POST.get("descricao"),
            request.POST.get("area"), request.POST.get("tecnologias"),
            request.user.id, request.POST.get("ano")
        )
        messages.success(request, msg) if sucesso else messages.error(request, msg)
        if sucesso:
            return redirect("meus_projetos")
    return render(request, "core/cadastrar_projeto.html", {"areas": config.AREAS_PROJETO})


@requer_login
def meus_projetos_view(request):
    projetos = services.listar_projetos_por_usuario(request.user.id)
    return render(request, "core/meus_projetos.html", {"projetos": projetos})


@requer_login
def remover_projeto_view(request, projeto_id):
    sucesso, msg = services.remover_projeto(
        projeto_id, request.user.id, request.user.tipo
    )
    messages.success(request, msg) if sucesso else messages.error(request, msg)
    return redirect("meus_projetos")


@requer_login
def avaliar_view(request):
    if request.method == "POST":
        sucesso, msg = services.avaliar_projeto(
            request.user.id, request.POST.get("projeto_id"),
            request.POST.get("nota"), request.POST.get("comentario")
        )
        messages.success(request, msg) if sucesso else messages.error(request, msg)
        return redirect("avaliar")
    projetos = [p for p in services.buscar_projetos() if p.usuario_id != request.user.id]
    return render(request, "core/avaliar.html", {"projetos": projetos})


# ============ SALAS ============
@requer_coordenador
def gerenciar_salas_view(request):
    if request.method == "POST":
        acao = request.POST.get("acao")
        if acao == "cadastrar":
            sucesso, msg = services.cadastrar_sala(
                request.POST.get("nome"), request.POST.get("andar"),
                request.POST.get("capacidade"), request.POST.get("tipo"),
                request.user.id
            )
        elif acao == "desativar":
            sucesso, msg = services.desativar_sala(request.POST.get("sala_id"), request.user.id)
        else:
            sucesso, msg = False, "Ação desconhecida."
        messages.success(request, msg) if sucesso else messages.error(request, msg)
        return redirect("gerenciar_salas")
    salas = banco.listar_salas()
    return render(request, "core/gerenciar_salas.html",
                  {"tipos": config.TIPOS_SALA, "salas": salas})


# ============ RESERVAS ============
@requer_professor_ou_coordenador
def reservar_sala_view(request):
    if request.method == "POST":
        sucesso, msg = services.reservar_sala(
            request.user.id, request.POST.get("sala_id"),
            request.POST.get("data"), request.POST.get("horario"),
            request.POST.get("motivo")
        )
        messages.success(request, msg) if sucesso else messages.error(request, msg)
        if sucesso:
            return redirect("minhas_reservas")
    return render(request, "core/reservar_sala.html",
                  {"horarios": config.HORARIOS, "salas": banco.listar_salas()})


@requer_login
def minhas_reservas_view(request):
    reservas = services.listar_minhas_reservas(request.user.id)
    return render(request, "core/minhas_reservas.html", {"reservas": reservas})


@requer_login
def cancelar_reserva_view(request, reserva_id):
    sucesso, msg = services.cancelar_reserva(
        reserva_id, request.user.id, request.user.tipo
    )
    messages.success(request, msg) if sucesso else messages.error(request, msg)
    return redirect("minhas_reservas")


@requer_coordenador
def todas_reservas_view(request):
    reservas = services.listar_todas_reservas()
    return render(request, "core/todas_reservas.html", {"reservas": reservas})


# ============ USUÁRIOS ============
@requer_coordenador
def listar_usuarios_view(request):
    usuarios = services.listar_usuarios()
    return render(request, "core/listar_usuarios.html", {"usuarios": usuarios})


# ============ RELATÓRIOS ============
@requer_coordenador
def exportar_csv_view(request):
    sucesso, msg = services.exportar_csv()
    messages.success(request, msg) if sucesso else messages.error(request, msg)
    return redirect("home")
