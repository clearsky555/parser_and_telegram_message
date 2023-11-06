from django.urls import path
from . import views

# app_name = 'parser_app'

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('telegram/', views.get_tg, name='get_telegram'),
    path('ok/<str:user>', views.p_results, name='results'),
]