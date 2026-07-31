from yaml_read_write import *

area = ''
client= ''
file = create_config_file_name(area, client, test=False, prefix=None)
config = load_yaml(file)
        
rule_choose_group = [rule.split(',')[2] for rule in config['rules'][:-1]]
proxy_group = [group['name'] for i, group in enumerate(config['proxy-groups'])]

print("Uncreated proxy group: ", set(rule_choose_group) - set(proxy_group))
