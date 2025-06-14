#!/usr/bin/env python3
"""
Mocking Option Value API Server

A simple Flask REST API server that returns a list of option values.
Returns: ["option1", "option2", "option3"]
"""

from flask import Flask, jsonify
from flask_cors import CORS
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Mock data - list of option values
OPTION_VALUES = ["option1", "option2", "option3"]

@app.route('/api/options', methods=['GET'])
def get_options():
    """
    GET endpoint that returns the list of option values.
    
    Returns:
        JSON response with the list of options
    """
    logger.info("GET /api/options - Returning option values")
    return jsonify({
        "success": True,
        "data": OPTION_VALUES
    })

@app.route('/api/options', methods=['POST'])
def add_option():
    """
    POST endpoint to add a new option value.
    
    Returns:
        JSON response with updated list of options
    """
    logger.info("POST /api/options - Adding new option value")
    # For this mock server, we'll just return the existing list
    # In a real implementation, you would add the new option to the list
    return jsonify({
        "success": True,
        "message": "Option added successfully (mock)",
        "data": OPTION_VALUES
    })

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    
    Returns:
        JSON response indicating server is healthy
    """
    return jsonify({
        "status": "healthy",
        "service": "mocking_option_value_api",
        "version": "1.0.0"
    })

@app.route('/', methods=['GET'])
def root():
    """
    Root endpoint with API information.
    
    Returns:
        JSON response with API information
    """
    return jsonify({
        "service": "Mocking Option Value API",
        "version": "1.0.0",
        "endpoints": {
            "GET /api/options": "Get list of option values",
            "POST /api/options": "Add new option value (mock)",
            "GET /health": "Health check",
            "GET /": "API information"
        }
    })

if __name__ == '__main__':
    # Run the Flask app
    print("Starting Mocking Option Value API Server...")
    print("Available endpoints:")
    print("  GET  /api/options - Get option values")
    print("  POST /api/options - Add option value (mock)")
    print("  GET  /health      - Health check")
    print("  GET  /            - API information")
    print("\nServer will be available at: http://localhost:5000")
    
    app.run(
        host='0.0.0.0',
        port=6000,
        debug=True,
        use_reloader=True
    ) 