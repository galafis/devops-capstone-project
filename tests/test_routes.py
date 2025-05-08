"""
TestAccount API Service Test Suite

Test cases can be run with the following command from the root directory:
  pytest -v --cov=service --cov-report=term-missing
"""
import os
import logging
from unittest import TestCase
# from unittest.mock import MagicMock, patch # If we need to mock later
from service import app
from service.common import status  # HTTP Status Codes
# from service.models import db, Account, init_db # Assuming models will be here

# DATABASE_URI = os.getenv(
#     "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
# )
BASE_URL = "/accounts"

######################################################################
#  T E S T   C A S E S
######################################################################
class TestAccountService(TestCase):
    """Account Service Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI # If using DB
        # app.logger.setLevel(logging.CRITICAL)
        # init_db(app) # If using DB

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        pass

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()
        # db.session.query(Account).delete()  # clean up the last tests
        # db.session.commit()

    def tearDown(self):
        """Runs after each test"""
        # db.session.remove()
        pass

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################

    def _create_accounts(self, count):
        """Factory method to create accounts in bulk"""
        accounts = []
        for _ in range(count):
            # For now, we assume the create endpoint works or we mock account creation
            # This is a placeholder as the actual account structure is not defined yet
            # The lab implies using POST /accounts to create test data.
            test_account_data = {"name": "Test User", "email": f"test{_}@example.com", "address": "123 Main St"} 
            response = self.client.post(BASE_URL, json=test_account_data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED, "Could not create test Account")
            new_account = response.get_json()
            accounts.append(new_account)
        return accounts

    ######################################################################
    #  A C C O U N T   T E S T   C A S E S
    ######################################################################

    def test_index(self):
        """It should call the home page"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], "Account REST API Service")

    def test_get_account(self):
        """It should Read a single Account"""
        # Create an account to read
        # For now, let's assume _create_accounts(1) works by calling POST /accounts
        # We'll need to define what an account looks like and how it's created.
        # The lab states: "The function and route to create an account are already provided in the sample code"
        # So, we should be able to use self.client.post() to create an account.
        
        # Placeholder for account data, adapt when Account model is clear
        sample_account_data = {"name": "John Doe", "email": "john.doe@example.com", "address": "123 Test St", "phone_number": "123-456-7890"}
        
        # Create the account using the POST endpoint
        post_response = self.client.post(BASE_URL, json=sample_account_data)
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        created_account_data = post_response.get_json()
        account_id = created_account_data["id"] # Assuming the POST response includes an 'id'

        # Retrieve the account
        response = self.client.get(f"{BASE_URL}/{account_id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        retrieved_account_data = response.get_json()
        self.assertEqual(retrieved_account_data["name"], sample_account_data["name"])
        self.assertEqual(retrieved_account_data["email"], sample_account_data["email"])
        # Add more assertions as needed for other fields

    def test_get_account_not_found(self):
        """It should not Read an Account that is not found"""
        response = self.client.get(f"{BASE_URL}/0") # Assuming 0 is an unlikely ID
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # More tests will go here for Create, Update, Delete, List

