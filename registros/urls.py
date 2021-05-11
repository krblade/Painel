from django.urls import path
from django.contrib.auth import views as auth_views
from .views import LotesDetalheView

urlpatterns = [
    path('lotes-detalhados/', LotesDetalheView.as_view(), name='lotes-detalhados'),   
]