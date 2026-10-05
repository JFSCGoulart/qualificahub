"""Injeta as opções de menu em todos os templates automaticamente."""
from . import menus


def menu_context(request):
    """
    Disponibiliza 'menu_opcoes' em todos os templates,
    independente da view. Corrige o bug da navbar que
    mostrava 'Entrar/Cadastrar' mesmo estando logado.
    """
    if request.user.is_authenticated:
        return {
            "menu_opcoes": menus.opcoes_por_tipo(request.user.tipo),
            "menu_logado": True,
            "menu_usuario": request.user,
        }
    return {
        "menu_opcoes": menus.opcoes_publicas(),
        "menu_logado": False,
        "menu_usuario": None,
    }
