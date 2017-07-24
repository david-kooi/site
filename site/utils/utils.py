import os

def GetTextAsList(text_path, filename):
    info = []
    info_path = os.path.join(text_path, filename)
    with open(info_path) as f:
        #info = f.read().splitlines()
        info = f.read()

    return info
