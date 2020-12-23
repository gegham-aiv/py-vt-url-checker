import json
import os

from inc.vtclient import VTClient
from inc.helpers import output_info as info, get_out_file_name


class Scanner:
    def __init__(self, path, num):
        self.path = path
        self.client = VTClient()
        self.num = num
        self.out_path = 'out'
        # create the directory for saving output if does not exist
        if not os.path.isdir(self.out_path):
            os.makedirs(self.out_path)

    def start(self):
        # retrieving the list of all files
        files = self.get_files()
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
            file_path = f"{self.path}/{file}"
            file_handler = open(file_path, 'r')
            hostnames = file_handler.readlines()

            for hostname in hostnames:
                if entities_scanned >= self.num:
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

    def get_files(self):
        if not os.path.isdir(self.path):
            raise ValueError('Provided path is not a valid directory')

        return [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]
