from functools import wraps

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import connections
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from tailwaglabs.models import Estadosexperiencia, Utilizador, Experiencia, Medicoestemperatura, Salas_ratos


def restrict_access_to_experiencia(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        experiencia_id = kwargs.get('id_exp')
        experiencia = get_object_or_404(Experiencia, pk=experiencia_id)
        if request.user.utilizador.id != experiencia.idinvestigador.id:
            return HttpResponseForbidden("Não tem permissões para aceder a esta experiência.")
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def get_cursor(request):
    if request.user.utilizador.tipoutilizador.designacao == "Investigador":
        cursor = connections['investigador'].cursor()
    elif request.user.utilizador.tipoutilizador.designacao == "Tecnico":
        cursor = connections['tecnico'].cursor()
    else:
        cursor = connections['default'].cursor()
    return cursor


@login_required(login_url='/tailwaglabs/login')
def index(request):
    return render(request, 'tailwaglabs/experiencias.html',
                  {'object_list': Experiencia.objects.filter(idinvestigador=request.user.utilizador.id, isactive=1)})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('tailwaglabs:index'))
            else:
                context = {'error_message': "Conta inativa"}
                return render(request, 'tailwaglabs/login.html', context)
        else:
            context = {'error_message': "Credenciais inválidas"}
            return render(request, 'tailwaglabs/login.html', context)
    context = {}
    return render(request, 'tailwaglabs/login.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('tailwaglabs:login_view'))


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = "twl-" + request.POST.get('username')
        email = request.POST.get('email')
        name = request.POST.get('name')
        role = request.POST.get('role')
        try:
            newuser = User.objects.create_user(username=username, email=email, password=password)
            with connections['default'].cursor() as cursor:
                cursor.callproc('CriarUtilizador', [name, role, newuser.id])
                cursor.close()
        except Exception as e:
            print(e)
            return render(request, 'tailwaglabs/registration.html', {'error_message': "Utilizador Existente"})

        return HttpResponseRedirect(reverse('tailwaglabs:login_view'))

    return render(request, 'tailwaglabs/registration.html')


def perfil(request):
    utilizador = (Utilizador.objects.get(user=request.user))
    role = utilizador.tipoutilizador.designacao
    telefone = utilizador.telefone
    context = {'role': role, 'telefone': telefone}
    return render(request, 'tailwaglabs/perfil.html', context)


def criarexperiencia(request):
    if request.method == 'POST':
        descricao = request.POST.get('descricao')
        substancia = request.POST.get('substancia')
        idinvestigador = request.user.utilizador.id
        nr_ratos = request.POST.get('nr_ratos')
        lim_ratos_sala = request.POST.get('lim_ratos_sala')
        lim_ratos_movimento = request.POST.get('lim_ratos_movimento')
        temp_ideal = request.POST.get('temp_ideal')
        temp_maxima = request.POST.get('temp_maxima')
        temp_minima = request.POST.get('temp_minima')
        outlier_vartempmax = request.POST.get('outlier_vartempmax')
        outlier_leiturasnumero = request.POST.get('outlier_leiturasnumero')
        variacaodrastica_temperatura = request.POST.get('variacaodrastica_temperatura')
        variacaodrastica_intervalotempo = request.POST.get('variacaodrastica_intervalotempo')
        try:
            with get_cursor(request) as cursor:
                cursor.callproc('CriarExperiencia',
                                [descricao, substancia, idinvestigador, nr_ratos, lim_ratos_sala, lim_ratos_movimento,
                                 temp_ideal, temp_maxima, temp_minima, outlier_vartempmax, outlier_leiturasnumero,
                                 variacaodrastica_temperatura, variacaodrastica_intervalotempo])
                cursor.close()
        except Exception as e:
            print(e)
            return render(request, 'tailwaglabs/experiencias.html',
                          {
                              'error_message': "Erro ao criar experiência, não tem permissões. Por favor contacte um "
                                               "administrador",
                              'object_list': Experiencia.objects.filter(idinvestigador=request.user.utilizador.id,
                                                                        isactive=1)})

    return render(request, 'tailwaglabs/experiencias.html',
                  {'object_list': Experiencia.objects.filter(idinvestigador=request.user.utilizador.id, isactive=1)})


def estadosexperiencia(request):
    estados = Estadosexperiencia.objects
    # Serialize our data
    return JsonResponse(list(estados.values()), safe=False, json_dumps_params={'ensure_ascii': False},
                        content_type='application/json; charset=utf-8')


@restrict_access_to_experiencia
def removerexperiencia(request):
    if request.method == 'POST':
        idexperiencia = request.POST.get('idexperiencia')
        try:
            with get_cursor(request) as cursor:
                cursor.callproc('RemoverExperiencia', [idexperiencia])
                cursor.close()
        except Exception as e:
            print(e)
            return render(request, 'tailwaglabs/experiencias.html', {'error_message': "Falha ao remover a experiencia"})
        return render(request, 'tailwaglabs/experiencias.html',
                      {'object_list': Experiencia.objects.filter(idinvestigador=request.user.utilizador.id,
                                                                 isactive=1)})


@restrict_access_to_experiencia
def alterarexperiencia(request, id_exp):
    if request.method == 'POST':
        descricao = request.POST.get('descricao')
        substancia = request.POST.get('substancia')
        idinvestigador = request.user.utilizador.id
        nr_ratos = request.POST.get('nr_ratos')
        lim_ratos_sala = request.POST.get('lim_ratos_sala')
        lim_ratos_movimento = request.POST.get('lim_ratos_movimento')
        temp_ideal = request.POST.get('temp_ideal')
        temp_maxima = request.POST.get('temp_maxima')
        temp_minima = request.POST.get('temp_minima')
        outlier_vartempmax = request.POST.get('outlier_vartempmax')
        outlier_leiturasnumero = request.POST.get('outlier_leiturasnumero')
        variacaodrastica_temperatura = request.POST.get('variacaodrastica_temperatura')
        variacaodrastica_intervalotempo = request.POST.get('variacaodrastica_intervalotempo')
        idparametros = Experiencia.objects.get(idexperiencia=id_exp).idparametros
        try:
            with get_cursor(request) as cursor:
                cursor.callproc('AlterarExperiencia',
                                [id_exp, descricao, substancia, idinvestigador, nr_ratos, lim_ratos_sala,
                                 lim_ratos_movimento,
                                 temp_ideal, temp_maxima, temp_minima, outlier_vartempmax, outlier_leiturasnumero,
                                 variacaodrastica_temperatura, variacaodrastica_intervalotempo, idparametros])
                cursor.close()
        except Exception as e:
            print(e)
            return render(request, 'tailwaglabs/experiencias.html',
                          {'error_message': "Erro ao alterar experiência. A experiência está a decorrer",
                           'object_list': Experiencia.objects.filter(idinvestigador=request.user.utilizador.id,
                                                                     isactive=1)})

    experiencia = Experiencia.objects.select_related('idparametros').get(pk=id_exp)
    parametros = experiencia.idparametros
    salasResultados = Salas_ratos.objects.filter(experiencia=id_exp).order_by('sala')
    salas = []
    for sala in salasResultados:
        resultado = {
            'sala': sala.sala,
            'ratos': sala.ratos
        }
        salas.append(resultado)

    return render(request, 'tailwaglabs/experiencias.html',
                  {'object_list': Experiencia.objects.filter(idinvestigador=request.user.utilizador.id, isactive=1),
                   'id_exp': id_exp, 'parametros': parametros,
                   'experiencia': experiencia, 'salas': salas})


@restrict_access_to_experiencia
def iniciarexperiencia(request, id_exp):
    try:
        with get_cursor(request) as cursor:
            cursor.callproc('UpdateExperienciaTime', [id_exp, 1])
            cursor.close()
        Experiencia.objects.filter(pk=id_exp).update(idestado=2)
    except Exception as e:
        print(e)
        return render(request, 'tailwaglabs/experiencias.html',
                      {'object_list': Experiencia.objects.filter(idinvestigador=request.user.utilizador.id,
                                                                 isactive=1),
                       'error_message': "Já existe uma experiência a decorrer"})
    return render(request, 'tailwaglabs/experiencias.html',
                  {'object_list': Experiencia.objects.filter(idinvestigador=request.user.utilizador.id, isactive=1)})


@restrict_access_to_experiencia
def concluirexperiencia(request, id_exp):
    try:
        Experiencia.objects.filter(pk=id_exp).update(idestado=3)
        with get_cursor(request) as cursor:
            cursor.callproc('UpdateExperienciaTime', [id_exp, 0])
            cursor.close()
    except Exception as e:
        print(e)
    return render(request, 'tailwaglabs/experiencias.html',
                  {'object_list': Experiencia.objects.filter(idinvestigador=request.user.utilizador.id, isactive=1)})


@restrict_access_to_experiencia
def apagarexperiencia(request, id_exp):
    try:
        with get_cursor(request) as cursor:
            cursor.callproc('RemoverExperiencia',
                            [id_exp])
            cursor.close()
    except Exception as e:
        print(e)
        return render(request, 'tailwaglabs/experiencias.html',
                      {'error_message': "Erro ao eliminar experiência, por favor contacte o administrador",
                       'object_list': Experiencia.objects.filter(idinvestigador=request.user.utilizador.id,
                                                                 isactive=1)})
    return render(request, 'tailwaglabs/experiencias.html',
                  {'object_list': Experiencia.objects.filter(idinvestigador=request.user.utilizador.id, isactive=1)})


def alterarutilizador(request):
    if request.method == 'POST':
        telefone = request.POST.get('telefone')
        password = request.POST.get('password')
        try:
            with get_cursor(request) as cursor:
                cursor.callproc('AlterarUtilizador',
                                [request.user.utilizador.id, telefone])
                cursor.close()
                message = "Telefone alterado com sucesso!"
            if password:
                u = User.objects.get(username=request.user.username)
                u.set_password(password)
                u.save()
                update_session_auth_hash(request, u)
                message = "Dados alterados com sucesso!"
        except Exception as e:
            return render(request, 'tailwaglabs/perfil.html',
                          {'error_message': "Falha ao alterar utilizador"})
    return render(request, 'tailwaglabs/experiencias.html',
                  {'object_list': Experiencia.objects.filter(idinvestigador=request.user.utilizador.id, isactive=1),
                   'password_message': message})


def leituras_momento(request):
    temp_sensor1 = Medicoestemperatura.objects.filter(sensor=1, isoutlier=0, iserror=0).latest('hora').leitura
    temp_sensor2 = Medicoestemperatura.objects.filter(sensor=2, isoutlier=0, iserror=0).latest('hora').leitura
    print(temp_sensor1, temp_sensor2)
    if not Experiencia.objects.filter(idestado=2).exists():
        return render(request, 'tailwaglabs/sensores.html',
                      {'error_message': "Não existe nenhuma experiência a decorrer", 'temp_sensor1': temp_sensor1,
                       'temp_sensor2': temp_sensor2})
    salas = []
    idexp_in_progress = Experiencia.objects.get(idestado=2).idexperiencia
    if idexp_in_progress > 0:
        for x in Salas_ratos.objects.filter(experiencia=idexp_in_progress).order_by('sala'):
            salas.append(x.ratos)
    context = {
        'temp_sensor1': temp_sensor1,
        'temp_sensor2': temp_sensor2,
        'salas': salas,
    }
    return render(request, 'tailwaglabs/sensores.html', context)


def leituras_momento_JSON(request):
    temp_sensor1 = Medicoestemperatura.objects.filter(sensor=1, isoutlier=0, iserror=0).latest('hora').leitura
    temp_sensor2 = Medicoestemperatura.objects.filter(sensor=2, isoutlier=0, iserror=0).latest('hora').leitura
    if not Experiencia.objects.filter(idestado=2).exists():
        return JsonResponse({'error_message': "Não existe nenhuma experiência a decorrer", 'temp_sensor1': temp_sensor1,
                       'temp_sensor2': temp_sensor2})

    salas = []
    idexp_in_progress = Experiencia.objects.get(idestado=2).idexperiencia
    if idexp_in_progress > 0:
        for x in Salas_ratos.objects.filter(experiencia=idexp_in_progress).order_by('sala'):
            salas.append(x.ratos)
    context = {
        'temp_sensor1': temp_sensor1,
        'temp_sensor2': temp_sensor2,
        'salas': salas,
    }
    return JsonResponse(context)
