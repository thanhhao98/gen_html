#!/usr/bin/env python3
"""
Test script for the mocking API
Run this after starting the mocking API server
"""

import requests
import json

# Base URL for the mocking API
BASE_URL = "http://localhost:5001"

def test_health_check():
    """Test the health check endpoint"""
    print("=== Testing Health Check ===")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"Error: {e}")
    print()

def test_list_templates():
    """Test listing all templates"""
    print("=== Testing List Templates ===")
    try:
        response = requests.get(f"{BASE_URL}/api/templates")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"Error: {e}")
    print()

def test_mock_data_single(template_name="test1"):
    """Test generating single mock data record"""
    print(f"=== Testing Mock Data (Single) for {template_name} ===")
    try:
        response = requests.get(f"{BASE_URL}/api/mock/{template_name}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"Error: {e}")
    print()

def test_mock_data_multiple(template_name="test1", count=3):
    """Test generating multiple mock data records"""
    print(f"=== Testing Mock Data (Multiple) for {template_name} ===")
    try:
        response = requests.get(f"{BASE_URL}/api/mock/{template_name}?count={count}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"Error: {e}")
    print()

def test_mock_submit_valid(template_name="test1"):
    """Test form submission with valid data"""
    print(f"=== Testing Mock Submit (Valid) for {template_name} ===")
    
    # First get mock data to use as valid submission
    try:
        mock_response = requests.get(f"{BASE_URL}/api/mock/{template_name}")
        if mock_response.status_code == 200:
            mock_data = mock_response.json()['data']
            
            # Submit the mock data
            submit_response = requests.post(
                f"{BASE_URL}/api/mock/{template_name}/submit",
                json=mock_data,
                headers={'Content-Type': 'application/json'}
            )
            print(f"Status Code: {submit_response.status_code}")
            print(f"Response: {json.dumps(submit_response.json(), indent=2, ensure_ascii=False)}")
        else:
            print(f"Failed to get mock data: {mock_response.status_code}")
    except Exception as e:
        print(f"Error: {e}")
    print()

def test_mock_submit_invalid(template_name="test1"):
    """Test form submission with invalid data"""
    print(f"=== Testing Mock Submit (Invalid) for {template_name} ===")
    
    # Submit invalid data
    invalid_data = {
        "full_name": "Test User",
        "phone_number": "123",  # Invalid phone number
        "satisfaction": "invalid_rating"  # Invalid rating
        # Missing other required fields
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/mock/{template_name}/submit",
            json=invalid_data,
            headers={'Content-Type': 'application/json'}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"Error: {e}")
    print()

def main():
    """Run all tests"""
    print("Starting Mocking API Tests...")
    print("Make sure the mocking API server is running on port 5001")
    print("=" * 50)
    
    test_health_check()
    test_list_templates()
    test_mock_data_single()
    test_mock_data_multiple()
    test_mock_submit_valid()
    test_mock_submit_invalid()
    
    print("All tests completed!")

if __name__ == "__main__":
    main() 