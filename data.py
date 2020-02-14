import json
import random


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
