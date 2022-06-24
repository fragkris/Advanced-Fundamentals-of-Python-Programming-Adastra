import os
import json
import hcl
import ast

cfn = [".json", ".template", ".yaml", ".yml"]
tf = ["tf"]


def file_handler(dir):
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith(tuple(cfn)):
                with open(os.path.join(root, file), 'r') as fin:
                    try:
                        file = fin.read()
                        if "awstemplateformatversion" in file:
                            data = json.dumps(file)
                            print(data)
                    except ValueError as e:
                        raise SystemExit(e)
            elif file.endswith(tuple(tf)):
                with open(os.path.join(root, file), 'r') as file:
                    try:
                        obj = hcl.load(file)
                        data = json.dumps(obj)
                        print(data)
                    except ValueError as e:
                        raise SystemExit(e)
    return data



funcdef = ast.parse("""
def file_handler(dir):
    for root, dirs, files in os.walk(dir):#+1
        for file in files:# +2
            if file.endswith(tuple(cfn)):# +3
                with open(os.path.join(root, file), 'r') as fin:
                    try:# +4
                        file = fin.read()
                        if "awstemplateformatversion" in file:#+5
                            data = json.dumps(file)
                            print(data)
                    except ValueError as e:
                        raise SystemExit(e)
            elif file.endswith(tuple(tf)):#+2
                with open(os.path.join(root, file), 'r') as file:
                    try: # +3
                        obj = hcl.load(file)
                        data = json.dumps(obj)
                        print(data)
                    except ValueError as e:
                        raise SystemExit(e)
    return data
    """).body[0]

from cognitive_complexity.api import get_cognitive_complexity
print("Cognitive complexity =",get_cognitive_complexity(funcdef))
