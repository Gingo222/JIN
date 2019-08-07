# -*- coding: utf-8 -*-


def select_user_state(name):
    return "SELECT state FROM cta.cases where patient_name = '" + str(name) + "';"


def update_user_state(name):
    return "UPDATE cta.cases SET state='2' WHERE patient_name = '" + str(name) + "';"
