# encoding: utf-8
import requests
import os
import json
import yaml
from sqlalchemy import create_engine


host = 'http://192.168.1.22:8101'
token_url = '/api/login'
del_case = '/api/cases/'


def get_token():
    login = req_api(
        url=host+token_url,
        method='POST',
        data={
            "username": "shukun",
            "password": "06a86ffbd63e1366951b2da9af7cbd2640dcc60b848f74eb22585d4ef3fbc0af"
            },
        headers={'Content-Type': 'application/json'}
        )
    return json.loads(login)['token']


def clean_cases():
    listdir = os.listdir(os.path.join(os.getcwd(), 'cta_srv_cases'))
    case_list = [x for x in listdir if x.startswith('P')]
    token = str(get_token())
    try:
        for y in case_list:
            result = req_api(url=host+del_case+y,
                             method='post',
                             data=None,
                             headers={'Authorization': token})
            print("{y}: {result}".format(y=y, result=result))
    except Exception as e:
        print(e)


def req_api(url, method, data, headers):
    method = method.upper()
    if method == 'GET':
        req = requests.get(url, params=data, headers=headers)
        return req.text

    elif method == 'POST':
        if not data:
            req = requests.post(url, json={}, headers=headers)
        elif isinstance(data, dict):
            req = requests.post(url, json=data, headers=headers)
        else:
            req = requests.post(url, data=data, headers=headers)
        return req.text

    elif method == 'DELETE':
        req = requests.delete(url)
        return req.text

    else:
        return


def sql_engine():
    with open('coronary.yml', 'r') as f:
        res = yaml.load(f, Loader=yaml.SafeLoader)
        db_uri = res.get('QLALCHEMY_DATABASE_URI')
        engine = create_engine(db_uri)
        return engine


def clean_mysql(case_num, record=False):
    engine = sql_engine()
    if record:
        engine.execute("delete from feedbacks where 1=1")
        engine.execute("delete from issues where 1=1")
    engine.execute("delete from cases where case_num='{}'".format(case_num))





if __name__ == '__main__':
    print(get_token())
