from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from model_utils import FieldTracker
# Create your models here.


class Proceso(models.Model):
    iri = models.CharField(max_length=200)
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(max_length=400, blank=True)
    estado = models.CharField(max_length=10, blank=True)
    alimenta_proceso = models.CharField(max_length=50, blank=True)
    # It will updated once a new instances of the model is created
    created_at = models.DateTimeField(auto_now_add=True)
    # It will updated every time the model instance is saved
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre}"

    def get_cname(self):
        class_name = "Proceso"
        return class_name

    """ Method used to redirect to detail page after create a new instance"""
    # def get_absolute_url(self):
    #     return reverse('sistema_monitoreo_app:error-detail', kwargs={'pk': self.pk})


class Variable(models.Model):
    proceso = models.ForeignKey(Proceso, on_delete=models.CASCADE,
                                related_name="tieneVariable",
                                null=True, blank=True)
    iri = models.CharField(max_length=200)
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(max_length=400, blank=True)
    maximo = models.FloatField()
    minimo = models.FloatField()
    nominal = models.FloatField()
    unidad = models.CharField(max_length=10)
    # It will updated once a new instances of the model is created
    created_at = models.DateTimeField(auto_now_add=True)
    # It will updated every time the model instance is saved
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('nombre',) # To order in the ListView

    def __str__(self):
        return f"{self.nombre}"

    def get_cname(self):
        class_name = "Variable"
        return class_name

    """ Method used to redirect to detail page after create a new instance"""
    # def get_absolute_url(self):
    #     return reverse('sistema_monitoreo_app:error-detail', kwargs={'pk': self.pk})


class Medicion(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    da_dil1 = models.FloatField()
    da_agv_in = models.FloatField()
    da_dqo_in = models.FloatField()
    da_biomasa_x = models.FloatField()
    da_dqo_out = models.FloatField()
    da_agv_out = models.FloatField()
    mec_agv_in = models.FloatField()
    mec_dil2 = models.FloatField()
    mec_eapp = models.FloatField()
    mec_ace = models.FloatField()
    mec_xa = models.FloatField()
    mec_xm = models.FloatField()
    mec_xh = models.FloatField()
    mec_mox = models.FloatField()
    mec_imec = models.FloatField()
    mec_qh2 = models.FloatField()
    ml_label = models.PositiveIntegerField(validators=[MaxValueValidator(1), MinValueValidator(0)],
                                           null=True,
                                           blank=True)
    da_estado = models.CharField(max_length=10, blank=True)
    mec_estado = models.CharField(max_length=10, blank=True)
    fbr_estado = models.CharField(max_length=10, blank=True)

    class Meta:
        get_latest_by = "date"  # To use MyModel.objects.latest()

    def __str__(self):
        return f"{self.date}"

    """ Method used to redirect to detail page after create a new instance"""
    def get_absolute_url(self):
        return reverse('sistema_monitoreo_app:estado-actual')


class Error(models.Model):
    # oneToMany relationship (one medicion may have many errors)
    variable = models.ManyToManyField(Variable,
                                      related_name="afectaVariable",
                                      blank=True)
    proceso = models.ForeignKey(Proceso,
                                on_delete=models.CASCADE,
                                related_name="presentaError",
                                blank=True, null=True)
    medicion = models.ManyToManyField(Medicion,
                                      related_name="tieneError",
                                      blank=True)
    iri = models.CharField(max_length=200)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=400, blank=True)
    peligro = models.CharField(max_length=10)
    es_error_de = models.CharField(max_length=10, blank=True)
    # It will updated once a new instances of the model is created
    created_at = models.DateTimeField(auto_now_add=True)
    # It will updated every time the model instance is saved
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('nombre',)  # To order in the ListView

    def __str__(self):
        return f"{self.nombre}"

    def get_cname(self):
        class_name = "Error"
        return class_name

    """ Method used to redirect to detail page after create a new instance"""
    def get_absolute_url(self):
        return reverse('sistema_monitoreo_app:error-detail', kwargs={'pk': self.pk})


class Recomendacion(models.Model):
    error = models.ManyToManyField(Error, related_name="tieneRecomendacion", blank=True)
    iri = models.CharField(max_length=200)
    nombre = models.CharField(max_length=40, unique=True)
    descripcion = models.TextField(max_length=400, blank=True)
    # It will updated once a new instances of the model is created
    created_at = models.DateTimeField(auto_now_add=True, editable=True)
    # It will updated every time the model instance is saved
    updated_at = models.DateTimeField(auto_now=True, editable=True)

    class Meta:
        ordering = ('nombre',) # To order in the ListView

    def __str__(self):
        return f"{self.nombre}"

    # """ Method used to redirect to detail page after create a new instance"""
    # def get_absolute_url(self):
    #     return reverse('sistema_monitoreo_app:error-detail', kwargs={'pk': self.pk})

    def get_cname(self):
        class_name = "Recomendacion"
        return class_name


class Regla(models.Model):
    activo = models.BooleanField()
    nombre = models.CharField(max_length=40, unique=True)
    proceso = models.ForeignKey(Proceso, on_delete=models.SET_NULL,
                                related_name="tieneRegla",
                                null=True, blank=True)
    # proceso = models.CharField(max_length=10)
    descripcion = models.TextField(max_length=400, blank=True)
    regla = models.TextField(max_length=10000)

    # It will updated once a new instances of the model is created
    created_at = models.DateTimeField(auto_now_add=True, editable=True)
    # It will updated every time the model instance is saved
    updated_at = models.DateTimeField(auto_now=True, editable=True)

    class Meta:
        ordering = ('nombre',) # To order in the ListView

    def __str__(self):
        return f"{self.nombre}"

    def get_cname(self):
        class_name = "Regla"
        return class_name

    """ Method used to redirect to detail page after create a new instance"""
    def get_absolute_url(self):
        return reverse('sistema_monitoreo_app:regla-detail', kwargs={'pk': self.pk})

