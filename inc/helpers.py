import os
from datetime import datetime
import sys


def argument_or_input(message, index):
    if len(sys.argv) < index + 1:
        print(message)
        path = input()
    else:
        path = sys.argv[index]

    return path


def output_info(message):
    print(prepare_output('INFO', message))


def output_error(message):
    print(prepare_output('ERR', message))


def prepare_output(type, message):
    date_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return f'[{type}]: [{date_time}] {message}'


def get_files_from_dir(path):
    if not os.path.isdir(path):
        raise ValueError('Provided path is not a valid directory')

    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
