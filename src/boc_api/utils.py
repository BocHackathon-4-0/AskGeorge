import json


def loadJsonFile(filename):
    with open(filename, 'r') as file:
        data = json.load(file)

    return data

def getUserData():
    return loadJsonFile('updated_data.json')

def getPaymentData():
    return loadJsonFile('testData.json')


