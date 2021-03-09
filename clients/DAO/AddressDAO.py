from clients.models import Address

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
    
    def addListOfAddress(self, listOfNewAddresses: list):
        for newAddress in listOfNewAddresses:
            if newAddress is None:
                return False
            if not newAddress.isCorrect():
                return False
       
        [newAddress.save() for newAddress in listOfNewAddresses]
        return True
######################################[FIND]##########################################
    def findAddress(self,targetAddressID:int):
        if not list(self.addressRepo.all()):
            return None
        if self.addressRepo.get(targetAddressID) is None:
            return None
        return self.addressRepo.get(targetAddressID)
    