from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Registro
import requests
from .forms import RegistroForm

# abaixo estão as views que serão exibidas nas rotas.

# listar e buscar dados da API.
class RegistroListView(LoginRequiredMixin, ListView):
    model = Registro
    template_name = 'core/home.html'
    context_object_name = 'registros'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Registro.objects.all()
        return Registro.objects.filter(autor=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RegistroForm()
        return context

    def post(self, request, *args, **kwargs):
        form = RegistroForm(request.POST)
        if form.is_valid():
            novo_registro = form.save(commit=False)
            novo_registro.autor = request.user
            novo_registro.save()
            return redirect('home')
        return self.get(request, *args, **kwargs)


# editar
class RegistroUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Registro
    fields = ['titulo', 'descricao']
    template_name = 'core/form.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.autor or self.request.user.is_superuser

# excluir
class RegistroDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Registro
    template_name = 'core/confirm_delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        return self.request.user.is_superuser
    


def login_cadastro_view(request):
    # inicializa os dois formulários.
    form_login = AuthenticationForm()
    form_cadastro = UserCreationForm()

    if request.method == 'POST':
        if 'btn_cadastro' in request.POST:
            form_cadastro = UserCreationForm(request.POST)
            if form_cadastro.is_valid():
                user = form_cadastro.save()
                login(request, user) # Loga automaticamente após cadastrar
                return redirect('home')
        
        elif 'btn_login' in request.POST:
            form_login = AuthenticationForm(data=request.POST)
            if form_login.is_valid():
                user = form_login.get_user()
                login(request, user)
                return redirect('home')

    return render(request, 'core/login.html', {
        'form_login': form_login,
        'form_cadastro': form_cadastro
    })