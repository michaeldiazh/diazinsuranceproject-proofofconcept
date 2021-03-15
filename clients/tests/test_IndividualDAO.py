from clients.models import Address, Individual
from clients.DAO.IndividualDAO import IndividualDAO 
from django.test import TestCase
from django.db.models.query import QuerySet
import unittest.mock

class IndividualDAOTest(TestCase):
    def setUp(self):
        self.dao = IndividualDAO()
        self.individualRepo = Individual.objects


        self.mockAddress1 = unittest.mock.Mock(id = 1)
        self.mockAddress2 = unittest.mock.Mock(id = 2)
        self.mockAddress3 = unittest.mock.Mock(id = 3)
        self.mockAddress4 = unittest.mock.Mock(id = 4)    

        self.mockIndividual1 = unittest.mock.Mock(spec=Individual,licenseNumber = '1111111111111111', firstName = 'f1', lastName = 'l1', email = 'test1@test.com', phoneNumber = '0000000000')
        self.mockIndividual2 = unittest.mock.Mock(spec=Individual,licenseNumber = '2222222222222222', firstName = 'f2', lastName = 'l2', email = 'test2@test.com', phoneNumber = '1111111111')
        self.mockIndividual3 = unittest.mock.Mock(spec=Individual,licenseNumber = '3333333333333333', firstName = 'f3', lastName = 'l3', email = 'test3@test.com', phoneNumber = '2222222222')
        self.mockIndividual4 = unittest.mock.Mock(spec=Individual,licenseNumber = '4', firstName = 'f4', lastName = 'l4', email = 'test4@test.com', phoneNumber = '3333333333')

        return super().setUp()
    
    def tearDown(self):
        return None

    @unittest.mock.patch('clients.models.Individual.save')
    def test_1_1_addIndividual_Method_When_Individual_Is_Null(self,mock_save):
        actualValue = self.dao.addIndividual(None)
        self.assertFalse(actualValue)

    @unittest.mock.patch('clients.models.Individual')
    @unittest.mock.patch('clients.models.Individual.save')
    def test_1_2_addIndividual_Method_When_Individual_Address_Is_Null(self,mock_save,mock_Individual):
        mock_Individual.address = None
        actualValue = self.dao.addIndividual(mock_Individual)
        self.assertTrue(mock_save.return_value.call_count == 0)
        self.assertFalse(actualValue)

    @unittest.mock.patch('clients.models.Individual.objects.get')
    @unittest.mock.patch('clients.models.Individual.save')
    def test_1_3_addIndividual_Method_When_Individual_Is_Correctly_Added(self,mock_save,mock_get):
        mock_get.return_value = None
        self.mockIndividual1.address = self.mockAddress1
        self.mockIndividual1.return_value.save =  mock_save
        self.dao.individualRepo.get = mock_get
        actualValue = self.dao.addIndividual(self.mockIndividual1)
        self.assertTrue(self.mockIndividual1.save.call_count==1)
        self.assertTrue(actualValue)


    @unittest.mock.patch('clients.models.Individual.save')
    def test_1_4_addIndividual_Method_When_Individual_License_Number_(self,mock_save):
        self.mockIndividual1.address = self.mockAddress1
        self.mockIndividual1.licenseNumber = '1'
        self.mockIndividual1.return_value.save =  mock_save
        actualValue = self.dao.addIndividual(self.mockIndividual1)
        self.assertTrue(self.mockIndividual1.save.call_count == 0)
        self.assertFalse(actualValue) 

    @unittest.mock.patch('clients.models.Individual.objects.get')
    @unittest.mock.patch('clients.models.Individual.save')
    def test_1_5_addIndividual_Method_When_Individual_Is_Already_Exist_In_DB(self,mock_save,mock_get):
        mock_get.return_value = self.mockIndividual1
        self.mockIndividual1.address = self.mockAddress1
        self.mockIndividual1.return_value.save =  mock_save
        self.dao.individualRepo.get = mock_get
        actualValue = self.dao.addIndividual(self.mockIndividual1)
        self.assertTrue(self.mockIndividual1.save.call_count==0)
        self.assertFalse(actualValue)

    @unittest.mock.patch('clients.models.Individual.objects.get')
    @unittest.mock.patch('clients.models.Individual.save')
    def test_1_6_addListOfIndividuals_Where_All_Individuals_Are_Added_With_No_Errors(self,mock_save,mock_get):
        mock_get.return_value= None
        listOfMockIndividuals = [self.mockIndividual1, self.mockIndividual2, self.mockIndividual3]
        self.mockIndividual1.address = self.mockAddress1
        self.mockIndividual2.address = self.mockAddress2
        self.mockIndividual3.address = self.mockAddress3
        for individuals in listOfMockIndividuals:
            individuals.return_value.save = mock_save
            individuals.return_value.get = mock_get
        
        actualValue = self.dao.addListOfIndividuals(listOfMockIndividuals)
        for ind in listOfMockIndividuals:
            self.assertTrue(ind.save.call_count == 1)
        self.assertTrue(actualValue) 


    @unittest.mock.patch('clients.models.Individual.objects.get')
    @unittest.mock.patch('clients.models.Individual.save')
    def test_1_7_addListOfIndividuals_Where_One_Individual_Is_None(self,mock_save,mock_get):
        mock_get.return_value= None
        self.mockIndividual2 = None
        listOfMockIndividuals = [self.mockIndividual1, self.mockIndividual2, self.mockIndividual3]
        self.mockIndividual1.address = self.mockAddress1
        self.mockIndividual3.address = self.mockAddress3
        listOfRealIndividuals = [self.mockIndividual1, self.mockIndividual3]
        for individuals in listOfRealIndividuals:
            individuals.return_value.save = mock_save
            individuals.return_value.get = mock_get
        
        actualValue = self.dao.addListOfIndividuals(listOfMockIndividuals)
        for ind in listOfRealIndividuals:
            self.assertTrue(ind.save.call_count == 0)
        self.assertFalse(actualValue) 

    @unittest.mock.patch('clients.models.Individual.objects.get')
    @unittest.mock.patch('clients.models.Individual.save')
    def test_1_8_addListOfIndividuals_Where_One_Individuals_Address_Is_None(self,mock_save,mock_get):
        mock_get.return_value= None
        listOfMockIndividuals = [self.mockIndividual1, self.mockIndividual2, self.mockIndividual3]
        self.mockIndividual1.address = self.mockAddress1
        self.mockIndividual2.address = self.mockAddress2
        self.mockIndividual3.address = None
        for individuals in listOfMockIndividuals:
            individuals.return_value.save = mock_save
            individuals.return_value.get = mock_get
        
        actualValue = self.dao.addListOfIndividuals(listOfMockIndividuals)
        for ind in listOfMockIndividuals:
            self.assertTrue(ind.save.call_count == 0)
        self.assertFalse(actualValue) 

    @unittest.mock.patch('clients.models.Individual.objects.get')
    @unittest.mock.patch('clients.models.Individual.save')
    def test_1_9_addListOfIndividuals_Where_One_Individual_Already_Exist_In_The_Database(self,mock_save,mock_get):
        mock_get.return_value= None
        listOfMockIndividuals = [self.mockIndividual1, self.mockIndividual2, self.mockIndividual3]
        listOfRealIndividuals = [self.mockIndividual1, self.mockIndividual3]
        self.mockIndividual1.address = self.mockAddress1
        self.mockIndividual2.address = self.mockAddress2
        self.mockIndividual3.address = None
        for individuals in listOfRealIndividuals:
            individuals.return_value.save = mock_save
            individuals.return_value.get = mock_get
        mock_get.return_value= self.mockIndividual2
        self.mockIndividual2.return_value.get = mock_get
        actualValue = self.dao.addListOfIndividuals(listOfMockIndividuals)
        for ind in listOfMockIndividuals:
            self.assertTrue(ind.save.call_count == 0)
        self.assertFalse(actualValue) 

    @unittest.mock.patch('clients.models.Individual.objects.get')
    @unittest.mock.patch('clients.models.Individual.save')
    def test_1_10_addListOfIndividuals_Where_One_Individual_Has_An_Incorrect_LicenseNumber(self,mock_save,mock_get):
        mock_get.return_value= None
        listOfMockIndividuals = [self.mockIndividual1, self.mockIndividual2, self.mockIndividual3]
        self.mockIndividual2.licenseNumber = '1'
        self.mockIndividual1.address = self.mockAddress1
        self.mockIndividual2.address = self.mockAddress2
        self.mockIndividual3.address = self.mockAddress3
        for individuals in listOfMockIndividuals:
            individuals.return_value.save = mock_save
            individuals.return_value.get = mock_get
        
        actualValue = self.dao.addListOfIndividuals(listOfMockIndividuals)
        for ind in listOfMockIndividuals:
            self.assertTrue(ind.save.call_count == 0)
        self.assertFalse(actualValue) 
