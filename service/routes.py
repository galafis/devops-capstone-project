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
# LIST ALL ACCOUNTS (GET /accounts)
######################################################################
@app.route("/accounts", methods=["GET"])
def list_accounts():
    """Returns all of the Accounts"""
    app.logger.info("Request to list all accounts")
    
    # Get all accounts from the in-memory store
    accounts_list = list(IN_MEMORY_ACCOUNTS.values())
    
    app.logger.info(f"Returning {len(accounts_list)} accounts")
    return make_response(jsonify(accounts_list), status.HTTP_200_OK)

######################################################################
# CREATE A NEW ACCOUNT (POST /accounts)
######################################################################
@app.route("/accounts", methods=["POST"])
def create_accounts():
    """Creates a new Account."""
    global ACCOUNT_ID_COUNTER
    account_data = request.get_json()
    if not account_data or not isinstance(account_data, dict):
        abort(status.HTTP_400_BAD_REQUEST, "Invalid account data provided")

    new_account = account_data.copy()
    new_account["id"] = ACCOUNT_ID_COUNTER
    IN_MEMORY_ACCOUNTS[ACCOUNT_ID_COUNTER] = new_account
    ACCOUNT_ID_COUNTER += 1
    
    app.logger.info(f"Account with ID [{new_account['id']}] created.")
    location_url = url_for("get_account_by_id", account_id=new_account['id'], _external=True)
    return make_response(
        jsonify(new_account),
        status.HTTP_201_CREATED,
        {"Location": location_url}
    )

######################################################################
# READ AN ACCOUNT (GET /accounts/{id})
######################################################################
@app.route("/accounts/<int:account_id>", methods=["GET"])
def get_account_by_id(account_id):
    """Reads an Account by its ID."""
    app.logger.info(f"Request to retrieve account with id: {account_id}")
    account = IN_MEMORY_ACCOUNTS.get(account_id)
    if not account:
        abort(status.HTTP_404_NOT_FOUND, f"Account with id '{account_id}' was not found.")
    
    app.logger.info(f"Returning account with id: {account_id}")
    return make_response(jsonify(account), status.HTTP_200_OK)

######################################################################
# UPDATE AN EXISTING ACCOUNT (PUT /accounts/{id})
######################################################################
@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_accounts(account_id):
    """Updates an Account by its ID."""
    app.logger.info(f"Request to update account with id: {account_id}")
    account = IN_MEMORY_ACCOUNTS.get(account_id)
    if not account:
        abort(status.HTTP_404_NOT_FOUND, f"Account with id '{account_id}' was not found.")
    
    updated_data = request.get_json()
    if not updated_data or not isinstance(updated_data, dict):
        abort(status.HTTP_400_BAD_REQUEST, "Invalid account data provided for update")

    updated_data["id"] = account_id
    IN_MEMORY_ACCOUNTS[account_id] = updated_data
    
    app.logger.info(f"Account with ID [{updated_data['id']}] updated.")
    return make_response(jsonify(updated_data), status.HTTP_200_OK)

######################################################################
# DELETE AN ACCOUNT (DELETE /accounts/{id})
######################################################################
@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_accounts(account_id):
    """Deletes an Account by its ID."""
    app.logger.info(f"Request to delete account with id: {account_id}")
    if account_id in IN_MEMORY_ACCOUNTS:
        del IN_MEMORY_ACCOUNTS[account_id]
        app.logger.info(f"Account with ID [{account_id}] deleted.")
    return make_response("", status.HTTP_204_NO_CONTENT)


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################
def init_db():
    """ Initializes the in-memory store """
    global IN_MEMORY_ACCOUNTS, ACCOUNT_ID_COUNTER
    IN_MEMORY_ACCOUNTS = {}
    ACCOUNT_ID_COUNTER = 1
    app.logger.info("In-memory database initialized.")

