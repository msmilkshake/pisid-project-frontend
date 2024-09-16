from django.urls import path
from . import views

app_name = 'tailwaglabs'
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login_view'),
    path('estadosexperiencia', views.estadosexperiencia, name='estadosexperiencia'),
    path('removerexperiencia', views.removerexperiencia, name='removerexperiencia'),
    path('signup', views.signup, name='signup'),
    path('criarexperiencia', views.criarexperiencia, name='criarexperiencia'),
    path('alterarexperiencia/<int:id_exp>/', views.alterarexperiencia, name='alterarexperiencia'),
    path('logout', views.logout_view, name='logout_view'),
    path('perfil', views.perfil, name='perfil'),
    path('alterarutilizador', views.alterarutilizador, name='alterarutilizador'),
    path('iniciarexperiencia/<int:id_exp>/', views.iniciarexperiencia, name='iniciarexperiencia'),
    path('concluirexperiencia/<int:id_exp>/', views.concluirexperiencia, name='concluirexperiencia'),
    path('apagarexperiencia/<int:id_exp>/', views.apagarexperiencia, name='apagarexperiencia'),
    path('leituras_momento', views.leituras_momento, name='leituras_momento'),
    path('leituras_momento_JSON', views.leituras_momento_JSON, name='leituras_momento_JSON'),
]
