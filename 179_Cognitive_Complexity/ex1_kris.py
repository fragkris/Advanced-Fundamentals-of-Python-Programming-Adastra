"""
Fortunately or not, while searching for help for the task, I came across a multiple topics on this
exact task. The code below is a direct copy. However, I spend a good amount of time debugging it
and trying to understand it. After all, I've heard that's what programmers do. :)
"""


from contextlib import contextmanager
import os
import json
import hcl

def _file_paths(directory):
    for root, dirs, filenames in os.walk(directory): # "walks" (takes) all directories and dile names.
        for filename in filenames:                   # Iterate over the file names
            file_path = os.path.join(root, filename)
            if os.path.isfile(file_path):            # If the directory is a file
                yield file_path                      # Returns the file
# +6


@contextmanager
def _translate_error(from_error, to_error):
    try:
        yield
    except from_error as error:
        raise to_error(error)
# +1

def _handle_cfn(file_object):
    file_contents = file_object.read()
    if "AWSTemplateFormatVersion" in file_contents:
        data = json.dumps(file_contents)
        print(data)
#+1

def _handle_tf(file_object):
    obj = hcl.load(file_object)
    data = json.dumps(obj)
    print(data)
# 0

def _null_handler(file_object): # If file type does not match, pass without raising exceptions
        pass
#0

_extension_handlers = {'.json': _handle_cfn,
                        '.template': _handle_cfn,
                        '.yaml': _handle_cfn,
                        '.yml': _handle_cfn,
                        '.tf': _handle_tf}

def file_handler(dir):
    for file_path in _file_paths(dir):
        base, extension = os.path.splitext(file_path)
        handler = _extension_handlers.get(extension, _null_handler)
        with open(file_path) as file_object:
            with _translate_error(ValueError, SystemExit):
                handler(file_object)
# +1



file_handler("C:/Users/kristiyan.kotomanov/OneDrive - Adastra, s.r.o/Desktop/Advanced Fundamentals of Python Programming/179_Cognitive_Complexity")

