import json
import os
import re
import warnings


def readfile_or_default(fp, default=''):
    if os.path.exists(fp):
        with open(fp) as fd:
            return fd.read()
    return default


def count_slashes(input_string):
    dot_count = 0
    for char in input_string:
        if char == '/':
            dot_count += 1
    return dot_count


def is_name_legit(input_string):
    """
    Checks the validity of a given input string as per specified constraints.

    The function verifies if the input string:
    1. Starts with an alphabetic character (a-z or A-Z).
    2. Contains only alphanumeric characters (a-z, A-Z, 0-9), underscores ('_'), or
       hyphens ('-') after the initial character.

    Args:
        input_string: The string to check for validity.

    Returns:
        bool: True if the input string is valid according to the specified
        constraints, otherwise False.
    """
    return bool(re.match(r'^(?=[a-zA-Z])[a-zA-Z0-9_-]*$', input_string))


def parse_dataset_name(name: str):
    s_count = count_slashes(name)
    if s_count == 1:
        username, dataset_name = name.split('/')
    else:
        raise ValueError('dataset name must be [username]/[dataset_name]')

    if not is_name_legit(username) or not is_name_legit(dataset_name):
        raise ValueError('dataset name and store name must startswith a-zA-Z, and contains only [a-zA-Z0-9_-]')

    return username, dataset_name


def read_jsonl(line_stream):
    for line in line_stream:
        try:
            yield json.loads(line)
        except json.decoder.JSONDecodeError:
            pass


def id_function(x):
    return x


def get_tqdm(silent=False):
    if silent:
        return id_function
    try:
        import tqdm
        return tqdm.tqdm
    except ModuleNotFoundError as e:
        warnings.warn('cannot load module tqdm, maybe it is not installed ?', UserWarning)
        return id_function


def parse_tags(tag: str) -> list[str]:
    return [t.strip() for t in tag.split(',') if t.strip() != '']
