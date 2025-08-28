from extension import db
from datetime import date

class Child:
    def __init__(self, name, dateOfBirth, gender, heightCm=None, weightKg=None):
        self.id = None
        self.name = name
        self.dateOfBirth = dateOfBirth
        self.gender = gender
        self.heightCm = heightCm
        self.weightKg = weightKg

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "dateOfBirth": self.dateOfBirth.isoformat(),
            "gender": self.gender,
            "heightCm": self.heightCm,
            "weightKg": self.weightKg,
        }
