from clients.models import Address
from typing import List

class AddressDAO:  
    def __init__(self):
        self.addressRepo = Address.objects
        super().__init__()
    
######################################[CREATE]##########################################
    def addAddress(self,newAddress: Address):
        if newAddress is None:
            return False
        if not newAddress.isCorrect():
            return False
        newAddress.save()
        return True
    
    def addListOfAddress(self, listOfNewAddresses: List[Address]):
        for newAddress in listOfNewAddresses:
            if newAddress is None:
                return False
            if not newAddress.isCorrect():
                return False
       
        [newAddress.save() for newAddress in listOfNewAddresses]
        return True
    
######################################[RETRIEVE]##########################################
    def findAddress(self,targetAddressID: int):
        if int(targetAddressID) < 1:
            return None
        if not list(self.addressRepo.all()):
            return None
        if self.addressRepo.get(targetAddressID) is None:
            return None
        return self.addressRepo.get(targetAddressID)
    
    def findAddressByZipcode(self, addressZipcode: str):
        if len(addressZipcode) != 5:
            return None
        if not self.addressRepo.all():
            return list()
        if not self.addressRepo.filter(zipcode = addressZipcode):
            return list()
        return self.addressRepo.filter(zipcode = addressZipcode)      
    
######################################[UPDATE]##########################################
    def updateAddress(self,targetAddress):
        if targetAddress.id < 1:
            return False
        if not self.addressRepo.get(id = targetAddress.id):
            return False
        if not targetAddress.isCorrect():
            return False
        targetAddress.save()
        return True

######################################[DELETE]##########################################

    def deleteAddress(self,targetID):
        targetAddress = self.addressRepo.get(id = targetID)
        if not targetAddress:
            return False
        targetAddress.delete()
        return True
