import json
import os
from requests.exceptions import HTTPError

from inc.vtclient import VTClient
from inc.helpers import output_info as info, output_error as error, get_out_file_name, mkdir


class Scanner:
    def __init__(self, path, num, verbose=False, client = VTClient()):
        self.path = path
        self.client = client
        self.num = num
        self.out_path = 'out'
        self.entities_scanned = 0
        self.needed_entities_scanned = False
        self.print = verbose
        # create the directory for saving output if does not exist
        mkdir(self.out_path)

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
            hostnames = list(filter(lambda n: not self.hostname_is_scanned(n, file), file_handler.readlines()))

            hostnames_scanned = 0
            for hostname in hostnames:
                if self.entities_scanned >= self.num:
                    self.needed_entities_scanned = True
                    break
                try:
                    self.scan_hostname(hostname, file)
                    hostnames_scanned += 1
                except HTTPError as e:
                    self.print_error(f'Could not fetch information from API: {e}')

            file_handler.close()
            if hostnames_scanned == len(hostnames):
                os.rename(file_path, f'{file_path}.done')

    def hostname_is_scanned(self, hostname, path):
        # if file exists, then it's already scanned
        filename = get_out_file_name(hostname.strip(), path)
        return os.path.isfile(filename)

    def get_files(self):
        if not os.path.isdir(self.path):
            raise ValueError('Provided path is not a valid directory')

        return [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]

    def scan_hostname(self, hostname, file):
        hostname = hostname.strip()
        self.print_info(f"Checking hostname: {hostname}")
        results = self.client.check_host(hostname)
        self.write_data_to_file(hostname, file, results)


    def write_data_to_file(self, hostname, file_name, data):
        out_file_name = get_out_file_name(hostname, file_name)

        negatives = data['malicious'] + data['suspicious']
        message = 'Not Suspicious'
        if negatives > 0:
            message = f'{negatives} services reported the host as malicious / suspicious'
        self.print_info(message)
        data_to_save = {hostname: message}
        json_data = json.dumps(data_to_save, sort_keys=True, indent=4)
        json_file_handler = open(out_file_name, "w+")
        json_file_handler.write(json_data)
        json_file_handler.close()
        self.entities_scanned += 1

    def print_info(self, message):
        if not self.print:
            return
        info(message)

    def print_error(self, message):
        error(message)
