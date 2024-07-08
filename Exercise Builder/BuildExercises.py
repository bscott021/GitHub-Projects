
import myCodaAPI


fetchedExercises = myCodaAPI.getExercises()

standardCount = 0
variantCount = 0
exercisesToAdd = []

for exercise in fetchedExercises:
    # print(exercise.formattedExercise)
    if exercise.variant == "Standard":
        standardCount += 1
    else:
        variantCount += 1
    
    if exercise.generate == True:
        # print(exercise.exercise)
        exercisesToAdd.append(exercise)


myCodaAPI.addExercises(exercisesToAdd)


print(f'Final Exercise Count: {len(fetchedExercises) + len(exercisesToAdd)}')
print(f'Exercises Added: {len(exercisesToAdd)}')
print(f'Standard : {standardCount}')
print(f'Variant : {variantCount}')
print('New Exercises : ')

for addedExercise in exercisesToAdd:
    print(addedExercise.formattedExercise)

