
import os
import logging
import tempfile
import subprocess

def generate_pdf(chapters: list, output_filename="textbook.pdf"):
    """
    Generate a PDF from a list of chapters.
    chapters: list of dicts {day, title, content_part1..., content_part2...}
    
    Returns: path to generated PDF
    """
    merged_markdown = "# PyTextbook: The Complete Journey\n\n"
    
    for ch in chapters:
        day = ch['day']
        title = ch.get('title', f"Day {day}")
        
        merged_markdown += f"\n\n# Day {day}: {title}\n\n"
        
        if ch.get('content_part1_theory'):
            merged_markdown += ch['content_part1_theory'] + "\n\n"
            
        if ch.get('content_part2_practice'):
            merged_markdown += "## Practice\n\n" + ch['content_part2_practice'] + "\n\n"
            
        if ch.get('content_part3_mentor'):
            merged_markdown += "## Mentor's Note\n\n" + ch['content_part3_mentor'] + "\n\n"

        merged_markdown += "\\newpage\n"  # LaTeX page break

    # Create temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".md", mode='w', encoding='utf-8') as f:
        f.write(merged_markdown)
        temp_md = f.name
        
    output_pdf = os.path.join(tempfile.gettempdir(), output_filename)
    
    # Call Pandoc via subprocess (more reliable than pypandoc sometimes)
    # Assumes pandoc is installed
    cmd = [
        "pandoc",
        temp_md,
        "-o", output_pdf,
        "--toc", # Table of contents
        "--number-sections",
        "-V", "geometry:margin=1in",
        "--pdf-engine=wkhtmltopdf" # OR pdflatex if available, wkhtmltopdf is simpler usually
    ]
    
    try:
        logging.info(f"Running pandoc: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            logging.error(f"Pandoc Failed: {result.stderr}")
            # Fallback to just returning MD if PDF fails?
            return None
            
        return output_pdf
        
    except FileNotFoundError:
        logging.error("Pandoc not found. Please install pandoc.")
        return None
    except Exception as e:
        logging.error(f"PDF Generation Error: {e}")
        return None
