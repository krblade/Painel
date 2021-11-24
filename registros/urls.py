from django.contrib import admin
from django.urls import path, include
from .views import *
from os import name
from django.urls import path
from django.contrib.auth.forms import UserCreationForm as create_user
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from .views import LoteCreateView, LotesDetView, LoteDetCreateView, LoteDetUpdateView, LoteInternoView, LoteUpdateView, LoteCreateView, LotesUpload, DisputaAbertaView
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='contas/reset_password.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='contas/reset_password_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='contas/reset_password_form.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='contas/reset_password_done.html'), name='password_reset_complete'),



    path('lotes-lista/', views.LotesBusca, name='lotes-lista'),
    path('gerencial-lista/', views.ListaGerencial, name='gerencial-lista'),
    path('lotes-det-lista/<str:pk>', LotesDetView.as_view(), name='lotes-det-lista'),
    path('lotes-upload/', views.LotesUpload, name='lotes-upload'),
    path('cadastrar-usuario/', views.CadastrarUsuario, name='cadastrar-usuario'),  
    path('lote-interno/<str:pk>/update', LoteUpdateView.as_view(), name='lote-interno'),
    path('lote-det-novo/<str:pk>/', LoteDetCreateView.as_view(), name='lote-det-novo'),
    path('lote-det-editar/<str:pk>/update', LoteDetUpdateView.as_view(), name='lote-det-editar'),
    path('lote-novo', LoteCreateView.as_view(), name='lote-novo'),
    path('leilao-upload/', views.LeilaoUpload, name='leilao-upload'),
    path('disputa-aberta-lista/', DisputaAbertaView.as_view(), name='disputa-aberta-lista'),
    path('export/', views.export, name='exportar'),
    path('exportdip/', views.export_disputa, name='exportardisp'),
    path('alterar_senha/', alterar_senha, name='alterar_senha'),
    path('alterar_perfil/', alterar_perfil, name='alterar_perfil'),
    path('responsavel-upload', responsavelUpload, name='responsavel-upload'),
    path('logs_tabela', logs_erro, name='logs_tabela'),
    path('acompanhamento', acompanhamento, name='acompanhamento'),
    path('tarefas', buscaTarefas, name='tarefas'),
    path('tarefas-editar/<str:pk>/', updateTarefas.as_view(), name='tarefas_editar'),
    path('tarefa-nova', LoteCreateView.as_view(), name='tarefa-nova'),
    path('post', Post, name='post'),
    path('inicio', inicio, name='inicio'),
] 