from inc.scanner import Scanner
from inc.helpers import argument_or_input, output_error as error, get_option

try:
    path = argument_or_input('Please provide the path to directory where the files are located:', 1)
    num = int(argument_or_input('Please provide a number of entities to be scanned', 2))
    verbose = get_option('verbose', 'V')
    scanner = Scanner(path, num, verbose)
    scanner.start()
except ValueError as e:
    error(e)
