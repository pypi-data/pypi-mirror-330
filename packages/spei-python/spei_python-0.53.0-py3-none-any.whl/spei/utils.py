import re


def to_upper_camel_case(string):
    temp = string.split('_')
    new_string = [ele.title() for ele in temp]
    return ''.join(new_string)


def to_snake_case(string):
    return re.sub('(.)([A-Z0-9])', r'\1_\2', str(string)).lower()
