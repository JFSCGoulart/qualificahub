from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("cadastro/", views.cadastro_view, name="cadastro"),

    path("projetos/", views.buscar_publico_view, name="buscar_publico"),
    path("projetos/cadastrar/", views.cadastrar_projeto_view, name="cadastrar_projeto"),
    path("projetos/meus/", views.meus_projetos_view, name="meus_projetos"),
    path("projetos/remover/<int:projeto_id>/", views.remover_projeto_view, name="remover_projeto"),
    path("projetos/avaliar/", views.avaliar_view, name="avaliar"),

    path("ranking/", views.ranking_view, name="ranking"),

    path("salas/", views.ver_salas_view, name="ver_salas"),
    path("salas/gerenciar/", views.gerenciar_salas_view, name="gerenciar_salas"),

    path("reservas/reservar/", views.reservar_sala_view, name="reservar_sala"),
    path("reservas/minhas/", views.minhas_reservas_view, name="minhas_reservas"),
    path("reservas/cancelar/<int:reserva_id>/", views.cancelar_reserva_view, name="cancelar_reserva"),
    path("reservas/todas/", views.todas_reservas_view, name="todas_reservas"),

    path("usuarios/", views.listar_usuarios_view, name="listar_usuarios"),
    path("exportar/", views.exportar_csv_view, name="exportar_csv"),
]
