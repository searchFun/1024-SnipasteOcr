import json

def resolveJson(path):
    file = open(path,"rb")
    fileJson = json.load(file)
    return fileJson