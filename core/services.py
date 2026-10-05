"""Regras de negócio do sistema."""
import re
from datetime import datetime
from . import banco, config


# ============ VALIDAÇÕES ============
def validar_email(email):
    if not email or not email.strip():
        return False, "O e-mail não pode estar vazio."
    padrao = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if re.match(padrao, email.strip()):
        return True, "E-mail válido."
    return False, "Formato de e-mail inválido."


def validar_senha(senha):
    if not senha or not senha.strip():
        return False, "A senha não pode estar vazia."
    if len(senha) < config.MIN_SENHA:
        return False, f"A senha deve ter no mínimo {config.MIN_SENHA} caracteres."
    return True, "Senha válida."


def validar_data(data):
    try:
        datetime.strptime(data, "%Y-%m-%d")
        return True, "Data válida."
    except (ValueError, AttributeError):
        return False, "Data inválida."


def validar_campo(valor, nome_campo):
    if valor is None or (isinstance(valor, str) and not valor.strip()):
        return False, f"O campo '{nome_campo}' não pode estar vazio."
    return True, "OK"


# ============ AUTENTICAÇÃO ============
def cadastrar_usuario(nome, email, senha, turma, tipo="publico"):
    ok, msg = validar_campo(nome, "nome")
    if not ok:
        return False, msg, None
    ok, msg = validar_email(email)
    if not ok:
        return False, msg, None
    ok, msg = validar_senha(senha)
    if not ok:
        return False, msg, None
    if tipo not in config.TIPOS_AUTOCADASTRO:
        return False, "Tipo inválido para autocadastro.", None
    if banco.buscar_usuario_por_email(email.strip()):
        return False, "E-mail já cadastrado.", None
    u = banco.criar_usuario(nome.strip(), email.strip(), senha, turma, tipo)
    return True, "Usuário cadastrado com sucesso!", u.id


def fazer_login(email, senha):
    usuario = banco.autenticar(email.strip(), senha)
    if usuario:
        return usuario, "Login realizado com sucesso!"
    return None, "E-mail ou senha incorretos."


# ============ PROJETOS ============
def cadastrar_projeto(titulo, descricao, area, tecnologias, usuario_id, ano):
    ok, msg = validar_campo(titulo, "título")
    if not ok:
        return False, msg
    ok, msg = validar_campo(descricao, "descrição")
    if not ok:
        return False, msg
    if len(descricao) < config.MIN_DESCRICAO:
        return False, f"A descrição deve ter pelo menos {config.MIN_DESCRICAO} caracteres."
    if area not in config.AREAS_PROJETO:
        return False, f"Área inválida. Use: {', '.join(config.AREAS_PROJETO)}"
    try:
        ano_int = int(ano)
    except (ValueError, TypeError):
        return False, "Ano inválido."
    p = banco.inserir_projeto(titulo, descricao, area, tecnologias, usuario_id, ano_int)
    if not p:
        return False, "Erro ao cadastrar projeto."
    return True, f"Projeto #{p.id} cadastrado com sucesso."


def remover_projeto(projeto_id, usuario_id, tipo_usuario):
    projeto = banco.buscar_projeto_por_id(projeto_id)
    if not projeto:
        return False, "Projeto não encontrado."
    if projeto.usuario_id != usuario_id and tipo_usuario != "coordenador":
        return False, "Sem permissão para remover este projeto."
    if banco.deletar_projeto(projeto_id):
        return True, "Projeto removido."
    return False, "Erro ao remover."


def buscar_projetos(termo=None, area=None):
    if termo:
        return list(banco.buscar_projetos_por_termo(termo))
    qs = banco.listar_projetos()
    if area:
        qs = qs.filter(area=area)
    return list(qs)


def listar_projetos_por_usuario(usuario_id):
    return list(banco.listar_projetos_por_usuario(usuario_id))


def obter_detalhes_projeto(projeto_id):
    p = banco.buscar_projeto_por_id(projeto_id)
    if not p:
        return None
    return {"projeto": p, "media": banco.media_projeto(projeto_id)}


def obter_ranking(limite=10):
    return list(banco.ranking_projetos(limite))


def listar_usuarios():
    return list(banco.listar_usuarios())


# ============ AVALIAÇÕES ============
def avaliar_projeto(usuario_id, projeto_id, nota, comentario):
    try:
        nota = int(nota)
    except (ValueError, TypeError):
        return False, "A nota deve ser um número inteiro."
    if not config.NOTA_MIN <= nota <= config.NOTA_MAX:
        return False, f"A nota deve estar entre {config.NOTA_MIN} e {config.NOTA_MAX}."
    projeto = banco.buscar_projeto_por_id(projeto_id)
    if not projeto:
        return False, "Projeto não encontrado."
    if projeto.usuario_id == usuario_id:
        return False, "Você não pode avaliar seu próprio projeto."
    if banco.ja_avaliou(usuario_id, projeto_id):
        return False, "Você já avaliou este projeto."
    if banco.inserir_avaliacao(usuario_id, projeto_id, nota, comentario):
        return True, "Avaliação registrada."
    return False, "Erro ao registrar avaliação."


# ============ SALAS ============
def listar_salas_agrupadas():
    salas = banco.listar_salas()
    agrupadas = {}
    for s in salas:
        agrupadas.setdefault(s.andar, []).append(s)
    return agrupadas


def cadastrar_sala(nome, andar, capacidade, tipo, usuario_id):
    u = banco.buscar_usuario_por_id(usuario_id)
    if not u or u.tipo != "coordenador":
        return False, "Apenas coordenadores podem cadastrar salas."
    ok, msg = validar_campo(nome, "nome")
    if not ok:
        return False, msg
    if tipo not in config.TIPOS_SALA:
        return False, f"Tipo inválido. Use: {', '.join(config.TIPOS_SALA)}"
    try:
        andar = int(andar)
        capacidade = int(capacidade)
    except (ValueError, TypeError):
        return False, "Andar e capacidade devem ser números."
    if capacidade <= 0:
        return False, "Capacidade deve ser maior que zero."
    s = banco.inserir_sala(nome, andar, capacidade, tipo)
    if not s:
        return False, "Erro ao cadastrar sala."
    return True, f"Sala #{s.id} cadastrada com sucesso."


def desativar_sala(sala_id, usuario_id):
    u = banco.buscar_usuario_por_id(usuario_id)
    if not u or u.tipo != "coordenador":
        return False, "Apenas coordenadores podem desativar salas."
    if banco.desativar_sala(sala_id):
        return True, "Sala desativada."
    return False, "Sala não encontrada."


def obter_grade_horarios(sala_id, data):
    sala = banco.buscar_sala_por_id(sala_id)
    if not sala:
        return None
    grade = []
    for h in config.HORARIOS:
        livre = banco.verificar_disponibilidade(sala_id, data, h)
        grade.append({"horario": h, "status": "LIVRE" if livre else "OCUPADO"})
    return grade


# ============ RESERVAS ============
def reservar_sala(usuario_id, sala_id, data, horario, motivo):
    u = banco.buscar_usuario_por_id(usuario_id)
    if not u:
        return False, "Usuário não encontrado."
    if not u.pode_reservar:
        return False, "Apenas professores e coordenadores podem reservar."
    sala = banco.buscar_sala_por_id(sala_id)
    if not sala or sala.status != "ATIVA":
        return False, "Sala inexistente ou inativa."
    if horario not in config.HORARIOS:
        return False, "Horário inválido."
    ok, msg = validar_data(data)
    if not ok:
        return False, msg
    if not banco.verificar_disponibilidade(sala_id, data, horario):
        return False, "Horário já reservado."
    r = banco.inserir_reserva(sala_id, usuario_id, data, horario, motivo)
    if not r:
        return False, "Erro ao reservar."
    return True, f"Reserva #{r.id} criada com sucesso."


def cancelar_reserva(reserva_id, usuario_id, tipo_usuario):
    r = banco.buscar_reserva_por_id(reserva_id)
    if not r:
        return False, "Reserva não encontrada."
    if r.status != "ativa":
        return False, "Reserva já cancelada."
    if r.usuario_id != usuario_id and tipo_usuario != "coordenador":
        return False, "Sem permissão para cancelar."
    if banco.cancelar_reserva(reserva_id):
        return True, "Reserva cancelada."
    return False, "Erro ao cancelar."


def listar_minhas_reservas(usuario_id):
    return list(banco.listar_reservas_usuario(usuario_id))


def listar_todas_reservas():
    return list(banco.listar_todas_reservas())


# ============ RELATÓRIOS ============
def exportar_csv():
    import csv, os
    from django.conf import settings
    relatorio = os.path.join(settings.BASE_DIR, "data", "relatorio.csv")
    try:
        os.makedirs(os.path.dirname(relatorio), exist_ok=True)
        with open(relatorio, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Tipo", "ID", "Título/Sala", "Autor/Usuário", "Data/Horário", "Detalhes"])
            for p in banco.listar_projetos():
                media = banco.media_projeto(p.id)
                w.writerow(["Projeto", p.id, p.titulo, p.usuario.first_name, "", f"Média: {media:.2f}"])
            for r in banco.listar_todas_reservas():
                w.writerow(["Reserva", r.id, r.sala.nome, r.usuario.first_name,
                            f"{r.data} {r.horario}", r.motivo])
        return True, f"Relatório salvo em {relatorio}."
    except Exception as e:
        return False, f"Erro ao exportar: {e}"
