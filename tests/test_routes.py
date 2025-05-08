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
from service.routes import init_db # Import init_db directly
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
        # Initialize the in-memory store for each test to ensure isolation
        init_db()

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
        for i in range(count):
            test_account_data = {
                "name": f"Test User {i}", 
                "email": f"test{i}@example.com", 
                "address": f"{i} Main St",
                "phone_number": f"123-456-78{i:02d}",
                "date_joined": "2023-01-15T10:00:00Z" # Example date
            } 
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
        created_account = self._create_accounts(1)[0]
        account_id = created_account["id"]

        # Retrieve the account
        response = self.client.get(f"{BASE_URL}/{account_id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        retrieved_account_data = response.get_json()
        self.assertEqual(retrieved_account_data["name"], created_account["name"])
        self.assertEqual(retrieved_account_data["email"], created_account["email"])

    def test_get_account_not_found(self):
        """It should not Read an Account that is not found"""
        response = self.client.get(f"{BASE_URL}/0") # Assuming 0 is an unlikely ID for a created account
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_account(self):
        """It should Update an existing Account"""
        # Create an account to update
        created_account = self._create_accounts(1)[0]
        account_id = created_account["id"]

        # Define new data for the account
        updated_data = {
            "name": "Updated Test User", 
            "email": "updated_test@example.com", 
            "address": "456 New St",
            "phone_number": "987-654-3210",
            "date_joined": created_account["date_joined"] # Keep original join date or update if needed
        }

        # Send PUT request to update the account
        response = self.client.put(f"{BASE_URL}/{account_id}", json=updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returned_account_data = response.get_json()

        # Verify the returned data matches the updated data
        self.assertEqual(returned_account_data["name"], updated_data["name"])
        self.assertEqual(returned_account_data["email"], updated_data["email"])
        self.assertEqual(returned_account_data["address"], updated_data["address"])
        self.assertEqual(returned_account_data["phone_number"], updated_data["phone_number"])

        # Optionally, verify by GETting the account again
        get_response = self.client.get(f"{BASE_URL}/{account_id}")
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        fetched_account_data = get_response.get_json()
        self.assertEqual(fetched_account_data["name"], updated_data["name"])
        self.assertEqual(fetched_account_data["email"], updated_data["email"])

    def test_update_account_not_found(self):
        """It should not Update an Account that is not found"""
        updated_data = {"name": "Non Existent User", "email": "nonexistent@example.com"}
        response = self.client.put(f"{BASE_URL}/0", json=updated_data) # Assuming 0 is an unlikely ID
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # More tests will go here for Create (if not fully covered by helper), Delete, List

