import subprocess
import shutil

# To try the actual template out, compile with the file under analysis/templates/

def generate_pdf(name, age):
    '''
    Generate a `.pdf` using the given template and the two dynamically added arguments.
    '''
    # Read the template
    with open('example.tex', 'r') as template_file:
        template_content = template_file.read()

    # Replace placeholders with dynamic data
    template_content = template_content.replace('<<NAME>>', name)
    template_content = template_content.replace('<<AGE>>', str(age))

    # Write the filled template to a new file
    with open('filled_template.tex', 'w') as filled_template_file:
        filled_template_file.write(template_content)

    # Compile LaTeX to PDF using pdflatex
    subprocess.run(['pdflatex', 'filled_template.tex'])

    # Clean up auxiliary files
    shutil.rmtree('__pycache__', ignore_errors=True)
    shutil.rmtree('filled_template.aux', ignore_errors=True)
    shutil.rmtree('filled_template.log', ignore_errors=True)

if __name__ == "__main__":
    generate_pdf('John Doe', 25)
