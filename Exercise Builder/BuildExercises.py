
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


exerciseCount = len(fetchedExercises)

print(f'Final Exercise Count: {exerciseCount}')
print(f'Standard : {standardCount}')
print(f'Variant : {variantCount}')

myCodaAPI.addExercises(exercisesToAdd)

addedExerciseCount = len(exercisesToAdd)

print(f'Exercises Added: {addedExerciseCount}')

for addedExercise in exercisesToAdd:
    print(addedExercise.formattedExercise)
