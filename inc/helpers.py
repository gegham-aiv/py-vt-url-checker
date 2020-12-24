import os
from datetime import datetime
import sys

from slugify import slugify


def argument_or_input(message, index):
    arguments = get_args()
    if len(arguments) < index + 1:
        print(message)
        path = input()
    else:
        path = arguments[index]

    return path


def get_option(name, alias):
    options = get_options()
    return f'--{name}' in options or f'-{alias}' in options


def get_options():
    return list(filter(lambda arg: arg.startswith('-'), sys.argv))


def get_args():
    return list(filter(lambda arg: not arg.startswith('-'), sys.argv))


def output_info(message):
    print(prepare_output('INFO', message))


def mkdir(path):
    # create a directory if not already exists
    if not os.path.isdir(path):
        os.makedirs(path)


def output_error(message):
    print(prepare_output('ERR', message))


def prepare_output(type, message):
    date_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return f'[{type}]: [{date_time}] {message}'


def get_files_from_dir(path):
    if not os.path.isdir(path):
        raise ValueError('Provided path is not a valid directory')

    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]


def get_out_file_name(hostname, path):
    out_dir_name = get_out_dir_name(path)
    # create the directory for saving output for the specific category if does not exist yet
    mkdir(out_dir_name)
    return f'{out_dir_name}/{slugify(hostname)}_VTResults.json'


def get_out_dir_name(path):
    dir = f'out/{os.path.splitext(path)[0]}'
    mkdir(dir)
    return dir
