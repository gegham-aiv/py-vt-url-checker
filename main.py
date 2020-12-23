from inc.vtclient import VTClient
import os
import sys

if len(sys.argv) < 2:
    print('Please provide the path to directory where the files are located:')
    path = input()
else:
    path = sys.argv[1]

if not os.path.isdir(path):
    print('Invalid path provided. Exiting')
    exit()

files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

for file in files:
    print(file)

# #
# # client = VTClient()
# #
# #
# #
# # client.check('https://www.facebook.com')
# #
# #
# # #
# # #
# # # print()
# # #
# # # print('hello world')
