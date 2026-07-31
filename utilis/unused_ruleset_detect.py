from yaml_read_write import *

data = load_yaml("rules\\rules_others.yaml")

rules = []
for r in data['rules']:
    rule = r.split(',')
    if rule[0] == 'RULE-SET':
        rules.append(rule[1])

rule_set = [ group for group in data['rule-providers'] ]

print("No rulesets for ", set(rules) - set(rule_set))
print("No rules for ", set(rule_set) - set(rules))