from django.urls import path
from .views import IndexView, TableView

urlpatterns = [
    path('inicio/', IndexView.as_view(), name='inicio'),
    path('tabela/', TableView.as_view(), name='tabela'),
    path('', IndexView.as_view(), name='inicio'),
]