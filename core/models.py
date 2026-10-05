from django.db import models
from django.contrib.auth.models import AbstractUser
from . import config


class Usuario(AbstractUser):
    """Usuário customizado com tipo e turma."""
    TIPOS = [(t, t) for t in config.TIPOS_USUARIO]
    tipo = models.CharField(max_length=20, choices=TIPOS, default="publico")
    turma = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name or self.username} ({self.tipo})"

    @property
    def is_coordenador(self):
        return self.tipo == "coordenador"

    @property
    def is_professor(self):
        return self.tipo == "professor"

    @property
    def pode_reservar(self):
        return self.tipo in ("professor", "coordenador")


class Projeto(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    area = models.CharField(max_length=50, choices=[(a, a) for a in config.AREAS_PROJETO])
    tecnologias = models.CharField(max_length=200, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="projetos")
    ano = models.IntegerField()
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criado_em"]

    def __str__(self):
        return self.titulo


class Avaliacao(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name="avaliacoes")
    nota = models.IntegerField(choices=[(i, i) for i in range(config.NOTA_MIN, config.NOTA_MAX + 1)])
    comentario = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("usuario", "projeto")
        ordering = ["-criado_em"]

    def __str__(self):
        return f"{self.usuario} -> {self.projeto} ({self.nota})"


class Sala(models.Model):
    nome = models.CharField(max_length=100)
    andar = models.IntegerField()
    capacidade = models.IntegerField()
    tipo = models.CharField(max_length=20, choices=[(t, t) for t in config.TIPOS_SALA], default="sala_aula")
    status = models.CharField(max_length=20, default="ATIVA")

    class Meta:
        ordering = ["andar", "nome"]

    def __str__(self):
        return f"{self.nome} (andar {self.andar})"


class Reserva(models.Model):
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name="reservas")
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    data = models.DateField()
    horario = models.CharField(max_length=20, choices=[(h, h) for h in config.HORARIOS])
    motivo = models.TextField(blank=True)
    status = models.CharField(max_length=20, default="ativa")
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["data", "horario"]

    def __str__(self):
        return f"{self.sala} - {self.data} {self.horario}"
