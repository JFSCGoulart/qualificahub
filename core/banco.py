"""Operações de banco de dados usando o ORM do Django."""
from django.db.models import Avg, Count, Q
from .models import Usuario, Projeto, Avaliacao, Sala, Reserva


# ============ USUÁRIOS ============
def buscar_usuario_por_email(email):
    return Usuario.objects.filter(email=email).first()


def buscar_usuario_por_id(uid):
    return Usuario.objects.filter(id=uid).first()


def listar_usuarios():
    return Usuario.objects.all().order_by("id")


def atualizar_tipo_usuario(uid, novo_tipo):
    return Usuario.objects.filter(id=uid).update(tipo=novo_tipo) > 0


def criar_usuario(nome, email, senha, turma, tipo):
    username = email.split("@")[0]
    base = username
    contador = 1
    while Usuario.objects.filter(username=username).exists():
        username = f"{base}{contador}"
        contador += 1
    return Usuario.objects.create_user(
        username=username, email=email, password=senha,
        first_name=nome, turma=turma, tipo=tipo
    )


def autenticar(email, senha):
    try:
        user = Usuario.objects.get(email=email)
        if user.check_password(senha):
            return user
    except Usuario.DoesNotExist:
        pass
    return None


# ============ PROJETOS ============
def inserir_projeto(titulo, descricao, area, tecnologias, usuario_id, ano):
    u = buscar_usuario_por_id(usuario_id)
    if not u:
        return None
    return Projeto.objects.create(
        titulo=titulo, descricao=descricao, area=area,
        tecnologias=tecnologias, usuario=u, ano=ano
    )


def buscar_projeto_por_id(pid):
    return Projeto.objects.filter(id=pid).first()


def listar_projetos():
    return Projeto.objects.select_related("usuario").all()


def listar_projetos_por_usuario(uid):
    return Projeto.objects.filter(usuario_id=uid)


def atualizar_projeto(pid, **kwargs):
    return Projeto.objects.filter(id=pid).update(**kwargs) > 0


def deletar_projeto(pid):
    return Projeto.objects.filter(id=pid).delete()[0] > 0


def buscar_projetos_por_termo(termo):
    return Projeto.objects.filter(
        Q(titulo__icontains=termo) | Q(tecnologias__icontains=termo)
    ).select_related("usuario")


# ============ AVALIAÇÕES ============
def inserir_avaliacao(usuario_id, projeto_id, nota, comentario):
    u = buscar_usuario_por_id(usuario_id)
    p = buscar_projeto_por_id(projeto_id)
    if not u or not p:
        return False
    Avaliacao.objects.create(usuario=u, projeto=p, nota=nota, comentario=comentario)
    return True


def ja_avaliou(usuario_id, projeto_id):
    return Avaliacao.objects.filter(usuario_id=usuario_id, projeto_id=projeto_id).exists()


def media_projeto(pid):
    result = Avaliacao.objects.filter(projeto_id=pid).aggregate(media=Avg("nota"))
    return float(result["media"]) if result["media"] else 0.0


def ranking_projetos(limite=10):
    return (
        Projeto.objects
        .select_related("usuario")
        .annotate(total=Count("avaliacoes"), media=Avg("avaliacoes__nota"))
        .filter(total__gt=0)
        .order_by("-media", "-total")[:limite]
    )


# ============ SALAS ============
def inserir_sala(nome, andar, capacidade, tipo):
    return Sala.objects.create(nome=nome, andar=andar, capacidade=capacidade, tipo=tipo)


def buscar_sala_por_id(sid):
    return Sala.objects.filter(id=sid).first()


def listar_salas():
    return Sala.objects.filter(status="ATIVA")


def listar_salas_por_andar(andar):
    return Sala.objects.filter(andar=andar, status="ATIVA")


def desativar_sala(sid):
    return Sala.objects.filter(id=sid).update(status="DESATIVADA") > 0


# ============ RESERVAS ============
def inserir_reserva(sala_id, usuario_id, data, horario, motivo):
    s = buscar_sala_por_id(sala_id)
    u = buscar_usuario_por_id(usuario_id)
    if not s or not u:
        return None
    return Reserva.objects.create(sala=s, usuario=u, data=data, horario=horario, motivo=motivo)


def verificar_disponibilidade(sala_id, data, horario):
    return not Reserva.objects.filter(
        sala_id=sala_id, data=data, horario=horario, status="ativa"
    ).exists()


def buscar_reserva_por_id(rid):
    return Reserva.objects.filter(id=rid).first()


def listar_reservas_usuario(uid):
    return Reserva.objects.filter(usuario_id=uid, status="ativa").select_related("sala")


def listar_todas_reservas():
    return Reserva.objects.all().select_related("sala", "usuario")


def cancelar_reserva(rid):
    return Reserva.objects.filter(id=rid).update(status="cancelada") > 0


# ============ DADOS DE TESTE ============
def inserir_dados_teste():
    if Usuario.objects.exists():
        return
    admin = Usuario.objects.create_superuser(
        username="admin", email="admin@qualifica.com", password="123456",
        first_name="Coordenador", tipo="coordenador"
    )
    joao = Usuario.objects.create_user(
        username="joao", email="joao@qualifica.com", password="123456",
        first_name="João Silva", turma="Turma A", tipo="professor"
    )
    maria = Usuario.objects.create_user(
        username="maria", email="maria@qualifica.com", password="123456",
        first_name="Maria Santos", turma="Turma A", tipo="publico"
    )
    pedro = Usuario.objects.create_user(
        username="pedro", email="pedro@qualifica.com", password="123456",
        first_name="Pedro Oliveira", turma="Turma B", tipo="publico"
    )

    p1 = Projeto.objects.create(
        titulo="Sistema de Biblioteca",
        descricao="Sistema para gerenciamento de livros e empréstimos.",
        area="Outros", tecnologias="Python, SQLite, Flask", usuario=maria, ano=2026
    )
    p2 = Projeto.objects.create(
        titulo="Aplicativo Educacional",
        descricao="Aplicativo para auxiliar alunos nos estudos.",
        area="Educação", tecnologias="Python, JavaScript", usuario=pedro, ano=2026
    )
    p3 = Projeto.objects.create(
        titulo="Controle de Estoque",
        descricao="Sistema para controle de produtos e estoque.",
        area="Financeiro", tecnologias="Python, SQLite", usuario=maria, ano=2026
    )

    Avaliacao.objects.create(usuario=joao, projeto=p1, nota=5, comentario="Excelente projeto.")
    Avaliacao.objects.create(usuario=joao, projeto=p2, nota=4, comentario="Boa ideia.")
    Avaliacao.objects.create(usuario=maria, projeto=p3, nota=5, comentario="Projeto muito útil.")

    s1 = Sala.objects.create(nome="Sala 101", andar=1, capacidade=30, tipo="sala_aula")
    Sala.objects.create(nome="Sala 102", andar=1, capacidade=30, tipo="sala_aula")
    s3 = Sala.objects.create(nome="Laboratório 103", andar=1, capacidade=20, tipo="laboratorio")
    Sala.objects.create(nome="Sala 201", andar=2, capacidade=40, tipo="sala_aula")
    Sala.objects.create(nome="Laboratório 202", andar=2, capacidade=25, tipo="laboratorio")
    Sala.objects.create(nome="Auditório 301", andar=3, capacidade=50, tipo="auditorio")

    from datetime import date
    Reserva.objects.create(sala=s1, usuario=admin, data=date(2026, 10, 1),
                           horario="08:00 - 09:00", motivo="Aula de programação")
    Reserva.objects.create(sala=s3, usuario=joao, data=date(2026, 10, 1),
                           horario="14:00 - 15:00", motivo="Aula prática")
