
import Exercise
from Exercise import Variant

import os
import json
import requests


authToken = os.getenv('authToken')
if not authToken:
    raise ValueError("Missing environment variable: authToken")


def loadConfig(configFile='config.json'):

        if not os.path.exists(configFile):
            raise FileNotFoundError(f"Configuration file '{configFile}' not found.")
        
        with open(configFile, 'r') as file:
            return json.load(file)

        
try:
    config = loadConfig()

    basePath = config['basePath']
    docId = config['docId']
    exerciseTableId = config['exerciseTableId']
    exerciseColId = config['exerciseColId']
    variantColId = config['variantColId']
    equipmentColId = config['equipmentColId']
            
    headers = {'Authorization': f'Bearer {authToken}'}
    uri = f'{basePath}/docs/{docId}/tables/{exerciseTableId}/rows'
    res = requests.get(uri, headers=headers).json()
            
    returnedItems = res["items"]

    baseExercises = []
    variantCount = 0
    totalCombinations = 0
            
    for variant in returnedItems:

        variantCount += 1

        variantRow = variant["values"]
        
        exercise = variantRow[exerciseColId]
        variant = variantRow[variantColId]
        equipmentString = variantRow[equipmentColId]
        equipmentList = equipmentString.split(",")

        addExerciseObject = True
        for i, obj in enumerate(baseExercises):
            if obj.exercise == exercise:
                totalCombinations += len(equipmentList)
                baseExercises[i].variants.append(Exercise.Variant(exercise, variant, equipmentList))
                addExerciseObject = False
                break

        
        print(len(equipmentList))

        if addExerciseObject:
            baseExercises.append(Exercise.Exercise(exercise, [Exercise.Variant(exercise, variant, equipmentList)]))


    exerciseDictonaryList = [e.toDictionary() for e in baseExercises]
    # exerciseJsonString = json.dumps(exerciseDictonaryList)

    buildFile = True

    if buildFile:
        with open("ExerciseData.json", "w") as file:
            json.dump(exerciseDictonaryList, file, indent=4)
    else:
        print(f'Total Exercise Variants {variantCount}')
        print(f'Total Combinations: {totalCombinations}')
        print(json.dumps(exerciseDictonaryList))


except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
    print(f"Error loading configuration during getExercises: {e}")
    exit(1)


