
import helpers


class Exercise:
    
    def __init__(self, variant, equipment, exercise, generate):
        """
        Exercise object initialization of variables and formatted exercise string 
        
        Parameters: self
            variant String: Variant of the exercise 
            equipment String: Equipment to use 
            exercise String: Main text for the exercise
            generate Bool: True when exercise should be generated in Coda
        
        Returns: None
        """
        
        self.variant = variant
        self.equipment = equipment
        self.exercise = exercise
        self.generate = generate
        self.formattedExercise = f'{self.equipment} {self.variant} {self.exercise}'

        self.formatExercise()

    def formatExercise(self):
        """
        Sets formattedExercise to the correct text formatting based on the exercise configuration
        
        Parameters: self
        
        Returns: None
        """
                
        if helpers.all([self.variant, self.equipment, self.exercise]):

            if self.equipment == "None" and self.variant == "Standard":
                self.formattedExercise = f'{self.exercise}'
                
            elif self.equipment == "None":
                self.formattedExercise = f'{self.variant} {self.exercise}'
                
            elif self.variant == "Standard":
                self.formattedExercise = f'{self.equipment} {self.exercise}'
                
            else:
                self.formattedExercise = f'{self.formattedExercise}'

