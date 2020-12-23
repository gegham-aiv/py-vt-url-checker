from slugify import slugify
import os
import json
from inc.vtclient import VTClient
from inc.helpers import argument_or_input, output_info as info, output_error as error, get_files_from_dir

try:
    path = argument_or_input('Please provide the path to directory where the files are located:', 1)
    # retrieving the list of all files
    files = get_files_from_dir(path)
    # filtering the files which have been marked as "done"
    files = list(filter(lambda file: not file.endswith('.done'), files))

    info(f"Total {len(files)} files detected")
    vt_client = VTClient()
    for file in files:
        info(f"Reading file {file}")
        file_path = f"{path}/{file}"
        file_handler = open(file_path, 'r')
        lines = file_handler.readlines()

        for hostname in lines:
            hostname = hostname.strip()
            info(f"Checking hostname: {hostname}")
            results = vt_client.check_host(hostname)
            negatives = results['malicious'] + results['suspicious']
            message = 'Not Suspicious' if negatives < 1 else f'{negatives} services reported the host as malicious / suspicious'
            info(message)
            data_to_save = {}
            data_to_save[hostname] = message
            json_data = json.dumps(data_to_save, sort_keys=True, indent=4)
            if not os.path.isdir('out'):
                os.makedirs('out')
            dir_name = f'out/{os.path.splitext(file)[0]}'
            if not os.path.isdir(dir_name):
                os.makedirs(dir_name)
            safe_host_name = slugify(hostname)
            safe_file_name = f'{dir_name}/{safe_host_name}.json'
            json_file_handler = open(safe_file_name, "w+")
            json_file_handler.write(json_data)
            json_file_handler.close()

        file_handler.close()
        os.rename(file_path, f'{file_path}.done')
except ValueError as e:
    error(e)
