
import os
import requests
import json
import Exercise
import helpers

def getExercises():
    """
    Get the exercise data and return it as a list of Exercise objects 
    
    Parameters: None
    
    Returns:
        [Exercise]: List of Exercise objects from a Coda document 
    """

    authToken = os.getenv('authToken')

    if not authToken:
        raise ValueError("Missing environment variable: authToken")
    
    try:
        config = helpers.loadConfig()

        basePath = config['basePath']

        docId = config['docId']
        exerciseTableId = config['exerciseTableId']
        exerciseColId = config['exerciseColId']
        variantColId = config['variantColId']
        equipmentColId = config['equipmentColId']
        generateFlagColId = config['generateFlagColId']
        
        headers = {'Authorization': f'Bearer {authToken}'}
        uri = f'{basePath}/docs/{docId}/tables/{exerciseTableId}/rows'
        res = requests.get(uri, headers=headers).json()
        
        returnedItems = res["items"]
        variantExercises = []
        
        for variant in returnedItems:
            
            variantRow = variant["values"]
            
            exercise = variantRow[exerciseColId]
            variant = variantRow[variantColId]
            equipmentString = variantRow[equipmentColId]
            generateFlag = variantRow[generateFlagColId]

            equipmentList = []

            if equipmentString != "":
                equipmentList = equipmentString.split(",")

            for equipment in equipmentList:
                variantExercises.append(Exercise.Exercise(variant, equipment, exercise, generateFlag))

    except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
        print(f"Error loading configuration during getExercises: {e}")
        exit(1)

    return variantExercises


def addExercises(exerciseList):
    """
    Add a list of Exercise objects to a Coda document 
    
    Parameters:
        exerciseList [String]: The List of Exercises to add
    
    Returns: None
    """

    authToken = os.getenv('authToken')

    if not authToken:
        raise ValueError("Missing environment variable: authToken")

    try:
        config = helpers.loadConfig()

        basePath = "https://coda.io/apis/v1"
        docId = config['docId']
        generatedTableId = config['generatedTableId']
        columnId = config['columnId']

        headers = {'Authorization': f'Bearer {authToken}'}
        uri = f'{basePath}/docs/{docId}/tables/{generatedTableId}/rows'

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

    except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
        print(f"Error loading configuration during addExercises: {e}")
        exit(1)

