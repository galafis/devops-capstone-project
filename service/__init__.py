# -*- coding: utf-8 -*-
"""
Service Package

This package contains the core service code.
"""
# Import the Flask app object to make it accessible from the service package
from .routes import app
from .common import status # Also make status codes easily accessible if needed elsewhere

