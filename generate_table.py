from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from the environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")

from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI(api_key=openai_api_key)

def generate_html_from_custom_fields(custom_fields):
    """
    Generates HTML table structure based on provided custom field information.
    
    Args:
        custom_fields (str): A string containing field definitions provided by the user
    
    Returns:
        str: The generated HTML content
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
    
    # Create prompt for GPT-4o
    prompt = f"""
    Create a standalone HTML file with embedded CSS and JavaScript that includes:
    
    1. A form with a table structure containing the following default fields:
    {default_field_definitions}
    
    2. Also include these custom fields defined in Vietnamese (interpret them intelligently even if the descriptions are brief):
    {custom_fields}
    
    3. A submit button that implements this functionality:
    {submit_functionality}
    
    4. Use this exact title for the form (as an h1 element):
    {form_title}
    
    IMPORTANT INTERPRETATION GUIDELINES:
    - For the custom fields in Vietnamese, be flexible and interpret the meaning even if descriptions are minimal
    - Infer the appropriate input type based on the field description
    - For rating scales, use appropriate UI elements like star ratings or slider inputs
    - For text inputs accepting detailed feedback, provide appropriate textarea elements
    - Match field names intelligently with their likely purpose in the submission function
    - EVERY field must have appropriate styling and behavior specific to its type
    
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
    
    FIELD-SPECIFIC STYLING AND BEHAVIOR REQUIREMENTS:
    - Text inputs:
      * Apply consistent padding (12px), border-radius, and subtle border
      * Include focus animation (border color change, subtle glow effect)
      * Add floating or animated labels/placeholders
      * Implement real-time validation with visual feedback
    
    - Textarea elements:
      * Auto-resize based on content (or set appropriate min/max height)
      * Line height and padding optimized for readability
      * Character/word count display when appropriate
      * Smooth focus transitions
    
    - Dropdown selects:
      * Custom arrow indicator for dropdown
      * Styled dropdown menu with hover effects
      * Properly aligned and consistent with other form elements
      * Animated dropdown expansion/collapse
    
    - Checkboxes and radio buttons:
      * Replace default styling with custom visuals (maintain accessibility)
      * Clear visual distinction between checked/unchecked states
      * Smooth transition animations between states
      * Adequate spacing and touch targets for mobile
    
    - Date inputs:
      * Formatted according to Vietnamese convention (DD/MM/YYYY)
      * Custom datepicker styling that matches overall design
      * Calendar popup with elegant animations
      * Pre-validation to ensure correct date format
    
    - Number inputs:
      * Custom styled increment/decrement buttons
      * Input validation for numeric values
      * Appropriate min/max constraints where logical
      * Proper formatting for currency or percentage values if applicable
    
    - Email/Phone inputs:
      * Field-specific validation (email format, Vietnamese phone format)
      * Visual indicators for validation status
      * Appropriate keyboard type on mobile devices
      * Helpful error messages in Vietnamese for invalid inputs

    RATING IMPLEMENTATION REQUIREMENTS:
    - For any rating or satisfaction fields (like "Độ hài lòng của khách hàng" or similar):
      * Always parse the field description to identify any specified rating scale (e.g., "rating out of 20", "scale from 1-10", "rate 1-7")
      * Use exactly the specified number of rating points when a scale is mentioned
      * If user doesn't specify a specific rating scale, use 5 stars as the default
      * Implement the appropriate UI based on scale size:
        - For scales 1-10: Use star, heart, or similar icon-based rating system
        - For larger scales (>10): Use a slider with visible tick marks and value display
      * Ensure each rating point/value is individually selectable
      * Properly capture and store the selected rating value
      * Add visual feedback (color change, animation) when ratings are selected
      * Handle hover states to preview potential selections
      * Implement responsive behavior for all screen sizes
      * Test thoroughly to ensure the selected value is correctly captured

    
    - Include visual elements like icons from Font Awesome or Material Icons for better UX
    - Use a modern Vietnamese-compatible font like 'Montserrat', 'Nunito', or 'Roboto'
    - Design the submit button with a gradient background and hover animation
    - Add a decorative header section with a subtle pattern or gradient background
    - Implement proper spacing using a consistent rhythm (8px multipliers for margins/padding)
    - Enhance mobile responsiveness with media queries for different device sizes
    - Add subtle background patterns or textures to add depth
    - Use CSS variables for consistent color application throughout the form
    
    Include all necessary HTML, CSS, and JavaScript in a single file.
    
    IMPLEMENTATION VERIFICATION REQUIREMENTS:
    - Confirm all fields have the specified styling applied
    - Verify all interactive behaviors work correctly
    - Test form validation for all field types
    - Ensure all animations and transitions function as expected
    - Check that the form renders properly on different screen sizes
    - Verify that all rating systems are fully functional with the EXACT number of rating points specified in the field description
    - Test all validation rules with both valid and invalid inputs
    """
    
    print(f"Prepared prompt for GPT-4o ({len(prompt)} characters)")
    
    # Generate HTML using GPT-4o
    try:
        print("Making API call to OpenAI...")
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
        
        html_content = response.choices[0].message.content
        
        # Extract just the HTML if it's wrapped in markdown code blocks
        if "```html" in html_content and "```" in html_content.split("```html")[1]:
            html_content = html_content.split("```html")[1].split("```")[0].strip()
            print("Extracted HTML content from markdown code block with ```html tag")
        elif "```" in html_content:
            html_content = html_content.split("```")[1].split("```")[0].strip()
            print("Extracted HTML content from generic markdown code block")
        
        print(f"Successfully generated HTML content ({len(html_content)} characters)")
        return html_content
    
    except Exception as e:
        print(f"Error generating HTML: {str(e)}")
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
    
    # Generate HTML using the new function
    html_content = generate_html_from_custom_fields(custom_field_definitions)
    
    if html_content:
        # Save HTML to file
        with open('generated_table.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"HTML file generated successfully: generated_table.html")
        return html_content
    else:
        return None

if __name__ == "__main__":
    generate_html_table() 