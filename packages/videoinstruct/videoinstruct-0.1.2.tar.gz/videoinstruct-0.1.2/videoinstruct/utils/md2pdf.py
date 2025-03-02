import os
import markdown
from xhtml2pdf import pisa
import re

def clean_markdown(markdown_text: str) -> str:
    """
    Clean Markdown text by:
      - Ensuring headings have exactly one contiguous group of '#' characters followed by a single space.
        Any extra '#' tokens accidentally placed before the actual heading text are removed.
      - Removing extra leading whitespace from non-code block lines.
      
    Code blocks (delimited by ``` markers) are left unchanged.
    
    Args:
        markdown_text (str): The raw Markdown content.
        
    Returns:
        str: The cleaned Markdown content.
    """
    lines = markdown_text.splitlines()
    cleaned_lines = []
    in_code_block = False

    for line in lines:
        # Check for code block delimiters and toggle code block state.
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            cleaned_lines.append(line)
            continue

        if not in_code_block:
            # Remove any extra indentation.
            line = line.lstrip()

            # Process headings: if the line starts with '#' characters, clean up the heading markers.
            if re.match(r'^#+', line):
                # Capture the initial '#' group and the rest of the text.
                m = re.match(r'^(#+)\s*(.*)$', line)
                if m:
                    hashes = m.group(1)
                    text = m.group(2)
                    # Remove any accidental extra '#' characters from the beginning of the heading text.
                    text = re.sub(r'^#+\s*', '', text)
                    # Reconstruct the heading with a single space after the '#' markers.
                    line = f"{hashes} {text}"
        cleaned_lines.append(line)
    
    return "\n".join(cleaned_lines)

def make_link_callback(base_path):
    """
    Create a link_callback function that resolves relative URIs using the provided base_path.

    Args:
        base_path (str): The directory of the Markdown file.

    Returns:
        function: A link_callback function for xhtml2pdf.
    """
    def link_callback(uri, rel):
        # If URI is absolute (i.e., a web URL), return it unchanged.
        if uri.startswith("http://") or uri.startswith("https://"):
            return uri

        # Build the absolute path relative to the Markdown file's directory.
        abs_path = os.path.join(base_path, uri)
        if not os.path.isfile(abs_path):
            raise Exception(f"File not found: {abs_path}")
        return abs_path

    return link_callback

def convert_html_to_pdf(source_html, output_filename, link_callback_func):
    """
    Convert HTML content to a PDF file using xhtml2pdf.

    Args:
        source_html (str): The HTML content.
        output_filename (str): The output PDF file path.
        link_callback_func (function): The function to resolve URIs (e.g., for images).

    Returns:
        int: 0 if success, or non-zero if an error occurred.
    """
    with open(output_filename, "w+b") as result_file:
        pisa_status = pisa.CreatePDF(source_html, dest=result_file, link_callback=link_callback_func)
    return pisa_status.err

def clean_html_whitespace(html):
    """
    Clean up whitespace in HTML output from markdown conversion.
    Specifically targets spacing issues around headers and paragraphs.
    
    Args:
        html (str): The HTML content generated from markdown.
        
    Returns:
        str: Cleaned HTML with reduced whitespace.
    """
    # Remove empty paragraphs
    html = re.sub(r'<p>\s*</p>', '', html)
    
    # Remove empty paragraphs after headers
    html = re.sub(r'(</h[1-6]>)\s*<p>\s*</p>', r'\1', html)
    
    # Fix spacing between list items
    html = re.sub(r'(</li>)\s*<li>', r'\1<li>', html)
    
    # Remove extra space between paragraphs
    html = re.sub(r'(</p>)\s*<p>', r'\1<p>', html)
    
    return html

def markdown_to_pdf(markdown_text, output_pdf, base_path):
    """
    Convert Markdown text to a PDF file using markdown and xhtml2pdf.
    
    Args:
        markdown_text (str): The Markdown content.
        output_pdf (str): The output PDF file path.
        base_path (str): Base directory to resolve relative paths (i.e., directory of the Markdown file).
    """
    # Convert Markdown to HTML
    html_content = markdown.markdown(markdown_text, extensions=['extra', 'codehilite'])
    
    # Clean up whitespace issues in the generated HTML
    html_content = clean_html_whitespace(html_content)
    
    # Wrap the HTML in a compact document with strict spacing control
    html_template = f"""
    <html>
      <head>
        <meta charset="utf-8">
        <style>
          /* Base body styles */
          body {{ 
            font-family: sans-serif; 
            padding: 20px; 
            line-height: 1.2;
          }}
          
          /* Control image size */
          img {{ max-width: 100%; height: auto; }}
          
          /* Zero margins for paragraphs */
          p {{ margin: 0; padding: 0; }}
          
          /* Tight header spacing */
          h1, h2, h3, h4, h5, h6 {{ 
            margin-top: 10px;
            margin-bottom: 5px;
            padding: 0;
          }}
          
          /* First header should have no top margin */
          body > h1:first-child, body > h2:first-child {{ margin-top: 0; }}
          
          /* Lists should be compact */
          ul, ol {{ 
            margin-top: 0; 
            margin-bottom: 0; 
            padding-top: 0; 
            padding-bottom: 0; 
          }}
          
          /* List items should be tight */
          li {{ 
            margin: 0; 
            padding: 0;
          }}
          
          /* Zero spacing for code blocks */
          pre {{ 
            margin: 0; 
            padding: 5px;
          }}
          
          /* Horizontal rule */
          hr {{
            margin: 10px 0;
            border: 0;
            height: 1px;
            background-color: #ddd;
          }}
        </style>
      </head>
      <body>
        {html_content}
      </body>
    </html>
    """
    
    # Create the link_callback using the provided base_path
    link_callback_func = make_link_callback(base_path)
    
    # Convert the HTML to PDF
    error = convert_html_to_pdf(html_template, output_pdf, link_callback_func)
    if error:
        print("An error occurred during PDF generation.")
    else:
        print(f"PDF generated successfully: {output_pdf}")


    
if __name__ == '__main__':
    # Path to your Markdown file
    md_filepath = '/Users/pouria/Documents/Coding/VideoInstruct/output/20250301_212703/documentation_v1_enhanced.md'
    # Determine the base directory from the Markdown file's absolute path
    base_path = os.path.dirname(os.path.abspath(md_filepath))
    
    # Read the Markdown file
    with open(md_filepath, 'r', encoding='utf-8') as file:
        md_text = file.read()

    # Clean the Markdown text
    cleaned_md_text = clean_markdown(md_text)
    
    # Generate the PDF with images resolved relative to the Markdown file's directory
    markdown_to_pdf(cleaned_md_text, 'output.pdf', base_path)