from clients.models import Address,Individual
from typing import List

class IndividualDAO:  
    def __init__(self):
        self.addressRepo = Address.objects
        self.individualRepo = Individual.objects
        super().__init__()

#########################[CREATE]#######################
    def addIndividual(self, newIndividual):
       #Check
        if not newIndividual:
            return False
        if not self.checkLicenseNumber(newIndividual.licenseNumber):
            return False
        if self.individualRepo.get(licenseNumber = newIndividual.licenseNumber) is not None:
            return False
        if newIndividual.address is None:
            return False
        else:   
            newIndividual.save()
            return True

    def addListOfIndividuals(self, listOfIndividuals):
        # Check all before adding to DB
        for individual in listOfIndividuals:
            if not individual:
                return False
            if self.individualRepo.get(licenseNumber = individual.licenseNumber) is not None:
                return False
            if not self.checkLicenseNumber(individual.licenseNumber):
                return False
            if individual.address is None:
                return False
        
        # Add all the individuals from the list
        for individual in listOfIndividuals:
            individual.save()
        return True
            
    def checkingIndividual(self,individual):
        if not individual:
            return False
        if not self.checkLicenseNumber(individual.licenseNumber):
            return False
        if self.individualRepo.get(licenseNumber = individual.licenseNumber) is not None:
            return False
        if individual.address is None:
            return False
        return True

    def checkLicenseNumber(self,stringNumber):
        import re
        check = re.search('/^[0-9]$/',str(stringNumber))
        return check is None and len(stringNumber) == 16

#########################[RETRIVE]#######################
    
    def findIndividual(self,targetLicenseNumber):
        if not self.checkLicenseNumber(targetLicenseNumber):
            return None
        if not self.individualRepo.get(licenseNumber = targetLicenseNumber):
            return None
        return self.individualRepo.get(licenseNumber = targetLicenseNumber)

    
        
