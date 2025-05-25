from dotenv import load_dotenv
import os
from jinja2 import Template

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from the environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")

from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI(api_key=openai_api_key)

def generate_html_from_custom_fields(custom_fields, template_name=None):
    """
    Generates HTML table structure and specs.json based on provided custom field information.
    
    Args:
        custom_fields (str): A string containing field definitions provided by the user
        template_name (str): The template name to use for API calls
    
    Returns:
        dict: Dictionary containing 'html' and 'specs' content, or None if error
    """
    print(f"Starting HTML generation with custom fields: {custom_fields[:100]}...")
    
    # Read default field definitions from default_field.txt
    try:
        with open('default_field.txt', 'r') as f:
            default_field_definitions = f.read().strip()
        print(f"Successfully loaded default field definitions ({len(default_field_definitions)} characters)")
    except Exception as e:
        print(f"Error loading default field definitions: {str(e)}")
        return None
    
    # Read default submit functionality 
    try:
        with open('default_submit_fn.txt', 'r') as f:
            submit_functionality = f.read().strip()
        print(f"Successfully loaded submit functionality ({len(submit_functionality)} characters)")
    except Exception as e:
        print(f"Error loading submit functionality: {str(e)}")
        return None
    
    # Read form title from default_form_title.txt
    try:
        with open('default_form_title.txt', 'r', encoding='utf-8') as f:
            form_title = f.read().strip()
        print(f"Successfully loaded form title: '{form_title}'")
    except Exception as e:
        print(f"Error loading form title: {str(e)}. Using default title.")
        form_title = "Form lấy ý kiến khách hàng"
    
    # Read and prepare API fetch data template
    api_endpoint = ""
    if template_name:
        try:
            with open('default_fetch_data.txt', 'r', encoding='utf-8') as f:
                fetch_data_content = f.read().strip()
            
            # Extract the API endpoint from the curl command
            lines = fetch_data_content.split('\n')
            curl_line = lines[0]  # First line contains the curl command
            
            # Use Jinja2 to render the template_name in the API endpoint
            template = Template(curl_line)
            rendered_curl = template.render(template_name=template_name)
            
            # Extract just the URL from the curl command
            import re
            url_match = re.search(r'"([^"]*)"', rendered_curl)
            if url_match:
                api_endpoint = url_match.group(1)
                print(f"Generated API endpoint: {api_endpoint}")
            
        except Exception as e:
            print(f"Error loading fetch data template: {str(e)}")
            api_endpoint = ""
    
    # Read prompt template from external file
    try:
        with open('prompt_template.txt', 'r', encoding='utf-8') as f:
            prompt_template = f.read().strip()
        print(f"Successfully loaded prompt template ({len(prompt_template)} characters)")
    except Exception as e:
        print(f"Error loading prompt template: {str(e)}")
        return None
    
    # Create prompt for GPT-4o by formatting the template
    prompt = prompt_template.format(
        default_field_definitions=default_field_definitions,
        custom_fields=custom_fields,
        submit_functionality=submit_functionality,
        form_title=form_title,
        api_endpoint=api_endpoint if api_endpoint else "No API endpoint provided"
    )
    
    print(f"Prepared prompt for GPT-4o ({len(prompt)} characters)")
    
    # Generate HTML using GPT-4o
    try:
        print("Making API call to OpenAI...")
        print(prompt)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2, # Lower temperature for more consistent outputs
            max_tokens=10000,
            presence_penalty=0.0, # Neutral presence penalty
            frequency_penalty=0.0, # Neutral frequency penalty
            top_p=0.9 # Slightly constrained sampling for consistency
        )
        print(f"Received response from OpenAI (length: {len(response.choices[0].message.content)} characters)")
        
        full_content = response.choices[0].message.content
        
        # Extract HTML content
        html_content = ""
        if "```html" in full_content:
            html_section = full_content.split("```html")[1].split("```")[0].strip()
            html_content = html_section
            print("Extracted HTML content from markdown code block")
        
        # Extract JSON content
        specs_content = ""
        if "```json" in full_content:
            json_section = full_content.split("```json")[1].split("```")[0].strip()
            specs_content = json_section
            print("Extracted JSON content from markdown code block")
        
        if html_content and specs_content:
            print(f"Successfully generated HTML content ({len(html_content)} characters)")
            print(f"Successfully generated specs content ({len(specs_content)} characters)")
            return {
                'html': html_content,
                'specs': specs_content
            }
        else:
            print("Failed to extract both HTML and JSON content from response")
            return None
    
    except Exception as e:
        print(f"Error generating content: {str(e)}")
        return None

def generate_html_table():
    """
    Generates a standalone HTML file with a table structure based on predefined fields
    and submit functionality.
    """
    # Read field definitions from default_field.txt
    with open('default_field.txt', 'r') as f:
        default_field_definitions = f.read().strip()
    
    # Read custom field definitions from custom_field.txt if it exists
    custom_field_definitions = ""
    if os.path.exists('custom_field.txt'):
        with open('custom_field.txt', 'r', encoding='utf-8') as f:
            custom_field_definitions = f.read().strip()
    
    # Generate content using the new function
    generated_content = generate_html_from_custom_fields(custom_field_definitions, "default_template")
    
    if generated_content and 'html' in generated_content:
        # Save HTML to file
        with open('generated_table.html', 'w', encoding='utf-8') as f:
            f.write(generated_content['html'])
        
        # Save specs.json to file if it exists
        if 'specs' in generated_content and generated_content['specs']:
            with open('generated_specs.json', 'w', encoding='utf-8') as f:
                f.write(generated_content['specs'])
        
        print(f"HTML file generated successfully: generated_table.html")
        return generated_content['html']
    else:
        return None

if __name__ == "__main__":
    generate_html_table() 