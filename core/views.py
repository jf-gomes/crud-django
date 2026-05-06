from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Registro
import requests

# abaixo estão as views que serão exibidas nas rotas.

# View para listar e buscar dados da API Flask
class RegistroListView(LoginRequiredMixin, ListView):
    model = Registro
    template_name = 'core/home.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Registro.objects.all() # Admin vê tudo
        return Registro.objects.filter(autor=self.request.user) # Comum vê o dele

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Exemplo de consumo da API Flask
        try:
            response = requests.get('http://sua-api-flask.com/dados')
            context['api_data'] = response.json()
        except:
            context['api_data'] = "Erro ao conectar com API Flask"
        return context

# View para Editar (Comum e Admin)
class RegistroUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Registro
    fields = ['titulo', 'descricao']
    template_name = 'core/form.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.autor or self.request.user.is_superuser

# View para Excluir (Apenas Admin)
class RegistroDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Registro
    template_name = 'core/confirm_delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        return self.request.user.is_superuser # Só o admin passa aqui