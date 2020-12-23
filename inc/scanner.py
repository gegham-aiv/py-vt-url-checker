import json
import os

from inc.vtclient import VTClient
from inc.helpers import output_info as info, get_out_file_name


class Scanner:
    def __init__(self, path, num, verbose = False):
        self.path = path
        self.client = VTClient()
        self.num = num
        self.out_path = 'out'
        self.entities_scanned = 0
        self.needed_entities_scanned = False
        self.print = verbose
        # create the directory for saving output if does not exist
        if not os.path.isdir(self.out_path):
            os.makedirs(self.out_path)

    def start(self):
        # retrieving the list of all files
        files = self.get_files()
        # filtering the files which have been marked as "done"
        files = list(filter(lambda f: not f.endswith('.done'), files))

        self.print_info(f"Total {len(files)} files detected")
        for file in files:
            if self.needed_entities_scanned:
                break
            self.print_info(f"Reading file {file}")
            file_path = f"{self.path}/{file}"
            file_handler = open(file_path, 'r')
            hostnames = file_handler.readlines()

            for hostname in hostnames:
                if self.entities_scanned >= self.num:
                    self.needed_entities_scanned = True
                    break
                self.scan_hostname(hostname, file)

            file_handler.close()
            os.rename(file_path, f'{file_path}.done')

    def get_files(self):
        if not os.path.isdir(self.path):
            raise ValueError('Provided path is not a valid directory')

        return [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]

    def scan_hostname(self, hostname, file):
        hostname = hostname.strip()
        out_file_name = get_out_file_name(hostname, file)
        if os.path.isfile(out_file_name):
            # this hostname has already been scanned
            return

        self.print_info(f"Checking hostname: {hostname}")
        results = self.client.check_host(hostname)
        self.write_data_to_file(hostname, out_file_name, results)


    def write_data_to_file(self, hostname, file_name,  data):
        negatives = data['malicious'] + data['suspicious']
        message = 'Not Suspicious'
        if negatives > 0:
            message = f'{negatives} services reported the host as malicious / suspicious'
        self.print_info(message)
        data_to_save = {hostname: message}
        json_data = json.dumps(data_to_save, sort_keys=True, indent=4)
        json_file_handler = open(file_name, "w+")
        json_file_handler.write(json_data)
        json_file_handler.close()
        self.entities_scanned += 1


    def print_info(self, message):
        if not self.print:
            return
        info(message)

