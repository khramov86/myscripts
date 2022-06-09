from copy import copy
import sys

import yaml
import json

src_filename = sys.argv[1]
dest_filename = sys.argv[2]
try:
    with open(src_filename) as file:
        report_dict = {}
        dep_dict = yaml.safe_load(file).get('user_list')
        if not dep_dict:
            print("Please specify file with correct structure")
        for root_key, root_value in dep_dict.items():
            depth = 1
            value = root_value
            while isinstance(value, dict):
                if not value:
                    break
                depth += 1
                temp_dict = dict()
                for key in value.keys():
                    if isinstance(value[key], dict):
                        iter_list = copy(value[key])
                        for sub_key in iter_list:
                            new_sub_key = sub_key
                            if sub_key in temp_dict:
                                while new_sub_key in temp_dict:
                                    new_sub_key += "_dupkeys"
                                temp = value[key][sub_key]
                                del value[key][sub_key]
                                value[key][new_sub_key] = temp
                        temp_dict = {**temp_dict, **value[key]}
                value = temp_dict
            report_dict[root_key] = depth
except Exception as e:
    print(f"No such file or directory {e}")
with open(dest_filename, 'w', encoding='utf-8') as file:
    print(json.dumps(report_dict, ensure_ascii=False), file=file)
