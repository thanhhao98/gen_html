from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from the environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")

from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI(api_key=openai_api_key)

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
    
    # Read submit functionality from default_submit_fn.txt
    with open('default_submit_fn.txt', 'r') as f:
        submit_functionality = f.read().strip()
    
    # Create prompt for GPT-4
    prompt = f"""
    Create a standalone HTML file with embedded CSS and JavaScript that includes:
    
    1. A form with a table structure containing the following default fields:
    {default_field_definitions}
    
    2. Also include these custom fields defined in Vietnamese (interpret them intelligently even if the descriptions are brief):
    {custom_field_definitions}
    
    3. A submit button that implements this functionality:
    {submit_functionality}
    
    IMPORTANT INTERPRETATION GUIDELINES:
    - For the custom fields in Vietnamese, be flexible and interpret the meaning even if descriptions are minimal
    - Infer the appropriate input type based on the field description
    - For rating scales, use appropriate UI elements like star ratings or slider inputs
    - For text inputs accepting detailed feedback, provide appropriate textarea elements
    - Match field names intelligently with their likely purpose in the submission function
    
    IMPORTANT REQUIREMENTS:
    
    - The HTML document should use Vietnamese language for all text, labels, placeholders, error messages, and button text
    - Set the language attribute to Vietnamese (vi) in the HTML tag
    - Use proper Vietnamese character encoding (UTF-8)
    - For validation:
      * Phone numbers should follow Vietnamese format (10 digits, typically starting with 03, 05, 07, 08, 09)
      * Date formats should follow Vietnamese convention (DD/MM/YYYY)
      * Error messages must be in Vietnamese
    
    DESIGN REQUIREMENTS:
    - Create a clean, modern, and professional design with soft shadows and rounded corners
    - Use a pleasing color palette suitable for Vietnamese users (consider using colors that resonate with Vietnamese culture)
    - Add subtle animations for form interactions (focus states, button hover effects)
    - Make the form responsive for all device sizes
    - Use a font that properly supports Vietnamese characters (like Roboto, Open Sans, or Noto Sans Vietnamese)
    - Include appropriate spacing between form elements for better readability
    - Add subtle background patterns or gradients to enhance visual appeal
    - Style the table with alternating row colors for better readability
    - Use clear visual hierarchy with proper heading sizes and font weights
    - For rating inputs, use visually appealing interactive elements
    
    Include all necessary HTML, CSS, and JavaScript in a single file.
    """
    
    # Generate HTML using GPT-4
    try:
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
        html_content = response.choices[0].message.content
        
        # Extract just the HTML if it's wrapped in markdown code blocks
        if "```html" in html_content and "```" in html_content.split("```html")[1]:
            html_content = html_content.split("```html")[1].split("```")[0].strip()
        elif "```" in html_content:
            html_content = html_content.split("```")[1].split("```")[0].strip()
        
        # Save HTML to file
        with open('generated_table.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"HTML file generated successfully: generated_table.html")
        return html_content
    
    except Exception as e:
        print(f"Error generating HTML: {str(e)}")
        return None

if __name__ == "__main__":
    generate_html_table() 