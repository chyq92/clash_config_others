from ruamel.yaml import YAML
import os

def load_yaml(file_path):
    yaml = YAML()
    yaml.default_flow_style = True
    yaml.allow_unicode = True
    yaml.preserve_quotes = True
    yaml.line_break = '\n'
    folder_path = os.getcwd()
    file_path = os.path.join(folder_path, file_path)
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.load(file)

def create_config_file_name(area, client, test=False, prefix=None):
    file = "configs\\"
    if client == 'home':
        client = 'openclash'
    if prefix:
        file += prefix + "_"
    file += client + "_" + area + "_config"
    if test:
        file += "_test"
    file += ".yaml"
    return file

def save_yaml(data, output_file):
    yaml = YAML()
    yaml.default_flow_style = False
    yaml.allow_unicode = True
    yaml.line_break = '\n'
    yaml.width = 300
    folder_path = os.getcwd()
    output_file = os.path.join(folder_path, output_file)
    with open(output_file, 'w', encoding='utf-8') as file:
        yaml.dump(data, file)

def load_yaml_old(file_path):
    yaml = YAML(typ='safe')
    yaml.default_flow_style = True
    yaml.allow_unicode = True
    yaml.line_break = '\n'
    folder_path = os.getcwd()
    file_path = os.path.join(folder_path, file_path)
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.load(file)