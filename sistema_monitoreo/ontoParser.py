from owlready2 import *
import datetime
# import pandas as pd
# from datetime import datetime
# onto_src = get_ontology("static/ontologia/bio_v4_4_2_rdf.owl").load()
onto_dir_path = "static/owl_files/bio_rule_added_rdf.owl"
onto_src = get_ontology(onto_dir_path).load()
print("###################### ONTO LOADED ######################")

def build_dict(seq, key):
    """  indexing the regla list  by storid (using a dictionary),
    this way 'get' operations would be O(1) time"""
    return dict((d[key], dict(d, index=index)) for (index, d) in enumerate(seq))


def clean_rule(regla):
    # Deleting onto name and change '^' by ','
    clean_regla = regla.replace(onto_src.name + ".", '')
    clean_regla = clean_regla.replace('^', ',')
    clean_regla = clean_regla.replace('swrlb:', '')
    return clean_regla


def get_iri(name):
    new_world = owlready2.World()
    # Loading our ontologia
    onto = new_world.get_ontology(onto_dir_path).load()

    return onto.base_iri + name


def get_list_of_procesos():
    all_procesos = onto_src.search(type=onto_src.Proceso)
    proceso_list = []

    for p in all_procesos:
        iri = p.get_iri()
        nombre = p.tieneNombre
        descripcion = p.tieneDescripcion
        alimenta_proceso = [proceso.tieneNombre for proceso in p.alimentaProceso] if p.alimentaProceso else ""

        proceso_list.append({'iri': iri,
                             'nombre': nombre,
                             'descripcion': descripcion,
                             'alimenta_proceso': alimenta_proceso})
    return proceso_list


def get_list_of_variables():
    all_variables = onto_src.search(type=onto_src.Variable)
    variable_list = []

    #        for v in all_variables:
    #            print(str(v.tieneValorMaximo) if v.tieneValorMaximo else 0.0)

    #        nombre = str(v).split('.')[1]
    #        unidad =  str(v.tieneUnidadDeMedida) if v.tieneUnidadDeMedida else "No definido"
    #        maximo = v.tieneValorMaximo if v.tieneValorMaximo else 0.0
    #        minimo = v.tieneValorMinimo if v.tieneValorMinimo else 0.0
    #        nominal = v.tieneValorNominal if v.tieneValorNominal else 0.0
    #        proceso = str(v.esVariableDe).split('.',1)[1] if v.esVariableDe else "No definido"

    for v in all_variables:
        nombre = str(v).split('.')[1]
        descripcion = v.tieneDescripcion if v.tieneDescripcion else "No definido"
        unidad = str(v.tieneUnidadDeMedida) if v.tieneUnidadDeMedida else "No definido"
        maximo = v.tieneValorMaximo if v.tieneValorMaximo else 0.0
        minimo = v.tieneValorMinimo if v.tieneValorMinimo else 0.0
        nominal = v.tieneValorNominal if v.tieneValorNominal else 0.0
        proceso = (str(v.esVariableDe[0]).split('.', 1)[1]).split('_', 1)[1] if v.esVariableDe else "No definido"

        variable_list.append({'nombre': nombre,
                              'iri': v.iri,
                              'descripcion': descripcion,
                              'unidad': unidad,
                              'maximo': maximo,
                              'minimo': minimo,
                              'nominal': nominal,
                              'proceso': proceso})
    return variable_list


def get_list_of_errors():
    """To obtain a list of all errors in the ontologia and its recomendacion"""
    all_errors = onto_src.search(type=onto_src.Error)
    errors_list = []

    for e in all_errors:
        nombre = str(e).split('.')[1]
        descripcion = str(e.tieneDescripcion) if e.tieneDescripcion else "No definido"
        peligro = str(e.tieneNivelDePeligro[0]) if e.tieneNivelDePeligro else "No definido"
        variable = [str(var).split('.', 1)[1] for var in e.afectaVariable] if e.afectaVariable else "No definido"
        recomendacion = str(e.tieneRecomendacion[0]).split('.')[1] if e.tieneRecomendacion else "No definido"
        r_iri = str(e.tieneRecomendacion[0].iri) if e.tieneRecomendacion else "No definido"
        es_error_de = str(e.esErrorDe[0]) if e.esErrorDe else "No definido"
        desc_recomendacion = str(e.tieneRecomendacion[0].tieneDescripcion[0]) if e.tieneRecomendacion and \
                                                                                                e.tieneRecomendacion[
                                                                                                    0].tieneDescripcion else "No definido"
        print(r_iri)
        errors_list.append({'nombre': nombre,
                            'iri': e.iri,
                            'descripcion': descripcion,
                            'peligro': peligro,
                            'variable': variable,
                            'recomendacion': recomendacion,
                            'r_iri': r_iri,
                            'desc_recomendacion': desc_recomendacion,
                            'es_error_de': es_error_de,})
    return errors_list


def get_list_of_rules():
    # from operator import itemgetter
    # # Obtain rules from the ontologia
    # new_world = owlready2.World()
    # # Loading our ontologia
    # onto = new_world.get_ontology("static/ontologia/bio_rule_added_rdf.owl").load()
    rules = list(onto_src.rules())
    rules_list = []

    for r in rules:
        rules_list.append({'nombre': r.label[0] if r.label else "No definido",
                           'proceso': r.label[0].split('_', 1)[0] if r.label else "No definido",
                           'descripcion': r.comment[0] if r.comment else "No definido",
                           'regla': str(r),
                           'activo': r.isRuleEnabled})

    # for r in rules:
    #     rules_list.append({'nombre': r.label[0],
    #                        'proceso': r.label[0].split('_', 1)[0],  # cut string at the first '_' en return left side
    #                        'descripcion': r.comment[0] if r.comment[0] != '' else 'No definido',
    #                        'regla': str(r)})
    # return sorted(rules_list, key=itemgetter('proceso'))
    return rules_list


def get_errors(estado):
    """ To obtain the errors associated to the current state of the process"""
    #    estados = list(onto.tieneEstadoDeProceso.get_relations())
    #    estado = estados[1]
    errores = list(estado[0].presentaError)
    errores_list = []
    recomendaciones_list = []

    for e in errores:
        errores_list.append(str(e).split('.', 1)[1])
        try:
            recomendaciones_list.append(str(e.tieneRecomendacion[0]).split('.', 1)[1])
        except Exception:
            recomendaciones_list.append("Sin recomendación")
    return errores_list, recomendaciones_list


def reasoner(data):
    # creating a new world to isolate the reasoning results
    new_world = owlready2.World()
    # Loading our ontologia
    onto = new_world.get_ontology(onto_dir_path).load()
    # Creating individuals of Lectura that will be used by the rules
    onto.Variable_Dil1_Entrada.tieneValorPropuesto = float(data.da_dil1)
    onto.Lectura_AGV_Entrada.tieneValorCensado = float(data.da_agv_in)
    onto.Lectura_DQO_Entrada.tieneValorCensado = float(data.da_dqo_in)
    onto.Lectura_Biomasa_Salida.tieneValorCensado = float(data.da_biomasa_x)
    onto.Lectura_DQO_Salida.tieneValorCensado = float(data.da_dqo_out)
    onto.Lectura_AGV_Salida.tieneValorCensado = float(data.da_agv_out)
    onto.Variable_Dil2_Entrada.tieneValorPropuesto = float(data.mec_dil2)
    onto.Lectura_Ace_Salida.tieneValorCensado = float(data.mec_ace)
    onto.Lectura_xa_Salida.tieneValorCensado = float(data.mec_xa)
    onto.Lectura_xm_Salida.tieneValorCensado = float(data.mec_xm)
    onto.Lectura_xh_Salida.tieneValorCensado = float(data.mec_xh)
    onto.Lectura_mox_Salida.tieneValorCensado = float(data.mec_mox)
    onto.Lectura_imec_Salida.tieneValorCensado = float(data.mec_imec)
    onto.Lectura_QH2_Salida.tieneValorCensado = float(data.mec_qh2)

    # Apply the rules using pellet reasoner
    sync_reasoner_pellet(onto, infer_property_values=True, debug=0)
    # Obtain the list of states for each process
    estados = list(onto.tieneEstadoDeProceso.get_relations())
    # print("inside reasonoer")
    # print(estados)
    estados_list = []

    # Transform list to dictionary
    # each estado es a tuple (process, state)
    for estado in estados:
        proceso = (str(estado[0]).split('.', 1)[1]).split('_', 1)[1]
        estado_desc = str(estado[1]).split('.', 1)[1]
        estados_list.append({'proceso': proceso,
                             'estado': estado_desc,
                             # get_errors() return a tuple (errors, recomen)
                             'error': get_errors(estado)[0],
                             'recomendacion': get_errors(estado)[1]})

    # print("after for of reasoner")
    # print(estados_list)
    return estados_list


def onto_save_error(error):
    from datetime import datetime
    # creating a new world to isolate the reasoning results
    # new_world = owlready2.World()
    # # Loading our ontologia
    # onto = new_world.get_ontology("static/ontologia/bio_rule_added_rdf.owl").load()
    # afecta_variables = []
    date = datetime.strftime(error.created_at, "%Y-%m-%d %H:%M:%S+0000")
    print(date)
    # for v in error.variable.all():
    #     afecta_variables.append(v)
    e = onto_src.Error(error.nombre,
                   namespace=onto_src,
                   tieneDescripcion=error.descripcion,
                   tieneFechaDeActualizacion=[date],
                   tieneNivelDePeligro=[error.peligro],
                   tieneNombre=error.nombre,
                   esErrorDe=[error.es_error_de],)
    for v in error.variable.all():
        e.afectaVariable.append(onto_src[v])

    onto_src.save(onto_dir_path, format="rdfxml")


def onto_update_error(old_error, updated_error, fields_updated):
    from datetime import datetime
    date = datetime.strftime(updated_error.updated_at, "%Y-%m-%d %H:%M:%S+0000")
    # new_world = owlready2.World()
    # # Loading our ontologia
    # onto = new_world.get_ontology("static/ontologia/bio_rule_added_rdf.owl").load()

    if 'nombre' in fields_updated:
        error_onto = onto_src[old_error.nombre]
        error_onto.iri = onto_src.base_iri + updated_error.nombre  # Change old iri name for the new one

    print(updated_error.nombre)
    error_onto = onto_src[updated_error.nombre]
    print(onto_src[updated_error.nombre])

    # Update variables affected
    if 'variable' in fields_updated:
        variables_from_request = [onto_src[var] for var in updated_error.variable.all()]
        error_onto.afectaVariable.clear()
        print("List cleared")
        error_onto.afectaVariable = variables_from_request
        print("New elements added")

    error_onto.tieneDescripcion = updated_error.descripcion
    error_onto.tieneNivelDePeligro = [updated_error.peligro]
    error_onto.esErrorDe = [updated_error.es_error_de]
    error_onto.tieneFechaDeActualizacion = [date]
    print("Error updated")
    onto_src.save(onto_dir_path, format="rdfxml")


def onto_save_recomendacion(recomendacion):
    from datetime import datetime
    # creating a new world to isolate the reasoning results
    new_world = owlready2.World()
    # Loading our ontologia
    onto = new_world.get_ontology(onto_dir_path).load()
    date = datetime.strftime(recomendacion.created_at, "%Y-%m-%d %H:%M:%S+0000")

    r = onto.Recomendacion(recomendacion.nombre,
                           namespace=onto,
                           tieneDescripcion=recomendacion.descripcion,
                           tieneFechaDeActualizacion=[date],
                           tieneNombre=recomendacion.nombre)
    for e in recomendacion.error.all():
        print(e)
        print(onto[e])
        r.esRecomendacionDe.append(onto[e])

    onto.save(onto_dir_path, format="rdfxml")


def onto_update_recomendacion(recomendacion, fields_updated):
    from datetime import datetime
    date = datetime.strftime(recomendacion.updated_at, "%Y-%m-%d %H:%M:%S+0000")

    recomendacion_iri = recomendacion.iri.split("#")[1]
    print(recomendacion_iri)
    recomendacion_onto = onto_src[recomendacion_iri]
    print(recomendacion_onto)


    if 'nombre' in fields_updated:
        recomendacion_onto.iri = onto_src.base_iri + recomendacion.nombre  # Change old iri name for the new one
        recomendacion_onto.tieneNombre = recomendacion.nombre

    # Update the Error to which belongs the current recomendacion
    if 'error' in fields_updated:
        errores_from_request = [onto_src[err] for err in recomendacion.error.all()]
        print(errores_from_request)
        recomendacion_onto.esRecomendacionDe.clear()
        print("List cleared")
        recomendacion_onto.esRecomendacionDe = errores_from_request
        print("New elements added")

    recomendacion_onto.tieneDescripcion = recomendacion.descripcion
    recomendacion_onto.tieneFechaDeActualizacion = [date]

    print("recomendacion_onto updated")
    onto_src.save(onto_dir_path, format="rdfxml")


def onto_save_regla(regla):
    with onto_src:
        r = Imp()  # Create a new instance of rule
        r.set_as_rule(clean_rule(regla.regla))  # Setting the cleaned rule
        r.label = [regla.nombre]
        r.comment = [regla.descripcion if regla.descripcion != '' else 'No definido']
        r.isRuleEnabled = [regla.activo]  # To enable the new rule
    onto_src.save(onto_dir_path, format="rdfxml")
    print("Regla creada")


def onto_update_regla(new_r, old_r):
    list_of_rules = get_list_of_rules()
    dic_of_rules = build_dict(list_of_rules, key='nombre')
    rules = list(onto_src.rules())
    rule_position = dic_of_rules.get(old_r.nombre)['index']
    r = rules[rule_position]
    print("rule which will be changed is {}".format(old_r.nombre))
    print("rule in dict rule position {} is {}".format(rule_position, dic_of_rules.get(old_r.nombre)))
    print("rule in rule position {} is {}".format(rule_position, r.label))

    r.label = new_r.nombre  # Change old  name for the new one
    r.comment = new_r.descripcion
    r.isRuleEnabled = [new_r.activo]
    r.set_as_rule(clean_rule(new_r.regla))

    print("Regla updated")
    onto_src.save(onto_dir_path, format="rdfxml")


def onto_delete_regla(nombre):
    rules = list(onto_src.rules())
    list_of_rules = get_list_of_rules()

    position = next((index for (index, d) in enumerate(list_of_rules) if d["nombre"] == nombre), None)
    print(position)
    print(nombre)

    destroy_entity(rules[position], undoable=True)

    onto_src.save(onto_dir_path, format="rdfxml")
    print("Regla Eliminada")


def onto_delete_individual(iri):
    nombre = iri.split("#")[1]
    print(nombre)
    individual_onto = onto_src[nombre]
    print(individual_onto)
    destroy_entity(individual_onto)
    print("individual {} deleted".format(individual_onto))
    onto_src.save(onto_dir_path, format="rdfxml")
