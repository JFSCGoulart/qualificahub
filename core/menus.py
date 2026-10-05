"""Menus e opções disponíveis por tipo de usuário."""


OPCOES_PUBLICAS = [
    {"nome": "Início", "url": "home", "icone": "home"},
    {"nome": "Buscar Projetos", "url": "buscar_publico", "icone": "search"},
    {"nome": "Ver Salas", "url": "ver_salas", "icone": "building"},
    {"nome": "Ranking", "url": "ranking", "icone": "star"},
]

OPCOES_PUBLICO = [
    {"nome": "Início", "url": "home", "icone": "home"},
    {"nome": "Buscar Projetos", "url": "buscar_publico", "icone": "search"},
    {"nome": "Ver Salas", "url": "ver_salas", "icone": "building"},
    {"nome": "Ranking", "url": "ranking", "icone": "star"},
]

OPCOES_PROFESSOR = [
    {"nome": "Início", "url": "home", "icone": "home"},
    {"nome": "Novo Projeto", "url": "cadastrar_projeto", "icone": "plus"},
    {"nome": "Meus Projetos", "url": "meus_projetos", "icone": "folder"},
    {"nome": "Reservar Sala", "url": "reservar_sala", "icone": "calendar"},
    {"nome": "Minhas Reservas", "url": "minhas_reservas", "icone": "list"},
    {"nome": "Avaliar", "url": "avaliar", "icone": "star"},
    {"nome": "Ranking", "url": "ranking", "icone": "trophy"},
]

OPCOES_COORDENADOR = [
    {"nome": "Início", "url": "home", "icone": "home"},
    {"nome": "Salas", "url": "gerenciar_salas", "icone": "building"},
    {"nome": "Reservas", "url": "todas_reservas", "icone": "calendar"},
    {"nome": "Usuários", "url": "listar_usuarios", "icone": "users"},
    {"nome": "Novo Projeto", "url": "cadastrar_projeto", "icone": "plus"},
    {"nome": "Meus Projetos", "url": "meus_projetos", "icone": "folder"},
    {"nome": "Reservar Sala", "url": "reservar_sala", "icone": "calendar"},
    {"nome": "Minhas Reservas", "url": "minhas_reservas", "icone": "list"},
    {"nome": "Avaliar", "url": "avaliar", "icone": "star"},
    {"nome": "Ranking", "url": "ranking", "icone": "trophy"},
    {"nome": "Exportar CSV", "url": "exportar_csv", "icone": "download"},
]


def opcoes_por_tipo(tipo):
    if tipo == "coordenador":
        return OPCOES_COORDENADOR
    elif tipo == "professor":
        return OPCOES_PROFESSOR
    return OPCOES_PUBLICO


def opcoes_publicas():
    return OPCOES_PUBLICAS
