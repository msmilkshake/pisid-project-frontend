# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.auth.models import User
from django.db import models


# python manage.py makemigrations tailwaglabs
# python manage.py migrate

class Alerta(models.Model):
    idalerta = models.AutoField(db_column='IDAlerta', primary_key=True)  # Field name made lowercase.
    idexperiencia = models.ForeignKey('Experiencia', models.DO_NOTHING,
                                      db_column='IDExperiencia')  # Field name made lowercase.
    hora = models.DateTimeField(db_column='Hora')  # Field name made lowercase.
    sala = models.IntegerField(db_column='Sala')  # Field name made lowercase.
    sensor = models.IntegerField(db_column='Sensor')  # Field name made lowercase.
    leitura = models.DecimalField(db_column='Leitura', max_digits=4, decimal_places=2)  # Field name made lowercase.
    tipoalerta = models.ForeignKey('Tipoalerta', models.DO_NOTHING,
                                   db_column='TipoAlerta')  # Field name made lowercase.
    mensagem = models.CharField(db_column='Mensagem', max_length=100)  # Field name made lowercase.
    horaescrita = models.DateTimeField(db_column='HoraEscrita')  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'alerta'


class Estadosexperiencia(models.Model):
    idestado = models.IntegerField(db_column='IDEstado', primary_key=True)  # Field name made lowercase.
    designacao = models.CharField(db_column='Designacao', max_length=25, blank=True,
                                  null=True)  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'estadosexperiencia'


class Experiencia(models.Model):
    idexperiencia = models.AutoField(db_column='IDExperiencia', primary_key=True)  # Field name made lowercase.
    descricao = models.CharField(db_column='Descricao', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.
    idinvestigador = models.ForeignKey('Utilizador', models.DO_NOTHING, db_column='IDInvestigador', blank=True,
                                       null=True)  # Field name made lowercase.
    datahorainicio = models.DateTimeField(db_column='DataHoraInicio', blank=True,
                                          null=True)  # Field name made lowercase.
    datahorafim = models.DateTimeField(db_column='DataHoraFim', blank=True, null=True)  # Field name made lowercase.
    idparametros = models.ForeignKey('Parametrosexperiencia', models.DO_NOTHING, db_column='IDParametros', blank=True,
                                     null=True)  # Field name made lowercase.
    idestado = models.ForeignKey(Estadosexperiencia, models.DO_NOTHING, db_column='IDEstado', blank=True,
                                 null=True)  # Field name made lowercase.
    experienciavalida = models.IntegerField(db_column='ExperienciaValida', blank=True,
                                            null=True)  # Field name made lowercase.
    substancia = models.CharField(db_column='Substancia', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    isactive = models.IntegerField(db_column='IsActive', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'experiencia'


class Medicoespassagens(models.Model):
    idmedicao = models.AutoField(db_column='IDMedicao', primary_key=True)  # Field name made lowercase.
    idexperiencia = models.ForeignKey(Experiencia, models.DO_NOTHING,
                                      db_column='IDExperiencia')  # Field name made lowercase.
    salaorigem = models.IntegerField(db_column='SalaOrigem')  # Field name made lowercase.
    saladestino = models.IntegerField(db_column='SalaDestino')  # Field name made lowercase.
    hora = models.DateTimeField(db_column='Hora')  # Field name made lowercase.
    iserror = models.IntegerField(db_column='IsError', blank=True, null=True)  # Field name made lowercase.
    timestampregisto = models.DateTimeField(db_column='TimestampRegisto', blank=True,
                                            null=True)  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'medicoespassagens'


class Medicoessalas(models.Model):
    idmedicao = models.AutoField(db_column='IDMedicao', primary_key=True)  # Field name made lowercase.
    idexperiencia = models.ForeignKey(Experiencia, models.DO_NOTHING,
                                      db_column='IDExperiencia')  # Field name made lowercase.
    numeroratosfinal = models.IntegerField(db_column='NumeroRatosFinal', blank=True,
                                           null=True)  # Field name made lowercase.
    sala = models.IntegerField(db_column='Sala')  # Field name made lowercase.
    iserror = models.IntegerField(db_column='IsError')  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'medicoessalas'


class Medicoestemperatura(models.Model):
    idmedicao = models.AutoField(db_column='IDMedicao', primary_key=True)  # Field name made lowercase.
    idexperiencia = models.ForeignKey(Experiencia, models.DO_NOTHING,
                                      db_column='IDExperiencia')  # Field name made lowercase.
    hora = models.DateTimeField(db_column='Hora')  # Field name made lowercase.
    leitura = models.DecimalField(db_column='Leitura', max_digits=4, decimal_places=2)  # Field name made lowercase.
    sensor = models.IntegerField(db_column='Sensor', blank=True, null=True)  # Field name made lowercase.
    iserror = models.IntegerField(db_column='IsError', blank=True, null=True)  # Field name made lowercase.
    isoutlier = models.IntegerField(db_column='IsOutlier', blank=True, null=True)  # Field name made lowercase.
    timestampregisto = models.BigIntegerField(db_column='TimestampRegisto', blank=True,
                                              null=True)  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'medicoestemperatura'


class Parametrosexperiencia(models.Model):
    idparametros = models.AutoField(db_column='IDParametros', primary_key=True)  # Field name made lowercase.
    numeroratosinicial = models.IntegerField(db_column='NumeroRatosInicial')  # Field name made lowercase.
    limiteratossala = models.IntegerField(db_column='LimiteRatosSala')  # Field name made lowercase.
    segundossemmovimento = models.IntegerField(db_column='SegundosSemMovimento', blank=True,
                                               null=True)  # Field name made lowercase.
    temperaturaideal = models.DecimalField(db_column='TemperaturaIdeal', max_digits=4,
                                           decimal_places=2)  # Field name made lowercase.
    temperaturamaxima = models.DecimalField(db_column='TemperaturaMaxima', max_digits=4,
                                            decimal_places=2)  # Field name made lowercase.
    temperaturaminima = models.DecimalField(db_column='TemperaturaMinima', max_digits=4,
                                            decimal_places=2)  # Field name made lowercase.
    outliervariacaotempmax = models.FloatField(db_column='OutlierVariacaoTempMax', blank=True,
                                               null=True)  # Field name made lowercase.
    outlierleiturasnumero = models.IntegerField(db_column='OutlierLeiturasNumero', blank=True,
                                                null=True)  # Field name made lowercase.
    variacaodrasticatemperatura = models.FloatField(db_column='VariacaoDrasticaTemperatura', blank=True,
                                                    null=True)  # Field name made lowercase.
    variacaodrasticaintervalotempo = models.IntegerField(db_column='VariacaoDrasticaIntervaloTempo', blank=True,
                                                         null=True)  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'parametrosexperiencia'


class Tipoalerta(models.Model):
    idtipoalerta = models.AutoField(db_column='IDTipoAlerta', primary_key=True)  # Field name made lowercase.
    designacao = models.CharField(db_column='Designacao', max_length=100)  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'tipoalerta'


class Tipoutilizador(models.Model):
    idtipoutilizador = models.AutoField(db_column='IDTipoUtilizador', primary_key=True)  # Field name made lowercase.
    designacao = models.CharField(db_column='Designacao', max_length=40)  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'tipoutilizador'


class Utilizador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(db_column='Nome', max_length=100)  # Field name made lowercase.
    telefone = models.CharField(db_column='Telefone', max_length=12)  # Field name made lowercase.
    tipoutilizador = models.ForeignKey(Tipoutilizador, models.DO_NOTHING,
                                       db_column='TipoUtilizador')  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'utilizador'


class Salas_ratos(models.Model):
    sala = models.IntegerField(db_column='Sala')
    ratos = models.IntegerField(db_column='Ratos')
    experiencia = models.ForeignKey(Experiencia, models.DO_NOTHING,
                                    db_column='experiencia')

    class Meta:
        managed = False
        db_table = 'salas_ratos'
