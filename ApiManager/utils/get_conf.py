from yaml import load
import os


config_path = os.path.join(os.path.dirname(__file__), 'runner.yaml')


def get_value_by_key(runner_key):
    with open(config_path, 'rb') as f:
        cont = f.read()
    cf = load(cont)
    return cf.get(runner_key)
