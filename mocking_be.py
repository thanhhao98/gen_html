from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import random
import os
from datetime import datetime, timedelta
from faker import Faker
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# Enable CORS for all routes
CORS(app, origins=['http://127.0.0.1:5000', 'http://localhost:5000'])

# Initialize Faker with Vietnamese locale
fake = Faker('vi_VN')

# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

def format_datetime_vietnamese(dt=None):
    """
    Format datetime in Vietnamese format (DD/MM/YYYY HH:MM:SS)
    
    Args:
        dt (datetime, optional): Datetime object to format. Defaults to current time.
    
    Returns:
        str: Formatted datetime string
    """
    if dt is None:
        dt = datetime.now()
    return dt.strftime('%d/%m/%Y %H:%M:%S')

def format_date_vietnamese(dt=None):
    """
    Format date in Vietnamese format (DD/MM/YYYY)
    
    Args:
        dt (datetime, optional): Datetime object to format. Defaults to current time.
    
    Returns:
        str: Formatted date string
    """
    if dt is None:
        dt = datetime.now()
    return dt.strftime('%d/%m/%Y')

def generate_mock_data_with_llm(field_specs):
    """
    Generate mock data using OpenAI GPT-4o model
    
    Args:
        field_specs (list): List of field specifications
    
    Returns:
        dict: Generated mock data for all fields
    """
    try:
        # Create a prompt for the LLM
        fields_description = []
        for field in field_specs:
            field_desc = f"- {field['ten_field']} ({field['ten_hien_thi']}): type={field['kieu_du_lieu']}"
            fields_description.append(field_desc)
        
        prompt = f"""Generate realistic mock data for a Vietnamese form with the following fields:

{chr(10).join(fields_description)}

Requirements:
- Use Vietnamese names, addresses, and context where appropriate
- For phone numbers, use Vietnamese format (10 digits starting with 0)
- For emails, use realistic Vietnamese email addresses
- For ALL date and datetime fields, ALWAYS use DD/MM/YYYY format (e.g., "15/03/1990", "25/12/1985")
- NEVER use YYYY-MM-DD, MM/DD/YYYY, or any other date format
- For datetime fields that need time, use DD/MM/YYYY HH:MM:SS format (e.g., "15/03/1990 14:30:00")
- For ratings, use numbers 1-5
- For select fields, choose appropriate Vietnamese options based on field name
- For text areas, write in Vietnamese
- Return ONLY a valid JSON object with field names as keys

Example format:
{{
    "field_name1": "value1",
    "field_name2": "value2",
    "date_field": "15/03/1990",
    "datetime_field": "25/12/1985 10:30:00"
}}"""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates realistic Vietnamese mock data for forms. Always respond with valid JSON only. IMPORTANT: For all date fields, use DD/MM/YYYY format (never YYYY-MM-DD or MM/DD/YYYY)."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        # Parse the response
        response_text = response.choices[0].message.content.strip()
        
        # Remove any markdown formatting if present
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        
        mock_data = json.loads(response_text)
        
        # Post-process to ensure date fields are in DD/MM/YYYY format
        for field_spec in field_specs:
            field_name = field_spec['ten_field']
            field_type = field_spec['kieu_du_lieu']
            
            if field_type in ['date', 'datetime'] and field_name in mock_data:
                date_value = mock_data[field_name]
                # Try to parse and reformat if it's not in correct format
                try:
                    if field_type == 'datetime':
                        # First try DD/MM/YYYY HH:MM:SS format
                        parsed_date = datetime.strptime(str(date_value), '%d/%m/%Y %H:%M:%S')
                        mock_data[field_name] = format_datetime_vietnamese(parsed_date)
                    else:
                        # First try DD/MM/YYYY format for date fields
                        parsed_date = datetime.strptime(str(date_value), '%d/%m/%Y')
                        mock_data[field_name] = format_date_vietnamese(parsed_date)
                except ValueError:
                    try:
                        if field_type == 'datetime':
                            # Try ISO format and convert to Vietnamese datetime
                            parsed_date = datetime.fromisoformat(str(date_value).replace('Z', '+00:00'))
                            mock_data[field_name] = format_datetime_vietnamese(parsed_date)
                        else:
                            # Try YYYY-MM-DD format and convert to Vietnamese date
                            parsed_date = datetime.strptime(str(date_value), '%Y-%m-%d')
                            mock_data[field_name] = format_date_vietnamese(parsed_date)
                    except ValueError:
                        try:
                            # Try MM/DD/YYYY format and convert
                            parsed_date = datetime.strptime(str(date_value), '%m/%d/%Y')
                            if field_type == 'datetime':
                                mock_data[field_name] = format_datetime_vietnamese(parsed_date)
                            else:
                                mock_data[field_name] = format_date_vietnamese(parsed_date)
                        except ValueError:
                            # If all parsing fails, use fallback
                            start_date = datetime(1970, 1, 1)
                            end_date = datetime(2005, 12, 31)
                            random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
                            if field_type == 'datetime':
                                mock_data[field_name] = format_datetime_vietnamese(random_date)
                            else:
                                mock_data[field_name] = format_date_vietnamese(random_date)
        
        return mock_data
        
    except Exception as e:
        print(f"Error generating data with LLM: {e}")
        # Fallback to original method if LLM fails
        return generate_fallback_mock_data(field_specs)

def generate_fallback_mock_data(field_specs):
    """
    Simple fallback method if LLM fails - returns basic mock data
    
    Args:
        field_specs (list): List of field specifications
    
    Returns:
        dict: Basic mock data for all fields
    """
    mock_data = {}
    for field_spec in field_specs:
        field_name = field_spec['ten_field']
        field_type = field_spec['kieu_du_lieu']
        
        # Simple fallback values based on field type
        if field_type == 'text':
            mock_data[field_name] = "Dữ liệu mẫu"
        elif field_type == 'tel':
            mock_data[field_name] = "0987654321"
        elif field_type == 'email':
            mock_data[field_name] = "example@email.com"
        elif field_type == 'date':
            # Generate random date between 1970 and 2005 in DD/MM/YYYY format
            start_date = datetime(1970, 1, 1)
            end_date = datetime(2005, 12, 31)
            random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
            mock_data[field_name] = format_date_vietnamese(random_date)
        elif field_type == 'datetime':
            # Generate random datetime between 1970 and 2005 in DD/MM/YYYY HH:MM:SS format
            start_date = datetime(1970, 1, 1)
            end_date = datetime(2005, 12, 31)
            random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
            # Add random time
            random_hour = random.randint(0, 23)
            random_minute = random.randint(0, 59)
            random_second = random.randint(0, 59)
            random_datetime = random_date.replace(hour=random_hour, minute=random_minute, second=random_second)
            mock_data[field_name] = format_datetime_vietnamese(random_datetime)
        elif field_type == 'rating':
            mock_data[field_name] = 3
        elif field_type == 'number':
            mock_data[field_name] = 1
        elif field_type == 'select':
            mock_data[field_name] = "Tùy chọn"
        elif field_type == 'textarea':
            mock_data[field_name] = "Nội dung mẫu"
        elif field_type == 'checkbox':
            mock_data[field_name] = True
        elif field_type == 'radio':
            mock_data[field_name] = "Có"
        else:
            mock_data[field_name] = "Giá trị mặc định"
    
    return mock_data

@app.route('/api/mock/<template_name>', methods=['GET'])
def get_mock_data(template_name):
    """
    Generate mock data based on specs.json for a specific template using LLM
    
    Args:
        template_name (str): Name of the template folder
    
    Returns:
        JSON response with mock data
    """
    try:
        # Path to specs.json file
        specs_path = os.path.join('templates', template_name, 'specs.json')
        
        if not os.path.exists(specs_path):
            return jsonify({
                'error': f'Specs file not found for template: {template_name}',
                'message': f'File {specs_path} does not exist'
            }), 404
        
        # Read specs.json
        with open(specs_path, 'r', encoding='utf-8') as f:
            specs = json.load(f)
        
        # Get count parameter for multiple records
        count = request.args.get('count', 1, type=int)
        count = min(count, 100)  # Limit to 100 records max
        
        if count == 1:
            # Generate single record using LLM
            mock_data = generate_mock_data_with_llm(specs)
            print(mock_data)
            
            return jsonify({
                'success': True,
                'template': template_name,
                'data': mock_data,
                'generated_by': 'llm'
            })
        else:
            # Generate multiple records
            records = []
            for _ in range(count):
                mock_data = generate_mock_data_with_llm(specs)
                records.append(mock_data)
            
            return jsonify({
                'success': True,
                'template': template_name,
                'count': count,
                'data': records,
                'generated_by': 'llm'
            })
    
    except json.JSONDecodeError:
        return jsonify({
            'error': 'Invalid JSON format in specs file',
            'message': f'Could not parse specs.json for template: {template_name}'
        }), 400
    
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route('/api/templates', methods=['GET'])
def list_templates():
    """
    List all available templates with their specs
    
    Returns:
        JSON response with list of templates
    """
    try:
        templates_dir = 'templates'
        if not os.path.exists(templates_dir):
            return jsonify({
                'error': 'Templates directory not found',
                'templates': []
            }), 404
        
        templates = []
        for item in os.listdir(templates_dir):
            item_path = os.path.join(templates_dir, item)
            if os.path.isdir(item_path):
                specs_path = os.path.join(item_path, 'specs.json')
                if os.path.exists(specs_path):
                    try:
                        with open(specs_path, 'r', encoding='utf-8') as f:
                            specs = json.load(f)
                        
                        templates.append({
                            'name': item,
                            'fields_count': len(specs),
                            'fields': [
                                {
                                    'display_name': field['ten_hien_thi'],
                                    'field_name': field['ten_field'],
                                    'field_type': field['kieu_du_lieu']
                                }
                                for field in specs
                            ]
                        })
                    except:
                        # Skip templates with invalid specs.json
                        continue
        
        return jsonify({
            'success': True,
            'count': len(templates),
            'templates': templates
        })
    
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route('/api/mock/<template_name>/submit', methods=['POST'])
def mock_submit(template_name):
    """
    Mock form submission endpoint that validates data against specs
    
    Args:
        template_name (str): Name of the template folder
    
    Returns:
        JSON response simulating form submission
    """
    try:
        # Path to specs.json file
        specs_path = os.path.join('templates', template_name, 'specs.json')
        
        if not os.path.exists(specs_path):
            return jsonify({
                'error': f'Specs file not found for template: {template_name}'
            }), 404
        
        # Read specs.json
        with open(specs_path, 'r', encoding='utf-8') as f:
            specs = json.load(f)
        
        # Get submitted data
        submitted_data = request.get_json() or request.form.to_dict()
        
        # Validate submitted data against specs
        validation_errors = []
        expected_fields = [field['ten_field'] for field in specs]
        
        for field_spec in specs:
            field_name = field_spec['ten_field']
            field_type = field_spec['kieu_du_lieu']
            
            if field_name not in submitted_data:
                validation_errors.append(f"Missing required field: {field_name}")
            else:
                value = submitted_data[field_name]
                
                # Basic type validation
                if field_type == 'tel' and value:
                    if not (len(str(value)) == 10 and str(value).isdigit()):
                        validation_errors.append(f"Invalid phone number format: {field_name}")
                
                elif field_type == 'email' and value:
                    if '@' not in str(value):
                        validation_errors.append(f"Invalid email format: {field_name}")
                
                elif field_type == 'rating' and value:
                    try:
                        rating_val = int(value)
                        if rating_val < 1 or rating_val > 5:
                            validation_errors.append(f"Rating must be between 1-5: {field_name}")
                    except ValueError:
                        validation_errors.append(f"Rating must be a number: {field_name}")
                
                elif field_type == 'date' and value:
                    try:
                        # Validate DD/MM/YYYY format
                        datetime.strptime(str(value), '%d/%m/%Y')
                    except ValueError:
                        validation_errors.append(f"Invalid date format, must be DD/MM/YYYY: {field_name}")
                
                elif field_type == 'datetime' and value:
                    try:
                        # Validate DD/MM/YYYY HH:MM:SS format
                        datetime.strptime(str(value), '%d/%m/%Y %H:%M:%S')
                    except ValueError:
                        validation_errors.append(f"Invalid datetime format, must be DD/MM/YYYY HH:MM:SS: {field_name}")
        
        # Simulate processing time
        import time
        time.sleep(0.5)
        
        if validation_errors:
            return jsonify({
                'success': False,
                'message': 'Validation failed',
                'errors': validation_errors,
                'submitted_data': submitted_data
            }), 400
        else:
            return jsonify({
                'success': True,
                'message': 'Form submitted successfully',
                'submission_id': f"SUB_{random.randint(100000, 999999)}",
                'timestamp': format_datetime_vietnamese(),
                'submitted_data': submitted_data
            })
    
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Mocking API',
        'timestamp': format_datetime_vietnamese()
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)
