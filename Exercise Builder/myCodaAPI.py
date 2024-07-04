
import requests
import Exercise

def getExercises():

    basePath = "https://coda.io/apis/v1"
    docId = "WTYDkTjAxz"
    tableId = "grid-nzuBA0Hsjq"
    
    headers = {'Authorization': 'Bearer c55ea82b-dea9-4acb-ae8b-0bad1df597a8'}
    uri = f'{basePath}/docs/{docId}/tables/{tableId}/rows'
    res = requests.get(uri, headers=headers).json()
    
    returnedItems = res["items"]
    variantExercises = []
    
    for variant in returnedItems:
        
        variantRow = variant["values"]
        
        exercise = variantRow["c-3J7Hiu8-9P"]
        variant = variantRow["c-xpDnxIH6PO"]
        equipmentString = variantRow["c-nwBMUW7iEr"]
        generateFlag = variantRow["c-DEofO8t4TF"]

        equipmentList = []

        if equipmentString != "":
            equipmentList = equipmentString.split(",")

        for equipment in equipmentList:
            variantExercises.append(Exercise.Exercise(variant, equipment, exercise, generateFlag))


    return variantExercises


def addExercises(exerciseList):

    basePath = "https://coda.io/apis/v1"
    docId = "WTYDkTjAxz"
    tableId = "grid-FYfHw3xFHW"

    headers = {'Authorization': 'Bearer c55ea82b-dea9-4acb-ae8b-0bad1df597a8'}
    uri = f'{basePath}/docs/{docId}/tables/{tableId}/rows'

    rows = []
    
    for e in exerciseList:
        rows.append({'cells': [
            {'column': 'c-zQTA3wRwKC', 'value': e.formattedExercise}
        ]})
    
    payload = {
        'rows': rows
    }
    
    req = requests.post(uri, headers=headers, json=payload)
    req.raise_for_status() # Throw if there was an error.
    res = req.json()
