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
    - Create a premium, modern UI with a professional design suitable for enterprise applications
    - Use a visually appealing color palette with a primary brand color and complementary accent colors
    - Implement a card-based design with elegant shadows (box-shadow: 0 10px 25px rgba(0,0,0,0.1))
    - Use modern CSS techniques including:
      * Subtle gradients for buttons and backgrounds
      * Border-radius of 8-12px for components
      * Variable font weights for better typography
      * CSS Grid or Flexbox for responsive layouts
    - Add sophisticated animations and transitions:
      * Smooth hover effects on all interactive elements (transform: scale(1.02), transition: 0.3s ease)
      * Loading/success animations for form submission
      * Subtle micro-interactions (focus states, validation feedback)
    - Implement modern form elements:
      * Custom-styled checkboxes and radio buttons
      * Elegant dropdown menus with custom styling
      * Placeholder animations for text inputs
      * Clean, accessible form validation with visual feedback
    - For rating inputs, use star ratings or emoji-based feedback systems instead of plain dropdowns
    - Include visual elements like icons from Font Awesome or Material Icons for better UX
    - Use a modern Vietnamese-compatible font like 'Montserrat', 'Nunito', or 'Roboto'
    - Design the submit button with a gradient background and hover animation
    - Add a decorative header section with a subtle pattern or gradient background
    - Implement proper spacing using a consistent rhythm (8px multipliers for margins/padding)
    - Enhance mobile responsiveness with media queries for different device sizes
    - Add subtle background patterns or textures to add depth
    - Use CSS variables for consistent color application throughout the form
    
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