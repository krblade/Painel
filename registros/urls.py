from os import name
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import LoteCreateView, LotesDetView, LoteDetCreateView, LoteDetUpdateView, LotesDetalheView, LoteInternoView, LoteUpdateView, LoteCreateView, LotesUpload, DisputaAbertaView
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
            template_name='index.html'
        ), name='inicio'),
    path('', auth_views.LoginView.as_view(
            template_name='index.html'
        ), name='inicio'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('lotes-lista/', views.LotesBusca, name='lotes-lista'),
    path('gerencial-lista/', views.ListaGerencial, name='gerencial-lista'),
    path('lotes-det-lista/<str:pk>', LotesDetView.as_view(), name='lotes-det-lista'),
    path('lotes-upload/', views.LotesUpload, name='lotes-upload'),
    path('lote-interno/<str:pk>/update', LoteUpdateView.as_view(), name='lote-interno'),
    path('lote-det-novo/<str:pk>/', LoteDetCreateView.as_view(), name='lote-det-novo'),
    path('lote-det-editar/<str:pk>/update', LoteDetUpdateView.as_view(), name='lote-det-editar'),
    path('lote-novo', LoteCreateView.as_view(), name='lote-novo'),
    path('leilao-upload/', views.LeilaoUpload, name='leilao-upload'),
    path('disputa-aberta-lista/', DisputaAbertaView.as_view(), name='disputa-aberta-lista'),
    path('export/', views.export, name='exportar'),
    path('testes', views.teste, name='testes')
]