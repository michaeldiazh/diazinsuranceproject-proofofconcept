from clients.models import Address
from clients.DAO.AddressDAO import AddressDAO 
from django.test import TestCase
from django.db.models.query import QuerySet
import unittest.mock

def getFunction(listOfAddress,id):
    if(len(listOfAddress) < id):
        return None
    for address in listOfAddress:
        if address.id == id:
            return address
    return None

def filterByZipcodeFunction(listOfAddress,zipcode):
    listOfFilteredFunctions = list()
    for address in listOfAddress:
        if address.zipcode is zipcode:
            listOfFilteredFunctions.append(address)
    return listOfFilteredFunctions

class AddressDAOTest(TestCase):

    def setUp(self):
        self.dao = AddressDAO()
        self.addressRepo = Address.objects
        
        self.mockAddress1 = unittest.mock.Mock(spec=Address,id=1, zipcode = '07003', city = 'Bloomfield', state = 'NJ')
        self.mockAddress2 = unittest.mock.Mock(spec=Address,id=2, zipcode = '07307', city = 'Jersey City', state = 'NJ')
        self.mockAddress3 = unittest.mock.Mock(spec=Address,id=3, zipcode = '11201', city = 'New York', state = 'NY')
        self.mockAddress4 = unittest.mock.Mock(spec=Address, id=4, zipcode = '78613', city = 'Los Angeles', state = 'CA')    
        self.mockAddress5 = unittest.mock.Mock(spec=Address, id=5, zipcode = '07003', city = 'Bloomfield', state = 'NJ')

        return super().setUp()

    def tearDown(self):
        self.addressRepo.all().delete()
        return super().tearDown()

    #############################################################################################################
    ########################################[CREATION TEST FOR DAO]##############################################
    
    @unittest.mock.patch('clients.models.Address.isCorrect')
    @unittest.mock.patch('clients.models.Address.save')
    def test_1_1_addAddress_Method_When_Address_It_Is_Null(self,mock_save,mock_isCorrect):
        self.assertFalse(self.dao.addAddress(None))

    @unittest.mock.patch('clients.models.Address.isCorrect')
    @unittest.mock.patch('clients.models.Address.save') 
    def test_1_2_addAddress_Method_When_Address_It_Is_Not_Null(self,mock_save,mock_isCorrect):
        self.mockAddress4.isCorrect = mock_isCorrect
        self.mockAddress4.save = mock_save
        mock_isCorrect.return_value = True
        actualValue = self.dao.addAddress(self.mockAddress1)
        self.assertTrue(mock_save.has_been_called)
        self.assertTrue(actualValue)   
    
    @unittest.mock.patch('clients.models.Address.isCorrect')
    @unittest.mock.patch('clients.models.Address.save')
    def test_1_3_addAddress_Method_When_Address_It_Is_Not_Null_But_Zipcode_is_Wrong(self,mock_save,mock_isCorrect):
        self.mockAddress4.isCorrect = mock_isCorrect
        self.mockAddress4.save = mock_save
        mock_isCorrect.return_value = False
        actualValue = self.dao.addAddress(self.mockAddress4)
        self.assertFalse(actualValue)
    
    @unittest.mock.patch('clients.models.Address.isCorrect')
    @unittest.mock.patch('clients.models.Address.save')
    def test_1_4_addListOfAddress_With_All_Items_In_List_To_Not_Be_Null_And_Is_Correct(self,mock_save,mock_isCorrect):
        mockList = [self.mockAddress1, self.mockAddress2, self.mockAddress3]
        for mockAddress in mockList:
            mockAddress.isCorrect = mock_isCorrect
            mockAddress.save = mock_save
        mock_isCorrect.return_value = True
        actualValue = self.dao.addListOfAddress(mockList)
        self.assertEqual(mock_isCorrect.call_count, 3)
        self.assertEqual(mock_save.call_count, 3)
        self.assertTrue(actualValue)

    @unittest.mock.patch('clients.models.Address.isCorrect')
    @unittest.mock.patch('clients.models.Address.save')
    def test_1_5_addListOfAddress_With_2_Items_In_List_To_Not_Be_Null_But_One_Is(self,mock_save,mock_isCorrect):
        mockList = [self.mockAddress1, self.mockAddress2, self.mockAddress3]
        for mockAddress in mockList:
            mockAddress.isCorrect = mock_isCorrect
            mockAddress.save = mock_save
        mock_isCorrect.return_value = True
        mockList.append(None)
        actualValue = self.dao.addListOfAddress(mockList)
        self.assertEqual(mock_isCorrect.call_count, 3)
        self.assertFalse(actualValue)

    #############################################################################################################
    ########################################[FIND TEST FOR DAO]##############################################
    
    @unittest.mock.patch('clients.models.Address.objects.all')
    def test_2_1_findAddress_Where_Database_Is_Empty(self, mock_all):
        mock_all.return_value = []
        self.assertIsNone(self.dao.findAddress(4),None)

    @unittest.mock.patch('clients.models.Address.objects.all') 
    @unittest.mock.patch('clients.models.Address.objects.get') 
    def test_2_2_findAddress_Where_Database_Is_Not_Empty_But_Target_Address_Not_In_Table(self, mock_all, mock_get):
        mock_all.return_value = [self.mockAddress1, self.mockAddress2]
        mock_get.return_value = getFunction(mock_all.return_value,3)
        self.dao.addressRepo.all = mock_all
        self.dao.addressRepo.get = mock_get
        self.assertIsNone(self.dao.findAddress(3))
    
    @unittest.mock.patch('clients.models.Address.objects.all') 
    @unittest.mock.patch('clients.models.Address.objects.get') 
    def test_2_3_findAddress_Where_Database_Is_Not_Empty_And_Target_Address_Is_In_Table(self, mock_all, mock_get):
        mock_all.return_value = [self.mockAddress1, self.mockAddress2]
        mock_get.return_value = getFunction(mock_all.return_value,2)
        self.dao.addressRepo.all = mock_all
        self.dao.addressRepo.get = mock_get
        self.assertEqual(self.dao.findAddress(2),self.mockAddress2)

    @unittest.mock.patch('clients.models.Address.objects.all') 
    @unittest.mock.patch('clients.models.Address.objects.get') 
    def test_2_4_findAddress_Where_Database_Is_Not_Empty_And_Target_Address_Is_In_Table(self, mock_all, mock_get):
        mock_all.return_value = [self.mockAddress1, self.mockAddress2]
        mock_get.return_value = getFunction(mock_all.return_value,0)
        self.dao.addressRepo.all = mock_all
        self.dao.addressRepo.get = mock_get
        self.assertEqual(self.dao.findAddress(0),None)

    @unittest.mock.patch('clients.models.Address.objects.all')
    @unittest.mock.patch('clients.models.Address.objects.filter')
    def test_2_5_findAddressByZipcode_Where_Zipcode_Does_Exist(self, mock_all, mock_filter):
        mock_all.return_value = [self.mockAddress1, self.mockAddress2,self.mockAddress3]
        mock_filter.return_value = filterByZipcodeFunction([self.mockAddress1, self.mockAddress2,self.mockAddress3],'07003')
        self.dao.addressRepo.filter = mock_filter
        self.assertTrue(self.mockAddress1 in self.dao.findAddressByZipcode('07003'))
    
    @unittest.mock.patch('clients.models.Address.objects.all')
    @unittest.mock.patch('clients.models.Address.objects.filter')
    def test_2_6_findAddressByZipcode_Where_Zipcode_Is_More_Than_9_Digits(self, mock_all, mock_filter):
        self.assertFalse(self.dao.findAddressByZipcode('070030'))

    @unittest.mock.patch('clients.models.Address.objects.all')
    @unittest.mock.patch('clients.models.Address.objects.filter')
    def test_2_7_findAddressByZipcode_Where_Database_Is_Empty(self, mock_all, mock_filter):
        mock_all.return_value = []
        self.assertFalse(self.dao.findAddressByZipcode('070030'))

    @unittest.mock.patch('clients.models.Address.objects.all')
    @unittest.mock.patch('clients.models.Address.objects.filter')
    def test_2_8_findAddressByZipcode_Where_Output_Is_More_Than_One(self, mock_all, mock_filter):
        mock_all.return_value = [self.mockAddress1, self.mockAddress2, self.mockAddress5]
        mock_filter.return_value = filterByZipcodeFunction([self.mockAddress1, self.mockAddress2, self.mockAddress5],'07003')
        self.dao.addressRepo.all = mock_all
        self.dao.addressRepo.filter = mock_filter
        expectedList = [self.mockAddress1, self.mockAddress5]
        actualList = self.dao.findAddressByZipcode('07003')
        self.assertTrue(len(actualList) == 2)
        [self.assertTrue(address in actualList) for address in expectedList]
    
#############################################################################################################
########################################[UPDATE TEST FOR DAO]##############################################
    
    @unittest.mock.patch('clients.models.Address.objects.get') 
    @unittest.mock.patch('clients.models.Address.isCorrect')
    @unittest.mock.patch('clients.models.Address.save')
    def test_3_1_updateAddress_With_Valid_ID(self, mock_get, mock_isCorrect, mock_save):
        mock_get.return_value = getFunction([self.mockAddress1, self.mockAddress2,self.mockAddress3],1)
        mock_isCorrect.return_value = True
        for address in [self.mockAddress1, self.mockAddress2,self.mockAddress3]:
            address.isCorrect = mock_isCorrect
            address.save = mock_save
        self.dao.addressRepo.get = mock_get
        self.mockAddress1 = unittest.mock.Mock(spec=Address,id=1, zipcode = '07307', city = 'Jersey City', state = 'NJ')
        self.assertTrue(self.dao.updateAddress(self.mockAddress1))

    @unittest.mock.patch('clients.models.Address.objects.get') 
    @unittest.mock.patch('clients.models.Address.isCorrect')
    @unittest.mock.patch('clients.models.Address.save')
    def test_3_2_updateAddress_With_InValid_ID_Of_4(self, mock_get, mock_isCorrect, mock_save):
        mock_get.return_value = getFunction([self.mockAddress1, self.mockAddress2,self.mockAddress3],4)
        mock_isCorrect.return_value = True
        for address in [self.mockAddress1, self.mockAddress2,self.mockAddress3]:
            address.isCorrect = mock_isCorrect
            address.save = mock_save
        self.dao.addressRepo.get = mock_get
        self.mockAddress1 = unittest.mock.Mock(spec=Address,id=1, zipcode = '07307', city = 'Jersey City', state = 'NJ')
        self.assertFalse(self.dao.updateAddress(self.mockAddress1))

    @unittest.mock.patch('clients.models.Address.objects.get') 
    @unittest.mock.patch('clients.models.Address.isCorrect')
    @unittest.mock.patch('clients.models.Address.save')
    def test_3_3_updateAddress_With_isCorrect_Being_False(self, mock_get, mock_isCorrect, mock_save):
        mock_get.return_value = getFunction([self.mockAddress1, self.mockAddress2,self.mockAddress3],4)
        mock_isCorrect.return_value = True
        for address in [self.mockAddress1, self.mockAddress2,self.mockAddress3]:
            address.isCorrect = mock_isCorrect
            address.save = mock_save
        mock_isCorrect.return_value = False
        self.mockAddress1.isCorrect = mock_isCorrect
        self.dao.addressRepo.get = mock_get
        self.mockAddress1 = unittest.mock.Mock(spec=Address,id=1, zipcode = '07307', city = 'Jersey City', state = 'NJ')
        self.assertFalse(self.dao.updateAddress(self.mockAddress1))
    
    @unittest.mock.patch('clients.models.Address.objects.get') 
    @unittest.mock.patch('clients.models.Address.isCorrect')
    @unittest.mock.patch('clients.models.Address.save')
    def test_3_4_updateAddress_With_Empty_Table(self, mock_get, mock_isCorrect, mock_save):
        mock_get.return_value = getFunction([],1)
        mock_isCorrect.return_value = True
        for address in [self.mockAddress1, self.mockAddress2,self.mockAddress3]:
            address.isCorrect = mock_isCorrect
            address.save = mock_save
        self.dao.addressRepo.get = mock_get
        self.mockAddress1 = unittest.mock.Mock(spec=Address,id=6, zipcode = '07307', city = 'Jersey City', state = 'NJ')
        self.assertFalse(self.dao.updateAddress(self.mockAddress1))

#############################################################################################################
########################################[DELETE TEST FOR DAO]##############################################
  
    @unittest.mock.patch('clients.models.Address.objects.get') 
    @unittest.mock.patch('clients.models.Address.isCorrect')
    @unittest.mock.patch('clients.models.Address.save')
    def test_4_1_deleteAddress_From_Empty_Table(self, mock_get, mock_isCorrect, mock_save):
        mock_get.return_value = getFunction([],1)
        for address in [self.mockAddress1, self.mockAddress2,self.mockAddress3]:
            address.isCorrect = mock_isCorrect
            address.save = mock_save
        self.dao.addressRepo.get = mock_get
        self.mockAddress1 = unittest.mock.Mock(spec=Address,id=1, zipcode = '07307', city = 'Jersey City', state = 'NJ')
        self.assertFalse(self.dao.deleteAddress(1))

    @unittest.mock.patch('clients.models.Address.objects.get') 
    @unittest.mock.patch('clients.models.Address.isCorrect')
    @unittest.mock.patch('clients.models.Address.save')
    def test_4_2_deleteAddress_From_Full_Table(self, mock_get, mock_isCorrect, mock_save):
        mock_get.return_value = getFunction([self.mockAddress1],1)
        for address in [self.mockAddress1, self.mockAddress2,self.mockAddress3]:
            address.isCorrect = mock_isCorrect
            address.save = mock_save
        self.dao.addressRepo.get = mock_get
        self.mockAddress1 = unittest.mock.Mock(spec=Address,id=1, zipcode = '07307', city = 'Jersey City', state = 'NJ')
        self.assertTrue(self.dao.deleteAddress(1))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~