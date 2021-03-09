from clients.models import Address
from clients.DAO.AddressDAO import AddressDAO 
from django.test import TestCase
import unittest.mock

@unittest.mock.patch('clients.models.Address.isCorrect')
@unittest.mock.patch('clients.models.Address.save')
class AddressDAOTest(TestCase):

    def setUp(self):
        self.dao = AddressDAO()
        self.addressRepo = Address.objects
        
        self.mockAddress1 = unittest.mock.Mock(spec=Address, 
                                              zipcode = '07003',
                                              city = 'Bloomfield',
                                              state = 'NJ')
        
        self.mockAddress2 = unittest.mock.Mock(spec=Address, 
                                              zipcode = '07307',
                                              city = 'Jersey City',
                                              state = 'NJ')
        
        self.mockAddress3 = unittest.mock.Mock(spec=Address, 
                                              zipcode = '11201',
                                              city = 'New York',
                                              state = 'NY')
        
        self.mockAddress4= unittest.mock.Mock(spec=Address, 
                                              zipcode = '78613',
                                              city = 'Los Angeles',
                                              state = 'NJ')    
        
        return super().setUp()


    def tearDown(self):
        self.addressRepo.all().delete()
        return super().tearDown()

    def test_addAddress_Method_When_Address_It_Is_Null(self,mockFunction,mockSave):
        self.assertFalse(self.dao.addAddress(None))

    def test_addAddress_Method_When_Address_It_Is_Not_Null(self,mockFunction,mockSave):
        self.mockAddress4.isCorrect = mockFunction
        self.mockAddress4.save = mockSave
        mockFunction.return_value = True
        self.assertTrue(self.dao.addAddress(self.mockAddress1))   
    
    def test_addAddress_Method_When_Address_It_Is_Not_Null_But_Zipcode_is_Wrong(self,mockFunction,mockSave):
        self.mockAddress4.isCorrect = mockFunction
        self.mockAddress4.save = mockSave
        mockFunction.return_value = False
        actualValue = self.dao.addAddress(self.mockAddress4)
        self.assertFalse(actualValue)
    