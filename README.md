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
