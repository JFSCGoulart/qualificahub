from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Projeto, Avaliacao, Sala, Reserva


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "tipo", "turma")
    list_filter = ("tipo",)
    fieldsets = UserAdmin.fieldsets + (
        ("Qualifica Hub", {"fields": ("tipo", "turma")}),
    )


@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ("id", "titulo", "area", "usuario", "ano")
    list_filter = ("area", "ano")
    search_fields = ("titulo", "tecnologias")


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "projeto", "nota", "criado_em")
    list_filter = ("nota",)


@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "andar", "capacidade", "tipo", "status")
    list_filter = ("andar", "tipo", "status")


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ("id", "sala", "usuario", "data", "horario", "status")
    list_filter = ("status", "data")
