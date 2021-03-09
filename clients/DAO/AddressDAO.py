from clients.models import Address

class AddressDAO:  
    def __init__(self):
        self.addressRepo = Address.objects
        super().__init__()
    

    def addAddress(self,newAddress: Address):
        if newAddress is None:
            return False
        if not newAddress.isCorrect():
            return False
        newAddress.save()
        return True
    
    def addAllListAddress(self, listOfNewAddresses: list):
        for newAddress in listOfNewAddresses:
            if newAddress is None:
                return False
            if not newAddress.isCorrect():
                return False
       
        [newAddress.save() for newAddress in listOfNewAddresses]
        return True

    