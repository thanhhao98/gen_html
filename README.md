# HTML Table Generator

This tool generates a standalone HTML file containing a table with form fields and submit functionality based on predefined specifications. The generated HTML is localized for Vietnamese users with appropriate language and validation standards.

## Features

- Vietnamese language for all text elements (labels, placeholders, error messages, buttons)
- Support for both default and custom field definitions
- Intelligent interpretation of brief field descriptions in Vietnamese
- Vietnamese phone number validation format (10 digits, typically starting with 03, 05, 07, 08, 09)
- Vietnamese date format (DD/MM/YYYY)
- Responsive design with modern aesthetics
- Form validation with Vietnamese error messages
- Smart UI element selection based on field type (star ratings, sliders, textareas, etc.)
- **Two-step AI generation**: HTML and JavaScript are generated separately for better compatibility
- **Field-aware JavaScript**: JavaScript is generated based on actual HTML structure for perfect compatibility

## Architecture

The system uses a **two-step LLM approach**:

1. **First LLM Call**: Generates HTML structure and CSS styling based on field definitions
2. **Second LLM Call**: Generates JavaScript based on the actual HTML structure created in step 1

This approach ensures that:
- JavaScript is always compatible with the generated HTML
- All field types are properly handled
- Vietnamese value mapping works correctly
- Edge cases are handled appropriately

## Setup

1. Create a `.env` file in the root directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Define your default form fields in `default_field.txt` using the format:
   ```
   field_name: field description
   ```

2. (Optional) Define custom Vietnamese fields in `custom_field.txt`, with one field per line:
   ```
   độ hài lòng của khách hàng, thang điểm từ 1 tới 5
   đánh giá cụ thể cho khách hàng nhập chi tiết ý kiến
   ```
   Note: Custom field descriptions can be brief - the system will intelligently interpret them.

3. Define your submit button functionality in `default_submit_fn.txt`.

4. Run the generator:
   ```
   python generate_table.py
   ```

5. The generated HTML file will be saved as `generated_table.html` in the same directory.

6. Open the HTML file in a web browser to test the form.

## Web Interface

For easier template management, you can also use the web interface:

1. Start the web server:
   ```
   python server.py
   ```

2. Open your browser to `http://localhost:5000`

3. Use the web interface to:
   - Create new templates with custom fields
   - View existing templates
   - Manage template directories

## Mock API

For testing purposes, a mock API server is included:

1. Start the mock API server:
   ```
   python mocking_be.py
   ```

2. The mock API will run on `http://localhost:5001` and provide realistic Vietnamese test data

3. Generated forms will automatically load data from the mock API

## Configuration Files

- `default_field.txt`: Base field definitions
- `default_submit_fn.txt`: Submit button functionality
- `default_form_title.txt`: Form title in Vietnamese
- `default_fetch_data.txt`: API endpoint template
- `prompt_template.txt`: HTML generation prompt
- `javascript_generation_prompt.txt`: JavaScript generation prompt

## Generated Output

Each template generates:
- `index.html`: Complete HTML form with embedded CSS and JavaScript
- `specs.json`: Field specifications for the mock API
