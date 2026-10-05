"""Decorators de permissão por tipo de usuário."""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def requer_login(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Você precisa estar logado.")
            return redirect("login")
        return view_func(request, *args, **kwargs)
    return wrapper


def requer_coordenador(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Você precisa estar logado.")
            return redirect("login")
        if request.user.tipo != "coordenador":
            messages.error(request, "Acesso restrito a coordenadores.")
            return redirect("home")
        return view_func(request, *args, **kwargs)
    return wrapper


def requer_professor_ou_coordenador(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Você precisa estar logado.")
            return redirect("login")
        if request.user.tipo not in ("professor", "coordenador"):
            messages.error(request, "Acesso restrito a professores e coordenadores.")
            return redirect("home")
        return view_func(request, *args, **kwargs)
    return wrapper
