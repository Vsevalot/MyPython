from os import makedirs
from os.path import exists

if not exists('C:\\abba'):
    makedirs('C:\\abba')

with open('C:\\abba\\r.txt', 'w') as testfile:
    testfile.write('Hello World')
    testfile.close()
