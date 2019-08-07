# encoding: utf-8
import requests
import os
import json

# 地址改下
host = 'http://192.168.1.91:6988'
token_url = '/api/login'
del_case = '/api/cases/'


def get_token():
    login = requests.post(
        url=host+token_url,
        json={
            "username": "shukun",
            "password": "06a86ffbd63e1366951b2da9af7cbd2640dcc60b848f74eb22585d4ef3fbc0af"
            },
        headers={'Content-Type': 'application/json'}
        )
    return json.loads(login.text)['token']

def clean_cases(case_num):
    try:
        result = requests.delete(url=host+case_num+y,
                                    headers={'Authorization': str(get_token())})
        print(result.text)
    except Exception as e:
        print(e)
    else:
        clean_mysql_case(case_num)
        pass

def clean_mysql_case(case_num):
    from sqlalchemy import create_engine
    import yaml
    # 完整的数据库地址地址
    with open('/data0/rundata/coronary.yml', 'r') as f:
        res = yaml.load(f, Loader=yaml.SafeLoader)
    # 配置地址样例
    # SQLALCHEMY_DATABASE_URI: "mysql+pymysql://shukun:shukun123@localhost:5506/cta?charset=utf8mb4"    
    DB_URI = res.get('SQLALCHEMY_DATABASE_URI')
    print(DB_URI)
    engine = create_engine(DB_URI)
    engine.execute("delete from feedbacks where case_id={};".format(case_num))
    engine.execute("delete from issues where case_id={};".format(case_num))
    engine.execute("delete from case_statistics  where case_id={};".format(case_num))
    engine.execute("delete from cases where case_num={};".format(case_num))
    print('suceess remove cases')


if __name__ == '__main__':
    # clean_cases(os.argv[1])
    print(1)