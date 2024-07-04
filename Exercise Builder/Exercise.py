
import helpers


class Exercise:
    
    def __init__(self, variant, equipment, exercise, generate):
        
        self.variant = variant
        self.equipment = equipment
        self.exercise = exercise
        self.generate = generate
        self.formattedExercise = f'{self.equipment} {self.variant} {self.exercise}'

        self.formatExercise()

    def formatExercise(self):
            
        if helpers.all([self.variant, self.equipment, self.exercise]):

            if self.equipment == "None" and self.variant == "Standard":
                self.formattedExercise = f'{self.exercise}'
                
            elif self.equipment == "None":
                self.formattedExercise = f'{self.variant} {self.exercise}'
                
            elif self.variant == "Standard":
                self.formattedExercise = f'{self.equipment} {self.exercise}'
                
            else:
                self.formattedExercise = f'{self.formattedExercise}'

