from slugify import slugify
import os
import json
from inc.vtclient import VTClient
from inc.helpers import argument_or_input, output_info as info, output_error as error, get_files_from_dir

try:
    path = argument_or_input('Please provide the path to directory where the files are located:', 1)
    num = argument_or_input('Please provide a number of entities to be scanned', 2)
    # create the directory for saving output if does not exist
    if not os.path.isdir('out'):
        os.makedirs('out')

    # retrieving the list of all files
    files = get_files_from_dir(path)
    # filtering the files which have been marked as "done"
    files = list(filter(lambda file: not file.endswith('.done'), files))

    entities_scanned = 0
    provided_entities_number_scanned = False

    info(f"Total {len(files)} files detected")
    vt_client = VTClient()
    for file in files:
        if (provided_entities_number_scanned):
            break
        info(f"Reading file {file}")
        out_dir_name = f'out/{os.path.splitext(file)[0]}'
        # create the directory for saving output for the specific category if does not exist yet
        if not os.path.isdir(out_dir_name):
            os.makedirs(out_dir_name)
        file_path = f"{path}/{file}"
        file_handler = open(file_path, 'r')
        lines = file_handler.readlines()

        for hostname in lines:
            if (entities_scanned >= num):
                provided_entities_number_scanned = True
                break
            hostname = hostname.strip()
            out_file_name_safe = f'{out_dir_name}/{slugify(hostname)}.json'
            if (os.path.isfile(out_file_name_safe)):
                # this hostname has already been scanned
                continue

            info(f"Checking hostname: {hostname}")
            results = vt_client.check_host(hostname)
            negatives = results['malicious'] + results['suspicious']
            message = 'Not Suspicious' if negatives < 1 else f'{negatives} services reported the host as malicious / suspicious'
            info(message)
            data_to_save = {}
            data_to_save[hostname] = message
            json_data = json.dumps(data_to_save, sort_keys=True, indent=4)
            json_file_handler = open(out_file_name_safe, "w+")
            json_file_handler.write(json_data)
            json_file_handler.close()
            entities_scanned += 1

        file_handler.close()
        os.rename(file_path, f'{file_path}.done')
except ValueError as e:
    error(e)
