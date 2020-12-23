import os
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
            info(f"Checking hostname: {hostname}")
            negatives = vt_client.is_host_secure(hostname)
            message = 'No negative feedback' if negatives < 1 else f'{negatives} services reported the host as malicious / suspicious'
            info(message)

        file_handler.close()
        os.rename(file_path, f'{file_path}.done')
except ValueError as e:
    error(e)
