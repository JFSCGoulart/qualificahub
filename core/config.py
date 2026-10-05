"""Configurações globais do sistema."""

NOME_SISTEMA = "Qualifica Hub"

TIPOS_USUARIO = ["publico", "professor", "coordenador"]
TIPOS_AUTOCADASTRO = ["publico", "professor"]  # coordenador só via admin

AREAS_PROJETO = [
    "Educação", "Saúde", "Financeiro", "E-commerce",
    "Produtividade", "Entretenimento", "Social", "Outros"
]

ANDARES = {
    1: "Térreo",
    2: "Primeiro Andar",
    3: "Segundo Andar",
    4: "Terceiro Andar",
}

HORARIOS = [
    "08:00 - 09:00", "09:00 - 10:00", "10:00 - 11:00",
    "11:00 - 12:00", "13:00 - 14:00", "14:00 - 15:00",
    "15:00 - 16:00", "16:00 - 17:00", "17:00 - 18:00",
]

TIPOS_SALA = ["sala_aula", "laboratorio", "auditorio", "reuniao"]

MIN_SENHA = 6
MIN_DESCRICAO = 20
NOTA_MIN = 1
NOTA_MAX = 5
