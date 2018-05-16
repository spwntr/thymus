import json
import logging
import random
from sys import stdout

from neo4j.util import watch
from neo4j.v1 import GraphDatabase

UNQUERYABLE = ['Left ventricle', 'Right ventricle', 'Right adrenal gland', 'Left adrenal gland', 'Ureter', 'Esophagus',
               'Myocardium of left atrium', 'Myocardium of right atrium', 'Myocardium of right ventricle',
               'Myocardium of left ventricle', 'Left atrium', 'Right atrium', 'Hippocampus proper', 'Clavicle',
               'Small intestine', 'Deltoid', 'Urinary bladder', 'Left kidney', 'Right kidney',
               'Anterior wall of right ventricle', 'Lung', 'Right clavicle', 'Left clavicle',
               'Superior segment of right kidney', 'Superior segment of left kidney', 'Superior segment of kidney',
               'Wall of tail of epididymis', 'Midbrain', 'Precentral gyrus', 'Postcentral gyrus', 'Kidney', ]
MYOCARDIAL_ZONE = 'Myocardial zone'
RENAL_SEGMENT = 'renal segment'

watch("neo4j.bolt", logging.DEBUG, stdout)


def query_for_blood_paths(tx, tissue):
    return tx.run(
        "MATCH ({ preferred_name: $tissue })-[:ARTERIAL_SUPPLY]->(n), "
        "(a { preferred_name: 'Aorta' }), "
        "p = shortestPath((a)-[:REGIONAL_PART_OF|:CONTINUOUS_DISTALLY_WITH|:BRANCH_OF*]-(n)) "
        "WHERE NONE(x IN NODES(p) WHERE x:Class AND x.preferred_name = 'Systemic arterial tree') "
        "RETURN extract(i IN NODES(p) | i.preferred_name)"
        , tissue=tissue
    )


def query_for_tissues_w_arterial_supply_defined(tx):
    return tx.run(
        "MATCH (n)-[:ARTERIAL_SUPPLY]->() "
        "WITH DISTINCT n "
        "RETURN collect(n.preferred_name)"
    )


def import_all_blood_paths():
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "pw4neo"))

    with driver.session() as session:
        tissues = session.write_transaction(query_for_tissues_w_arterial_supply_defined)

        counter = 1
        questions = []
        for tissue in tissues._records[0][0]:
            if not tissue.__contains__(RENAL_SEGMENT) and not tissue.__contains__(MYOCARDIAL_ZONE) \
                    and not UNQUERYABLE.__contains__(tissue):
                blood_paths = session.write_transaction(query_for_blood_paths, tissue)
                for path in blood_paths._records:
                    questions.append({
                        'id': counter,
                        'subject': tissue,
                        'blood_path': path[0]
                    })
                    counter += 1
                    print(counter)

    with open('data/questions.json', 'w') as file:
        json.dump(questions, file, indent=4)


def get_questions_as_dict():
    with open('data/questions.json') as json_data:
        return json.load(json_data)


def get_wrong_id(question_to_return, wrong_ids):
    wrong_id = question_to_return['id'].__str__()
    while wrong_id.__eq__(question_to_return['id'].__str__()) \
            or wrong_ids.__contains__(wrong_id):
        wrong_id = random.randint(1, 427).__str__()

    return wrong_id


def get_question_by_id(id):
    if not type(id) is str:
        id = id.__str__()
    question_to_return = None
    questions = get_questions_as_dict()

    for question in questions:
        q_id = question['id'].__str__()
        if q_id.__eq__(id):
            question_to_return = question

    wrong_ids = []
    for i in range(4):
        wrong_ids.append(get_wrong_id(question_to_return, wrong_ids))

    wrong_paths = []
    wrong_options = []
    blood_path_ = question_to_return['blood_path']
    for question in questions:
        q_id = question['id'].__str__()
        wrong_option = question['blood_path']
        if wrong_ids.__contains__(q_id) \
                and not wrong_option[-1].__eq__(blood_path_[-1]):
            wrong_paths.append(question)
            wrong_options.append(wrong_option)

    randomized_path = list(blood_path_)
    random.shuffle(randomized_path)
    question_to_return['randomized_path'] = randomized_path
    question_to_return['wrong_paths'] = wrong_paths
    wrong_options.append(blood_path_)
    question_to_return['randomized_options'] = wrong_options
    random.shuffle(question_to_return['randomized_options'])
    return question_to_return
