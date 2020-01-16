import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_monitoreo.settings')
import django
import sqlite3


django.setup()

# POPULATION SCRIPT
from pandas import read_json
from sistema_monitoreo_app.models import (Error,
                                 Recomendacion,
                                 Variable,
                                 Regla,
                                 Proceso,
                                 Medicion)

from ontoParser import (get_list_of_errors,
                      get_list_of_variables,
                      get_list_of_rules,
                      get_list_of_procesos,
                      reasoner)

def populate_procesos():
    print("Populating procesos")
    list_of_procesos = get_list_of_procesos()
    for p in list_of_procesos:
        # create errors
        proceso = Proceso.objects.get_or_create(nombre=p['nombre'],
                                            iri=p['iri'],
                                            descripcion=p['descripcion'],
                                            alimenta_proceso=str(p['alimenta_proceso']),)[0]
        print(proceso.nombre + " added")
    print("All procesos added")

def populate_variables():
    print("Populating variables")
    list_of_variables = get_list_of_variables()
    for v in list_of_variables:

        variable = Variable.objects.get_or_create(nombre=v['nombre'],
                                                  iri=v['iri'],
                                                  descripcion=v['descripcion'],
                                                  maximo=v['maximo'],
                                                  minimo=v['minimo'],
                                                  nominal=v['nominal'],
                                                  unidad=v['unidad'],
                                                  proceso= Proceso.objects.get(nombre=v['proceso']) if v['proceso'] != "No definido" else None,
                                                  )[0]
        print(variable.nombre + " added")
    print("All variables added")

def populate_errors():
    print("Populating errores")
    list_of_errors = get_list_of_errors()

    for e in list_of_errors:
        # create errors
        error = Error.objects.get_or_create(nombre=e['nombre'],
                                            iri=e['iri'],
                                            descripcion=e['descripcion'],
                                            peligro=e['peligro'],
                                            es_error_de=e['es_error_de'],)[0]
        print(error.nombre + " added")

        # Adding 'afectaVariable' relationship
        if e['variable'] != 'No definido':
            variables = e['variable']  # list of affected variables
            for v in variables:
                variable = Variable.objects.get(nombre=v)  # get the instance object of the variable v
                error.variable.add(variable)  # assign the variable to the current error
            error.save()  # save the modifications

        recomendacion = Recomendacion.objects.get_or_create(nombre=e['recomendacion'],
                                                            iri=e['r_iri'],
                                                            descripcion=e['desc_recomendacion'])[0]

        recomendacion.error.add(error)
        recomendacion.save()
        print(recomendacion.nombre + " added")
    print("All errores and recomendaciones added")

def populate_reglas():
    from operator import itemgetter
    print("Populating reglas")
    list_of_rules = sorted(get_list_of_rules(), key=itemgetter('proceso'))
    for rule in list_of_rules:
        print(f"Adding {rule['nombre']} to process {rule['proceso']}")
        p = Proceso.objects.get(nombre=rule['proceso'])
        regla = Regla.objects.get_or_create(nombre=rule['nombre'],
                                            proceso=p,
                                            descripcion=rule['descripcion'],
                                            regla=rule['regla'],
                                            activo=rule['activo'][0],)[0]
        print(regla.nombre + " added")
    print("All reglas added")

def populate_mediciones(n=10):
    data = read_json("static/data/bio_data_1year.json")
    for index, row in data.iloc[0:n, :].iterrows():
        medicion = Medicion.objects.get_or_create(
            da_dil1=row['da_dil1'],
            da_agv_in=row['da_agv_in'],
            da_dqo_in=row['da_dqo_in'],
            da_biomasa_x=row['da_biomasa_x'],
            da_dqo_out=row['da_dqo_out'],
            da_agv_out=row['da_agv_out'],
            mec_agv_in=row['mec_agv_in'],
            mec_dil2=row['mec_dil2'],
            mec_eapp=row['mec_eapp'],
            mec_ace=row['mec_ace'],
            mec_xa=row['mec_xa'],
            mec_xm=row['mec_xm'],
            mec_xh=row['mec_xh'],
            mec_mox=row['mec_mox'],
            mec_imec=row['mec_imec'],
            mec_qh2=row['mec_qh2'],
        )[0]

        estados = reasoner(medicion)  # Apply the reasoner to get the states
        print(f"\nAdding record #{index} - Current medicion {medicion}")
        # print(estados)
        medicion.da_estado = estados[1]['estado']
        medicion.mec_estado = estados[0]['estado']
        medicion.fbr_estado = estados[2]['estado']
        # medicion.save()

        # to get the list of errors in the current medicion for each
        # process (there are 3 dictionaries inside of estados)
        for estado in estados:
            # print(estado)
            errores_list = estado['error']
            for e in errores_list:
                error = Error.objects.get(nombre=e)  # parse Error to Error object
                # print(f"e is: {e} \n error object is: {error}")
                error.medicion.add(medicion)  # assign the error to medicion
                error.save()  # save the modifications of the error object
        medicion.save()
    print("All mediciones added")


def initial_data():
    # populate_mediciones(10)
    """To populate at the first time the db with data fetched from ontologia"""
    with sqlite3.connect("db.sqlite3") as db:
        cursor = db.cursor()
        # cursor.execute('''SELECT * FROM sqlite_master WHERE type='table'; ''')
        cursor.execute('''SELECT * FROM sistema_monitoreo_app_proceso; ''')
        result = cursor.fetchall()
        if result:
            print("Initial data already loaded")
        else:
            print("Populating script running!")
            populate_procesos()
            populate_variables()
            populate_errors()
            populate_reglas()
            populate_mediciones(10)
            print("Populating complete!")

