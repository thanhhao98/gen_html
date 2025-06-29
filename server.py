from flask import Flask, render_template, redirect, url_for, send_from_directory, request
import os
import re
from generate_table import generate_html_from_custom_fields

app = Flask(__name__)

@app.route('/')
def home():
    # Get all subfolders in the templates directory
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    subfolders = [f for f in os.listdir(template_dir) if os.path.isdir(os.path.join(template_dir, f))]
    
    return render_template('home.html', subfolders=subfolders)

@app.route('/create', methods=['POST'])
def create_template():
    template_name = request.form.get('template_name', '').strip()
    custom_fields = request.form.get('custom_fields', '').strip()
    print("from main", custom_fields)
    
    # Validate template name
    if not template_name:
        return render_template('home.html', 
                               message="Template name cannot be empty", 
                               message_class="error-message",
                               subfolders=get_subfolders())
    
    # Make sure the template name is safe for use as a directory name
    if not re.match(r'^[a-zA-Z0-9_-]+$', template_name):
        return render_template('home.html', 
                               message="Template name can only contain letters, numbers, underscores and hyphens", 
                               message_class="error-message",
                               subfolders=get_subfolders())
    
    # Check if template already exists
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates', template_name)
    if os.path.exists(template_dir):
        return render_template('home.html', 
                               message=f"Template '{template_name}' already exists", 
                               message_class="error-message",
                               subfolders=get_subfolders())
    
    # Generate HTML using LLM based on custom fields
    try:
        generated_content = generate_html_from_custom_fields(custom_fields, template_name)
        if not generated_content or 'html' not in generated_content:
            return render_template('home.html',
                                  message="Failed to generate HTML content",
                                  message_class="error-message",
                                  subfolders=get_subfolders())
        
        # Create template directory
        os.makedirs(template_dir)
        
        # Create index.html file
        with open(os.path.join(template_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(generated_content['html'])
        
        # Create specs.json file if specs content exists
        if 'specs' in generated_content and generated_content['specs']:
            with open(os.path.join(template_dir, 'specs.json'), 'w', encoding='utf-8') as f:
                f.write(generated_content['specs'])
        
        return render_template('home.html', 
                               message=f"Template '{template_name}' created successfully", 
                               message_class="success-message",
                               subfolders=get_subfolders())
    except Exception as e:
        return render_template('home.html', 
                               message=f"Error creating template: {str(e)}", 
                               message_class="error-message",
                               subfolders=get_subfolders())

@app.route('/view/<folder>')
def view_template(folder):
    # Check if folder exists
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates', folder)
    if not os.path.exists(template_dir):
        return redirect(url_for('home'))
    
    # Serve the index.html file from that folder
    return render_template(f'{folder}/index.html')

@app.route('/view/<folder>/<path:filename>')
def template_static(folder, filename):
    # Serve static files from template directories
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates', folder)
    return send_from_directory(template_dir, filename)

def get_subfolders():
    # Helper function to get all template subfolders
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    return [f for f in os.listdir(template_dir) if os.path.isdir(os.path.join(template_dir, f))]

if __name__ == '__main__':
    app.run(debug=True)
