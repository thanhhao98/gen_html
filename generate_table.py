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

def generate_fallback_javascript(api_endpoint):
    """
    Generate fallback JavaScript when LLM generation fails
    """
    return f"""
// Automatically load data when page loads
document.addEventListener('DOMContentLoaded', function() {{
    try {{
        const flag = window.parent.document.body
                       .querySelector('#outside_type')
                       .textContent;
        if (flag === 'Template') return;
    }} catch (error) {{
        // If parent window or element doesn't exist, continue with API call
        console.log('Parent window check failed, proceeding with API call');
    }}
    fetchDataFromAPI();
}});

async function fetchDataFromAPI() {{
    const loadingSpinner = document.getElementById('loadingSpinner');
    const messageDiv = document.getElementById('messageDiv');
    
    // Show loading state
    if (loadingSpinner) loadingSpinner.style.display = 'inline-block';
    
    try {{
        const response = await fetch('{api_endpoint}');
        const result = await response.json();
        
        if (result.success && result.data) {{
            // Populate form fields with data
            const formData = result.data;
            
            // Iterate through all form inputs
            const form = document.querySelector('form');
            const inputs = form.querySelectorAll('input, select, textarea');
            
            inputs.forEach(input => {{
                const fieldName = input.name;
                if (formData.hasOwnProperty(fieldName)) {{
                    let value = formData[fieldName];
                    
                    // Convert Vietnamese date format (DD/MM/YYYY) to ISO format (YYYY-MM-DD) for date inputs
                    if (input.type === 'date' && value) {{
                        const dateMatch = value.match(/^(\\d{{2}})\\/(\\d{{2}})\\/(\\d{{4}})$/);
                        if (dateMatch) {{
                            const [, day, month, year] = dateMatch;
                            value = `${{year}}-${{month}}-${{day}}`;
                        }}
                    }}
                    
                    if (input.type === 'radio') {{
                        if (input.value === value.toString()) {{
                            input.checked = true;
                        }}
                    }} else if (input.type === 'checkbox') {{
                        input.checked = Boolean(value);
                    }} else if (input.tagName === 'SELECT') {{
                        // Handle select elements with Vietnamese value mapping
                        if (fieldName === 'gender') {{
                            // Map Vietnamese gender values to option values
                            if (value === 'Nam') {{
                                input.value = 'M';
                            }} else if (value === 'Nữ') {{
                                input.value = 'F';
                            }} else {{
                                input.value = value;
                            }}
                        }} else {{
                            // For other select elements, try to find matching option text
                            const options = input.querySelectorAll('option');
                            let found = false;
                            options.forEach(option => {{
                                if (option.textContent.trim() === value || option.value === value) {{
                                    input.value = option.value;
                                    found = true;
                                }}
                            }});
                            if (!found) {{
                                input.value = value;
                            }}
                        }}
                    }} else {{
                        input.value = value;
                    }}
                }}
            }});
            
            showMessage('Dữ liệu đã được tải thành công!', 'success');
        }} else {{
            showMessage('Không thể tải dữ liệu từ API', 'error');
        }}
    }} catch (error) {{
        console.error('Error fetching data:', error);
        showMessage('Lỗi kết nối đến API: ' + error.message, 'error');
    }} finally {{
        // Hide loading spinner
        if (loadingSpinner) loadingSpinner.style.display = 'none';
    }}
}}

function showMessage(message, type) {{
    const messageDiv = document.getElementById('messageDiv');
    messageDiv.textContent = message;
    messageDiv.className = type === 'success' ? 'success-message' : 'error-message';
    messageDiv.style.display = 'block';
    
    // Hide message after 5 seconds
    setTimeout(() => {{
        messageDiv.style.display = 'none';
    }}, 5000);
}}

// Form submission functionality
document.addEventListener('DOMContentLoaded', function() {{
    const submitBtn = document.querySelector('button[type="button"]');
    if (submitBtn) {{
        submitBtn.addEventListener('click', function() {{
            const form = document.querySelector('form');
            const formData = new FormData(form);
            const dataObject = {{}};
            
            formData.forEach((value, key) => {{
                dataObject[key] = value;
            }});
            
            console.log('Form data:', dataObject);
            showMessage('Form đã được gửi thành công!', 'success');
        }});
    }}
}});
"""

def generate_html_from_custom_fields(custom_fields, template_name=None):
    """
    Generates HTML table structure and specs.json based on provided custom field information.
    Uses a two-step approach: first generate HTML, then generate JavaScript based on actual HTML structure.
    
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
    
    # Read HTML generation prompt template from external file
    try:
        with open('prompt_template.txt', 'r', encoding='utf-8') as f:
            html_prompt_template = f.read().strip()
        print(f"Successfully loaded HTML prompt template ({len(html_prompt_template)} characters)")
    except Exception as e:
        print(f"Error loading HTML prompt template: {str(e)}")
        return None
    
    # Create prompt for HTML generation
    html_prompt = html_prompt_template.format(
        default_field_definitions=default_field_definitions,
        custom_fields=custom_fields,
        submit_functionality=submit_functionality,
        form_title=form_title,
        api_endpoint=api_endpoint if api_endpoint else "No API endpoint provided"
    )
    
    print(f"Prepared HTML prompt for GPT-4o ({len(html_prompt)} characters)")
    
    # STEP 1: Generate HTML using GPT-4o
    try:
        print("Making first API call to OpenAI for HTML generation...")
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": html_prompt}
            ],
            temperature=0.2,
            max_tokens=10000,
            presence_penalty=0.0,
            frequency_penalty=0.0,
            top_p=0.9
        )
        print(f"Received HTML response from OpenAI (length: {len(response.choices[0].message.content)} characters)")
        
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
        
        if not html_content:
            print("Failed to extract HTML content from response")
            return None
            
    except Exception as e:
        print(f"Error generating HTML content: {str(e)}")
        return None
    
    # STEP 2: Generate JavaScript based on actual HTML structure
    try:
        print("Generating JavaScript using fallback method...")
        
        # Use fallback JavaScript directly since LLM generation is unreliable
        js_content = generate_fallback_javascript(api_endpoint)
        
        # Insert JavaScript into HTML
        if js_content:
            # Find the closing </body> tag and insert JavaScript before it
            if "</body>" in html_content:
                html_content = html_content.replace("</body>", f"""
    <script>
{js_content}
    </script>
</body>""")
            else:
                # If no </body> tag, append at the end
                html_content += f"""
    <script>
{js_content}
    </script>
"""
            print("Successfully integrated JavaScript into HTML")
        else:
            print("Warning: No JavaScript content available")
            
    except Exception as e:
        print(f"Error generating JavaScript content: {str(e)}")
        # Continue with HTML only if JavaScript generation fails
    
    if html_content and specs_content:
        print(f"Successfully generated HTML content ({len(html_content)} characters)")
        print(f"Successfully generated specs content ({len(specs_content)} characters)")
        return {
            'html': html_content,
            'specs': specs_content
        }
    else:
        print("Failed to generate complete content")
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