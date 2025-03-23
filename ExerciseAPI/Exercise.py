
import os
import json
import requests


class Exercise:
    
    def __init__(self, exercise, variants):
        
        self.exercise = exercise
        self.variants = variants
        

    def toDictionary(self):

        return {
            "exercise_base_name" : self.exercise,
            "variants" : [v.toDictionary() for v in self.variants]
        }


class Variant:

    def __init__(self, exercise, variant_name, equipmentString):

        self.exercise = exercise
        self.variant_name = variant_name
        self.equipmentString = equipmentString


    def toDictionary(self):

        return {
            "variant_name" : self.variant_name,
            "equipment" : self.equipmentString
        }

