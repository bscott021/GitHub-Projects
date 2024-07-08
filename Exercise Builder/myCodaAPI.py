
import requests
import Exercise

def getExercises():
    """
    Get the exercise data and return it as a list of Exercise objects 
    
    Parameters: None
    
    Returns:
        [Exercise]: List of Exercise objects from a Coda document 
    """

    authToken = "<replace>"
    basePath = "https://coda.io/apis/v1"

    docId = "<replace>"
    tableId = "<replace>"
    exerciseRowId = "<replace>"
    variantRowId = "<replace>"
    equipmentRowId = "<replace>"
    generateFlagId = "<replace>"
    
    headers = {'Authorization': f'Bearer {authToken}'}
    uri = f'{basePath}/docs/{docId}/tables/{tableId}/rows'
    res = requests.get(uri, headers=headers).json()
    
    returnedItems = res["items"]
    variantExercises = []
    
    for variant in returnedItems:
        
        variantRow = variant["values"]
        
        exercise = variantRow[exerciseRowId]
        variant = variantRow[variantRowId]
        equipmentString = variantRow[equipmentRowId]
        generateFlag = variantRow[generateFlagId]

        equipmentList = []

        if equipmentString != "":
            equipmentList = equipmentString.split(",")

        for equipment in equipmentList:
            variantExercises.append(Exercise.Exercise(variant, equipment, exercise, generateFlag))


    return variantExercises


def addExercises(exerciseList):
    """
    Add a list of Exercise objects to a Coda document 
    
    Parameters:
        exerciseList [String]: The List of Exercises to add
    
    Returns: None
    """

    authToken = "<replace>"

    basePath = "https://coda.io/apis/v1"
    docId = "<replace>"
    tableId = "<replace>"
    columnId = "<replace>"

    headers = {'Authorization': f'Bearer {authToken}'}
    uri = f'{basePath}/docs/{docId}/tables/{tableId}/rows'

    rows = []
    
    for e in exerciseList:
        rows.append({'cells': [
            {'column': columnId, 'value': e.formattedExercise}
        ]})
    
    payload = {
        'rows': rows
    }
    
    req = requests.post(uri, headers=headers, json=payload)
    req.raise_for_status() # Throw if there was an error.
    res = req.json()

