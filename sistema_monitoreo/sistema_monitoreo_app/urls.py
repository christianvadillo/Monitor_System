from django.urls import path

from sistema_monitoreo_app.views import (D3DashView, ontology, dendrogram,
                                     ErrorDetailView, ErrorCreateView, ErrorUpdateView, ErrorListView, ErrorDeleteView,
                                     RecomendacionCreateView, RecomendacionUpdateView, RecomendacionDeleteView,
                                     MedicionCreateView, MedicionListView, MedicionDetailView,
                                     ReglaListView, ReglaDetailView, ReglaUpdateView, ReglaCreateView, ReglaDeleteView,
                                     ProcesoListView, EstadoActualView, )
app_name = 'sistema_monitoreo_app'

urlpatterns = [
    path('', D3DashView.as_view(), name='d3-dash'),
    path('ontologia/', ontology, name='ontologia'),
    path('dendrogram/', dendrogram, name='dendrogram'),
    path('estado/', EstadoActualView.as_view(), name='estado-actual'),
    path('proceso/', ProcesoListView.as_view(), name='proceso-list'),
    path('error/', ErrorListView.as_view(), name='error-list'),
    path('error/<int:pk>/', ErrorDetailView.as_view(), name='error-detail'),
    path('error/create/', ErrorCreateView.as_view(), name='error-create'),
    path('error/<int:pk>/update/', ErrorUpdateView.as_view(), name='error-update'),
    path('error/<int:pk>/delete/', ErrorDeleteView.as_view(), name='error-delete'),
    path('recomendacion/create/', RecomendacionCreateView.as_view(), name='recomendacion-create'),
    path('recomendacion/<int:pk>/update/', RecomendacionUpdateView.as_view(), name='recomendacion-update'),
    path('recomendacion/<int:pk>/delete/', RecomendacionDeleteView.as_view(), name='recomendacion-delete'),
    path('medicion/', MedicionListView.as_view(), name='medicion-list'),
    path('medicion/<int:pk>/', MedicionDetailView.as_view(), name='medicion-detail'),
    path('medicion/create/', MedicionCreateView.as_view(), name='medicion-create'),
    path('regla/', ReglaListView.as_view(), name='regla-list'),
    path('regla/<int:pk>/', ReglaDetailView.as_view(), name='regla-detail'),
    path('regla/create/', ReglaCreateView.as_view(), name='regla-create'),
    path('regla/<int:pk>/update/', ReglaUpdateView.as_view(), name='regla-update'),
    path('regla/<int:pk>/delete/', ReglaDeleteView.as_view(), name='regla-delete'),
]
