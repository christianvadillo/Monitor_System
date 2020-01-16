from django.contrib import admin
from sistema_monitoreo_app.models import (Recomendacion,
                                 Error,
                                 Variable,
                                 Medicion,
                                 Regla,
                                 Proceso)
# Register your models here.

admin.site.register(Recomendacion)
admin.site.register(Error)
admin.site.register(Variable)
admin.site.register(Medicion)
admin.site.register(Regla)
admin.site.register(Proceso)
