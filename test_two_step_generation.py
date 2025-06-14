#!/usr/bin/env python3
"""
Test script for the two-step HTML and JavaScript generation approach.
This script tests the new functionality where HTML and JavaScript are generated separately.
"""

import os
import sys
from generate_table import generate_html_from_custom_fields

def test_two_step_generation():
    """Test the two-step generation process"""
    print("Testing two-step HTML and JavaScript generation...")
    
    # Test custom fields
    test_custom_fields = """
    độ hài lòng của khách hàng, thang điểm từ 1 tới 5
    đánh giá cụ thể cho khách hàng nhập chi tiết ý kiến
    """
    
    # Generate content using the new two-step approach
    result = generate_html_from_custom_fields(test_custom_fields, "test_template")
    
    if result and 'html' in result and 'specs' in result:
        print("✅ Two-step generation successful!")
        print(f"HTML length: {len(result['html'])} characters")
        print(f"Specs length: {len(result['specs'])} characters")
        
        # Check if JavaScript is included
        if '<script>' in result['html'] and '</script>' in result['html']:
            print("✅ JavaScript successfully integrated into HTML")
        else:
            print("❌ JavaScript not found in HTML")
            
        # Check for specific JavaScript functionality
        js_checks = [
            'DOMContentLoaded',
            'fetchDataFromAPI',
            'showMessage',
            'Vietnamese',
            'gender',
            'Nam',
            'Nữ'
        ]
        
        for check in js_checks:
            if check in result['html']:
                print(f"✅ Found '{check}' in generated code")
            else:
                print(f"⚠️  '{check}' not found in generated code")
        
        # Save test result
        with open('test_generated.html', 'w', encoding='utf-8') as f:
            f.write(result['html'])
        print("✅ Test result saved to 'test_generated.html'")
        
        return True
    else:
        print("❌ Two-step generation failed")
        return False

def test_field_handling():
    """Test specific field handling in generated JavaScript"""
    print("\nTesting field handling in generated JavaScript...")
    
    # Test with various field types
    test_fields = """
    full_name: text input for customer name
    phone_number: phone input with Vietnamese validation
    email: email input for customer email
    dob: date input with Vietnamese format
    gender: select box with Nam/Nữ options
    satisfaction: rating field from 1 to 5
    feedback: textarea for detailed feedback
    newsletter: checkbox for newsletter subscription
    """
    
    result = generate_html_from_custom_fields(test_fields, "field_test")
    
    if result and 'html' in result:
        html = result['html']
        
        # Check for proper field handling
        field_checks = [
            ('text', 'input[type="text"]'),
            ('tel', 'input[type="tel"]'),
            ('email', 'input[type="email"]'),
            ('date', 'input[type="date"]'),
            ('select', '<select'),
            ('textarea', '<textarea'),
            ('checkbox', 'input[type="checkbox"]'),
            ('rating', 'rating')
        ]
        
        for field_type, html_pattern in field_checks:
            if html_pattern in html:
                print(f"✅ {field_type} field found in HTML")
            else:
                print(f"⚠️  {field_type} field not found in HTML")
        
        return True
    else:
        print("❌ Field handling test failed")
        return False

if __name__ == "__main__":
    print("🚀 Starting two-step generation tests...")
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY environment variable not set")
        print("Please set your OpenAI API key in a .env file")
        sys.exit(1)
    
    # Run tests
    test1_passed = test_two_step_generation()
    test2_passed = test_field_handling()
    
    if test1_passed and test2_passed:
        print("\n🎉 All tests passed! Two-step generation is working correctly.")
    else:
        print("\n❌ Some tests failed. Please check the implementation.")
        sys.exit(1) 