# from django.shortcuts import render, redirect
# from django.conf import settings
# from django.urls import reverse
# from django.shortcuts import get_object_or_404

# Create your views here.
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.http import HttpResponseRedirect

from sistema_monitoreo_app.forms import (ErrorForm,
                                RecomendacionForm,
                                MedicionForm,
                                ReglaForm)
from sistema_monitoreo_app.models import (Recomendacion,
                                 Error,
                                 Medicion,
                                 Regla,
                                 Proceso,
                                 Variable)
from ontoParser import (reasoner,
                      onto_save_error,
                      onto_save_recomendacion,
                      onto_save_regla,
                      onto_update_error,
                      onto_update_recomendacion,
                      onto_update_regla,
                      onto_delete_individual,
                      onto_delete_regla,
                      get_iri)

from clasificador import clasificar_estado


class D3DashView(TemplateView):
    template_name = 'sistema_monitoreo_app/d3_dash.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            last_medicion = Medicion.objects.last()
            first_medicion = Medicion.objects.first()
            context['min_date'] = first_medicion.date
            context['max_date'] = last_medicion.date
        except:
            print("No records in db")
        return context


def ontology(request):
    return render(request, 'sistema_monitoreo_app/ontologia.html')


def dendrogram(request):
    return render(request, 'sistema_monitoreo_app/dendrogram.html')


class ErrorListView(ListView):
    model = Error
    context_object_name = "error_list"
    template_name = 'sistema_monitoreo_app/error_list.html'

    # To get the detail of the first element at the error_list.html page
    def get_context_data(self, **kwargs):
        context = super(ErrorListView, self).get_context_data(**kwargs)
        context['error_detail'] = Error.objects.first()
        return context


class ErrorDetailView(DetailView):
    model = Error
    context_object_name = "error_detail"
    template_name = 'sistema_monitoreo_app/error_detail.html'

    # To get the list of errors (left side) at the errores_detail.html page
    def get_context_data(self, **kwargs):
        context = super(ErrorDetailView, self).get_context_data(**kwargs)
        context['errores_list'] = Error.objects.all()
        return context


class ErrorCreateView(CreateView):
    model = Error
    form_class = ErrorForm
    template_name = 'sistema_monitoreo_app/error_create.html'
    # success_url = reverse_lazy('sistema_monitoreo_app:errores-detail', kwargs={'pk': 1})

    # def get_success_url(self, **kwargs):
    #     return reverse_lazy("sites:site_overview", args=(self.object.site_id,))

    # To create the Error in the ontologia rdf file
    def form_valid(self, form):
        # do something with self.object
        super(ErrorCreateView, self).form_valid(form)
        data = self.request.POST
        error = Error.objects.get(pk=self.object.id)
        onto_save_error(error)
        # Generate IRI for the new object and add it to django field
        self.object.iri = get_iri(data['nombre'])  # get the new IRI
        # print(self.object.iri)
        self.object = form.save()  # save the object
        return HttpResponseRedirect(self.get_success_url())


class ErrorUpdateView(UpdateView):
    model = Error
    form_class = ErrorForm
    template_name = 'sistema_monitoreo_app/error_update.html'
    context_object_name = "error_detail"

    # To update the Error in the ontologia rdf file
    def form_valid(self, form):
        old_error = Error.objects.get(pk=self.object.id)  # We retrieve old object before the update
        # do something with self.object
        super(ErrorUpdateView, self).form_valid(form)  # This update the object with the new data
        # if a changed is detected
        if form.has_changed():
            fields_changed = form.changed_data  # get the fields that have been changed
            data = self.request.POST  # get the data from the request form
            updated_error = Error.objects.get(pk=self.object.id)  # We retrieve updated object
            # print("error.iri from view update")
            # print(error.iri)
            # print()
            onto_update_error(old_error, updated_error, fields_changed)  # Update the error in the ontologia API
            # Update IRI field in django db if the name is updated from the Updateview
            if "nombre" in fields_changed:
                self.object.iri = get_iri(data['nombre'])  # get the new IRI
                # print(self.object.iri)
                self.object = form.save()  # save the update
                # print("error.iri in django after update")
                # print(self.object.iri)
                # print()
        return HttpResponseRedirect(self.get_success_url())


class ErrorDeleteView(DeleteView):
    model = Error
    template_name = 'sistema_monitoreo_app/_confirm_delete.html'
    context_object_name = 'object_detail'
    success_url = reverse_lazy('sistema_monitoreo_app:error-list')

    # To delete the object in the ontologia rdf file
    def delete(self, *args, **kwargs):
        self.object = self.get_object()  # get the object
        print(self.object.iri)
        onto_delete_individual(self.object.iri)  # Delete the object given a IRI
        # self.object.post.categories.all().update(posts=F('posts')-1)
        return super(ErrorDeleteView, self).delete(*args, **kwargs)


class RecomendacionCreateView(CreateView):
    model = Recomendacion
    form_class = RecomendacionForm
    template_name = 'sistema_monitoreo_app/recomendacion_create.html'
    # success_url = reverse_lazy('sistema_monitoreo_app:error-list')

    # To redirect to the current error_detail_page
    def get_success_url(self):
        errores = self.object.error.all()  # Get the error associated to the recomen
        for e in errores:
            print(e)
        error = Error.objects.get(pk=e.id)  # Get the object instance
        return error.get_absolute_url()  # Get the return url of the error

    # Try to find a way to return to current error
    # def get_success_url(self, **kwargs):
    #     return reverse_lazy("sites:site_overview", args=(self.object.site_id,))

    def form_valid(self, form):
        # do something with self.object
        super(RecomendacionCreateView, self).form_valid(form)
        data = self.request.POST
        # print(data)
        recomendacion = Recomendacion.objects.get(pk=self.object.id)
        onto_save_recomendacion(recomendacion)
        # Generate IRI for the new object and add it to django field
        self.object.iri = get_iri(data['nombre'])  # get the new IRI
        # print(self.object.iri)
        self.object = form.save()  # save the object
        return HttpResponseRedirect(self.get_success_url())


class RecomendacionUpdateView(UpdateView):
    model = Recomendacion
    form_class = RecomendacionForm
    context_object_name = 'recomendacion_detail'
    template_name = 'sistema_monitoreo_app/recomendacion_update.html'
    # success_url = reverse_lazy('sistema_monitoreo_app:error-list')

    def get_success_url(self):
        errores = self.object.error.all()
        for e in errores:
            print(e)
        error = Error.objects.get(pk=e.id)
        return error.get_absolute_url()

    def form_valid(self, form):
        # do something with self.object
        super(RecomendacionUpdateView, self).form_valid(form)
        # if a changed is detected
        if form.has_changed():
            fields_changed = form.changed_data  # get the fields that have been changed
            data = self.request.POST  # get the data from the request form
            recomendacion = Recomendacion.objects.get(pk=self.object.id)  # get the current Recomendacion object that is getting modified
            onto_update_recomendacion(recomendacion, fields_changed)  # Update the error in the ontologia API
            # Update IRI field in django db if the name is updated from the Updateview
            if "nombre" in fields_changed:
                self.object.iri = get_iri(data['nombre'])  # get the new IRI
                # print(self.object.iri)
                self.object = form.save()  # save the update
                # print("error.iri in django after update")
                # print(self.object.iri)
                # print()
        return HttpResponseRedirect(self.get_success_url())


class RecomendacionDeleteView(DeleteView):
    model = Recomendacion
    template_name = 'sistema_monitoreo_app/_confirm_delete.html'
    context_object_name = 'object_detail'
    # success_url = reverse_lazy('sistema_monitoreo_app:error-list')

    def get_success_url(self):
        errores = self.object.error.all()
        for e in errores:
            print(e)
        error = Error.objects.get(pk=e.id)
        return error.get_absolute_url()

    # To delete the object in the ontologia api
    def delete(self, *args, **kwargs):
        self.object = self.get_object()  # get the object
        print(self.object.iri)
        onto_delete_individual(self.object.iri)  # Delete the object given a IRI
        # self.object.post.categories.all().update(posts=F('posts')-1)
        return super(RecomendacionDeleteView, self).delete(*args, **kwargs)


class MedicionCreateView(CreateView):
    """ View usado para crear una lectura nueva de manera manual. Si los datos ingresados son validos se almacena la
     medicion en la base de datos y posteriormente se crean instancias ontologicas. Por último,
    se aplica el razonador para obtener el estado de los procesos"""
    model = Medicion
    form_class = MedicionForm
    template_name = 'sistema_monitoreo_app/medicion_create.html'
    # success_url = reverse_lazy('sistema_monitoreo_app:errores-detail', kwargs={'pk': 1})

    def form_valid(self, form):
        # do something with self.object
        super(MedicionCreateView, self).form_valid(form)
        # data = self.request.POST
        # print(data['dil1'])
        # print(type(float(data['dil1'])))

        bio_estado = clasificar_estado(self.request.POST)
        print(f"bio_estado:{bio_estado}")

        if bio_estado['code'] == 0:
            print("BIO NORMAL")
            print(bio_estado['code'])
            self.object.ml_label = bio_estado['code']
            self.object.da_estado = bio_estado['estado']
            self.object.mec_estado = bio_estado['estado']
            self.object.fbr_estado = bio_estado['estado']
            self.object = form.save()  # save the medicion

        else:
            print("BIO ANORMAL")
            estados = reasoner(self.object)  # Apply the reasoner to get the states
            print(estados)
            self.object.ml_label = bio_estado['code']
            self.object.da_estado = estados[1]['estado']
            self.object.mec_estado = estados[0]['estado']
            self.object.fbr_estado = estados[2]['estado']
            self.object = form.save()  # save the medicion

            # to get the list of errors in the current medicion for each
            # process (there are 3 dictionaries inside of estados)
            for estado in estados:
                # print(estado)
                proceso = Proceso.objects.get(nombre=estado['proceso'])
                proceso.estado = estado['estado']
                proceso.save()

                errores_list = estado['error']
                for e in errores_list:
                    error = Error.objects.get(nombre=e)  # parse Error to Error object
                    # print(error)
                    error.medicion.add(self.object)  # assign the error to medicion
                    error.proceso = proceso  # assign  real-time error to a Process
                    # print(error.medicion)
                    error.save()  # save the modifications of the error object

        # self.object.error = Error.objects.get(nombre=estados[1]['error'][0])
        # self.object.recomendacion = Recomendacion.objects.get(nombre=estados[1]['recomendacion'][0])
        # self.object.error = estados[1]['error']
        # self.object.recomendacion = estados[1]['recomendacion']

        # print(estados)

        # remember the import: from django.http import HttpResponseRedirect
        return HttpResponseRedirect(self.get_success_url())


class MedicionListView(ListView):
    model = Medicion
    template_name = 'sistema_monitoreo_app/medicion_list.html'
    context_object_name = 'mediciones'
    ordering = ['-date']  # To return recently object at top of the view

    # def get_context_data(self, **kwargs):
    #     context = super(MedicionListView, self).get_context_data(**kwargs)
    #     context['fields'] = [field.name for field in Medicion._meta.get_fields()]
    #     return context


class MedicionDetailView(DetailView):
    model = Medicion
    context_object_name = "medicion"
    template_name = 'sistema_monitoreo_app/medicion_detail.html'

    def get_context_data(self, **kwargs):
        context = super(MedicionDetailView, self).get_context_data(**kwargs)

        context['errores_da'] = self.object.tieneError.filter(es_error_de="DA")
        context['errores_mec'] = self.object.tieneError.filter(es_error_de="MEC")
        context['errores_fbr'] = self.object.tieneError.filter(es_error_de="FBR")
        return context


class ReglaListView(ListView):
    model = Regla
    context_object_name = 'regla_list'
    template_name = 'sistema_monitoreo_app/regla_list.html'

    def get_context_data(self, **kwargs):
        context = super(ReglaListView, self).get_context_data(**kwargs)
        context['regla_detail'] = Regla.objects.first()
        return context


class ReglaDetailView(DetailView):
    model = Regla
    context_object_name = 'regla_detail'
    template_name = 'sistema_monitoreo_app/regla_list.html'

    def get_context_data(self, **kwargs):
        context = super(ReglaDetailView, self).get_context_data(**kwargs)
        context['regla_list'] = Regla.objects.all()
        return context


class ReglaCreateView(CreateView):
    model = Regla
    form_class = ReglaForm
    template_name = 'sistema_monitoreo_app/regla_create.html'

    # To create the Regla in the ontologia rdf file
    def form_valid(self, form):
        # do something with self.object
        super(ReglaCreateView, self).form_valid(form)
        regla = Regla.objects.get(pk=self.object.id)
        storid = onto_save_regla(regla)
        print("storid in VIEW {}".format(storid))
        self.object.storid = storid
        self.object = form.save()  # save the object
        return HttpResponseRedirect(self.get_success_url())


class ReglaUpdateView(UpdateView):
    model = Regla
    form_class = ReglaForm
    context_object_name = 'regla_detail'
    template_name = 'sistema_monitoreo_app/regla_update.html'

    def form_valid(self, form):
        # do something with self.object
        old_regla = Regla.objects.get(pk=self.object.id)
        new_nombre = self.object.nombre
        print("old_regla_nombre is {}".format(old_regla.nombre))
        print("new_nombre is {}".format(new_nombre))
        super(ReglaUpdateView, self).form_valid(form)  # This update the object with the new data
        # after_regla = Regla.objects.get(pk=self.object.id)
        # old_nombre = old_regla.nombre
        # print("regla_aftetr_super is {}".format(after_regla.nombre))
        # self.object = form.save()

        # if a changed is detected
        if form.has_changed():
            new_regla = Regla.objects.get(
                pk=self.object.id)  # get the current Regla object that is getting modified
            onto_update_regla(new_regla, old_regla)  # Update the Regla in the ontologia API
        return HttpResponseRedirect(self.get_success_url())


class ReglaDeleteView(DeleteView):
    model = Regla
    template_name = 'sistema_monitoreo_app/_confirm_delete.html'
    context_object_name = 'object_detail'
    success_url = reverse_lazy('sistema_monitoreo_app:regla-list')

    # To delete the object in the ontologia api
    def delete(self, *args, **kwargs):
        self.object = self.get_object()  # get the object
        print(self.object.nombre)
        onto_delete_regla(self.object.nombre)  # Delete the object given a IRI
        # self.object.post.categories.all().update(posts=F('posts')-1)
        return super(ReglaDeleteView, self).delete(*args, **kwargs)


class ProcesoListView(ListView):
    model = Proceso
    context_object_name = 'proceso_list'
    template_name = 'sistema_monitoreo_app/proceso_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProcesoListView, self).get_context_data(**kwargs)
        context['errores_da'] = Error.objects.filter(es_error_de="DA")
        context['errores_mec'] = Error.objects.filter(es_error_de="MEC")
        context['errores_fbr'] = Error.objects.filter(es_error_de="FBR")
        return context


    # def get_context_data(self, *, object_list=None, **kwargs):
    #
    #     context = super(ProcesoListView, self).get_context_data(**kwargs)
    #     last_medicion = Medicion.objects.last()
    #     da_fields = [
    #         field.value_from_object(last_medicion) for field in getattr(last_medicion, '_meta').get_fields()
    #         if str(field.name).startswith("da_")
    #     ]
    #     mec_fields = [
    #         field for field in getattr(last_medicion, '_meta').get_fields()
    #         if str(field.name).startswith("mec_")
    #     ]
    #
    #     print(da_fields)
    #
    #     context['last_medicion'] = last_medicion
    #     context['da_fields'] = da_fields
    #     context['mec_fields'] = mec_fields
    #
    #     return context


class EstadoActualView(ListView):
    model = Medicion
    template_name = 'sistema_monitoreo_app/estado_actual.html'
    context_object_name = 'mediciones'
    ordering = ['-date']

    def get_context_data(self, **kwargs):
        context = super(EstadoActualView, self).get_context_data(**kwargs)
        # medicion_fields = Medicion._meta.get_fields()
        # medicion_names = [f.name for f in medicion_fields][3:]
        try:
            last_medicion = Medicion.objects.last()
            grouped_by_proceso = [{'nombre': 'DA',
                                   'da_dil1': last_medicion.da_dil1,
                                   'da_agv_in': last_medicion.da_agv_in,
                                   'da_dqo_in': last_medicion.da_dqo_in,
                                   'da_biomasa_x': last_medicion.da_biomasa_x,
                                   'da_dqo_out': last_medicion.da_dqo_out,
                                   'da_agv_out': last_medicion.da_agv_out,
                                   'estado': last_medicion.da_estado},
                                  {'nombre': 'MEC',
                                   'mec_agv_in': last_medicion.mec_agv_in,
                                   'mec_dil2':last_medicion.mec_dil2,
                                   'mec_eapp': last_medicion.mec_eapp,
                                   'mec_ace': last_medicion.mec_ace,
                                   'mec_xa': last_medicion.mec_xa,
                                   'mec_xm': last_medicion.mec_xm,
                                   'mec_xh': last_medicion.mec_xh,
                                   'mec_mox': last_medicion.mec_mox,
                                   'mec_imec': last_medicion.mec_imec,
                                   'mec_qh2': last_medicion.mec_qh2,
                                   'estado': last_medicion.mec_estado},
                                  {'nombre': 'FBR',
                                   'estado': last_medicion.fbr_estado}]

            # print(grouped_by_proceso)
            context['grouped_by_proceso'] = grouped_by_proceso
        except:
            print("No records in db")
        return context





