import os
for path in os.environ["PATH"].split(os.pathsep):
    print(path)