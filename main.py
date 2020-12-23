import os
import json
from inc.vtclient import VTClient
from inc.helpers import argument_or_input, output_info as info, output_error as error, get_files_from_dir, \
    get_out_file_name

try:
    path = argument_or_input('Please provide the path to directory where the files are located:', 1)
    num = int(argument_or_input('Please provide a number of entities to be scanned', 2))
    # create the directory for saving output if does not exist
    if not os.path.isdir('out'):
        os.makedirs('out')

    # retrieving the list of all files
    files = get_files_from_dir(path)
    # filtering the files which have been marked as "done"
    files = list(filter(lambda f: not f.endswith('.done'), files))

    entities_scanned = 0
    provided_entities_number_scanned = False

    info(f"Total {len(files)} files detected")
    vt_client = VTClient()
    for file in files:
        if provided_entities_number_scanned:
            break
        info(f"Reading file {file}")
        file_path = f"{path}/{file}"
        file_handler = open(file_path, 'r')
        hostnames = file_handler.readlines()

        for hostname in hostnames:
            if entities_scanned >= num:
                provided_entities_number_scanned = True
                break
            hostname = hostname.strip()
            out_file_name = get_out_file_name(hostname, file)
            if os.path.isfile(out_file_name):
                # this hostname has already been scanned
                continue

            info(f"Checking hostname: {hostname}")
            results = vt_client.check_host(hostname)
            negatives = results['malicious'] + results['suspicious']
            message = 'Not Suspicious'
            if negatives > 0:
                message = f'{negatives} services reported the host as malicious / suspicious'
            info(message)
            data_to_save = {hostname: message}
            json_data = json.dumps(data_to_save, sort_keys=True, indent=4)
            json_file_handler = open(out_file_name, "w+")
            json_file_handler.write(json_data)
            json_file_handler.close()
            entities_scanned += 1

        file_handler.close()
        os.rename(file_path, f'{file_path}.done')
except ValueError as e:
    error(e)
