import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utilis.yaml_read_write import *
import copy

def update_basic_file(area):
    with open("basic\\shadowrocket_basic_others.conf", "r", encoding="utf-8") as b:
        basic_output = b.readlines()
    dns = load_yaml(f"dns\\dns_others.yaml")

    for i in range(len(basic_output)):
        line = basic_output[i]
        if line.startswith('always-real-ip'):
            basic_output[i] = f"always-real-ip = {','.join(dns['dns']['fake-ip-filter'])}" + '\n'
        elif line.startswith('proxy-dns-server'):
            basic_output[i] = f"proxy-dns-server = {','.join(dns['dns']['proxy-server-nameserver'])}" + '\n'
        elif line.startswith('dns-server'):
            if area == 'cn':
                basic_output[i] = f"dns-server = https://dns.alidns.com/dns-query, https://doh.pub/dns-query" + '\n'
            else:
                basic_output[i] = f"dns-server = {', '.join(dns['dns']['nameserver'])}" + '\n'
    return basic_output

def write_conf_file(output, file, area, basic=False):
    # Join lines and save to a text file
    # final_text = "\n".join(output).strip()
    final_text = [line + '\n' for line in output]

    if basic:
        basic_output = update_basic_file(area)
        # final_text = basic_output + "\n" + final_text
        final_text = basic_output + ["\n"] + final_text

    output_file = file.replace('yaml','conf')
    with open(output_file, "w", encoding="utf-8") as f:
        # f.write(final_text)
        f.writelines(final_text)
    print(f"--------{output_file} is generated.--------")

def shadowrocket_convert(area, client, basic=False, test=False, prefix="others"):
    file = create_config_file_name(area, client, test, prefix)
    config = load_yaml(file)
    
    output=[]
    for part in config:
        if part not in  ['proxies', 'rule-providers']:
        # Append the header block for the current part
            if part == 'proxy-groups':
                output.append(f"[Proxy Group]")
            elif part == 'rules':
                output.append(f"[Rule]")

            # Iterate through the list of items under this part
            for element in config[part]:
                try:
                    if part == 'proxy-groups':
                        newline = f"{element['name']} = {element['type']}"
                        if 'proxies' in element:
                            newline += f",{','.join(element['proxies'])}"
                        elif 'use' in element:
                            newline += f",{','.join(element['use'])},use=true"
                        if 'filter' in element:
                            newline += f",policy-regex-filter={element['filter']}"
                        if element['type'] != 'select':
                            for key, value in element.items():
                                if key in ['interval', 'tolerance', 'url']:
                                    newline += f",{key}={value}"

                    elif part == 'rules':
                        if 'RULE-SET' in element:
                            rule = element.split(',')
                            rule[1] = config['rule-providers'][rule[1]]['url']
                            newline = ",".join(rule)
                        else:
                            newline = element.replace('MATCH', 'FINAL')

                    output.append(newline)
                except:
                    print(element)

        # Optional: Add a blank line between sections for better readability
        output.append("")

    write_conf_file(output, file, area, basic)

if __name__ == "__main__":
    
    shadowrocket_convert('cn', 'shadowrocket', basic=True)