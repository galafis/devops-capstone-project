"""
Account Service

Paths:
------
GET /accounts - Returns a list all of the Accounts
GET /accounts/{id} - Returns the Account with a given id number
POST /accounts - creates a new Account record in the database
PUT /accounts/{id} - updates an Account record in the database
DELETE /accounts/{id} - deletes an Account record in the database
"""

from flask import Flask, jsonify, request, url_for, make_response, abort
from service.common import status  # HTTP Status Codes

# Create the Flask app
app = Flask(__name__)

# Global in-memory store for accounts and a counter for IDs
# This is a temporary placeholder for a real database and Account model
# as per the lab's progression (DB and models are usually introduced later).
# The tests in test_routes.py imply that POST /accounts is used to create data for GET tests.
IN_MEMORY_ACCOUNTS = {}
ACCOUNT_ID_COUNTER = 1

######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return (
        jsonify(
            name="Account REST API Service",
            version="1.0",
        ),
        status.HTTP_200_OK,
    )

######################################################################
# CREATE A NEW ACCOUNT (POST /accounts)
######################################################################
@app.route("/accounts", methods=["POST"])
def create_accounts():
    """Creates a new Account.
    This endpoint will be called by test cases to create data for other tests (e.g., GET /accounts/{id}).
    It simulates account creation and storage in memory.
    """
    global ACCOUNT_ID_COUNTER
    account_data = request.get_json()
    
    # Basic validation (can be expanded)
    if not account_data or not isinstance(account_data, dict):
        abort(status.HTTP_400_BAD_REQUEST, "Invalid account data provided")

    # Simulate creating an account with an ID
    new_account = account_data.copy() # shallow copy
    new_account["id"] = ACCOUNT_ID_COUNTER
    IN_MEMORY_ACCOUNTS[ACCOUNT_ID_COUNTER] = new_account
    ACCOUNT_ID_COUNTER += 1
    
    app.logger.info(f"Account with ID [{new_account['id']}] created.")
    location_url = url_for("get_accounts", account_id=new_account["id"], _external=True)
    return make_response(
        jsonify(new_account),
        status.HTTP_201_CREATED,
        {"Location": location_url}
    )

######################################################################
# READ AN ACCOUNT (GET /accounts/{id})
######################################################################
@app.route("/accounts/<int:account_id>", methods=["GET"])
def get_accounts(account_id):
    """Reads an Account by its ID.
    Retrieves an account from the in-memory store.
    """
    app.logger.info(f"Request to retrieve account with id: {account_id}")
    account = IN_MEMORY_ACCOUNTS.get(account_id)
    if not account:
        abort(status.HTTP_404_NOT_FOUND, f"Account with id '{account_id}' was not found.")
    
    app.logger.info(f"Returning account with id: {account_id}")
    return make_response(jsonify(account), status.HTTP_200_OK)


# ######################################################################
# #  U T I L I T Y   F U N C T I O N S
# ######################################################################

def init_db():
    """ Initializes the SQLAlchemy app """
    # For now, we clear the in-memory store if this were to be used for reset
    global IN_MEMORY_ACCOUNTS, ACCOUNT_ID_COUNTER
    IN_MEMORY_ACCOUNTS = {}
    ACCOUNT_ID_COUNTER = 1
    app.logger.info("In-memory database initialized.")

# Import the routes After the Flask app is created
# pylint: disable=wrong-import-position, cyclic-import
# from service import routes # noqa: F401 E402 # This was causing a circular import if routes.py imports itself.
# Models would typically be imported here if they existed
# from service import models # noqa: F401 E402

