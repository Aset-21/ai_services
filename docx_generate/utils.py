from docxtpl import DocxTemplate
from datetime import datetime
import os

def generate_document(template_path, context: dict):
    doc = DocxTemplate(template_path)
    doc.render(context)
    filename = f"generated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
    output_path = os.path.join("media/generated", filename)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc.save(output_path)
    return output_path
