from django.urls import path
from django.contrib.auth import views as auth_views
from .views import LoteCreateView, LotesDetView, LoteInternoCreateView, LotesDetalheView, LoteInternoView, LoteUpdateView, LoteCreateView
from . import views

urlpatterns = [
    path('lotes-lista/', views.LotesBusca, name='lotes-lista'),
    path('lotes-det-lista/<str:pk>', LotesDetView.as_view(), name='lotes-det-lista'),
    path('lote-interno/<str:pk>/update', LoteUpdateView.as_view(), name='lote-interno'),
    path('lote-interno-novo/<str:pk>/update', LoteInternoCreateView.as_view(), name='lote-interno-novo'),
    path('lote-novo', LoteCreateView.as_view(), name='lote-novo'),
    path('testes', views.teste, name='testes')
]