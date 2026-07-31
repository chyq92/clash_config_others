# Generating config files for others
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utilis.yaml_read_write import *
from shadowrocket_convert import *
import copy

def config_create(area, client):
    print(f"--------Start to create config files for others {client} in {area}.--------")
    basic = load_yaml("basic\\basic_others.yaml")
    proxy_providers = load_yaml("outbounds\\proxy_providers_others.yaml")
    proxy_groups = load_yaml("proxy_groups\\proxy_groups_others.yaml")
    rules = load_yaml("rules\\rules_others.yaml")
    dns = load_yaml("dns\\dns_others.yaml")

    if client == 'clash_verge':
        basic['find-process-mode'] = 'strict'
    if client == "shadowrocket":
        config = copy.deepcopy( proxy_groups | rules )
    else:
        config = copy.deepcopy( basic | dns | proxy_providers | proxy_groups | rules )
    print("all files are loaded.")
    return config

def remove_exclude_filter(group):
    if 'exclude-filter' in group:
        if 'filter' in group:
            group['filter'] = f"^(?!.*(?i:{group['exclude-filter'][4:]}))(?=.*(?i:{group['filter'][4:]})).*$"
        else:
            group['filter'] = f"^(?!.*(?i:{group['exclude-filter'][4:]})).*$"
        del group['exclude-filter']
    return group

def config_processing(config, area, client):
    if client == "shadowrocket":
        # modify proxy_groups
        part = config['proxy-groups']
        for read_idx in range(len(part)):
            group = part[read_idx]
            group = remove_exclude_filter(group)
            if 'proxies' in group:
                group['proxies'].fa.set_block_style()
                if group['name'] in ['🐟 漏网之鱼']:
                    group['proxies'].insert(0,'PROXY')
                elif group['name'] in ['🚀 节点选择']:
                    group['proxies'].insert(1,'PROXY')
            group.fa.set_block_style()

        # modify rules
        config['rules'].insert(0,"AND,((NETWORK,UDP),(DST-PORT,443)),DIRECT")

    print("proxies, proxy_group and rules are modified.")

def config_write(config, area, client, prefix='others', test=False):
    output_file = create_config_file_name (area, client, test, prefix)
    save_yaml(config, output_file)
    print(f"--------{output_file} is generated.--------")
    
if __name__ == "__main__":
    # config = config_create("cn", "openclash")
    # config_processing(config, "cn", "openclash")
    # config_write(config, "cn", "openclash")
    
    # config = config_create("cn", "clash_verge")
    # config_processing(config, "cn", "clash_verge")
    # config_write(config, "cn", "clash_verge")

    config = config_create("cn", "shadowrocket")
    config_processing(config, "cn", "shadowrocket")
    config_write(config, "cn", "shadowrocket")
    shadowrocket_convert("cn", "shadowrocket", basic=True)