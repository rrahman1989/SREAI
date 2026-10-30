import ollama
from docx import Document

MODEL_NAME = "qwen2.5-coder:7b"

# 1. Read your incident artifacts
with open("incident_artifacts.txt", "r") as f:
    artifacts = f.read()

# 2. Ask Qwen to write the postmortem
prompt = f"""
You are an expert SRE lead. 
Based on the raw incident artifacts below, generate a professional, blameless postmortem report with these exact sections:
1. Incident Overview
2. Timeline
3. Root Cause
4. Action Items

Artifacts:
{artifacts}
"""

print("Generating postmortem content with Qwen...")
response = ollama.chat(model=MODEL_NAME, messages=[{"role": "user", "content": prompt}])
postmortem_text = response['message']['content']

# 3. Use python-docx to create a real Word document
doc = Document()
doc.add_heading("SRE Incident Postmortem", level=1)

# Add the AI-generated text into the Word document paragraphs
for line in postmortem_text.split("\n"):
    if line.startswith("#"):
        # Handle markdown headers by mapping them to Word heading levels
        doc.add_heading(line.replace("#", "").strip(), level=2)
    elif line.strip():
        doc.add_paragraph(line.strip())

# Save the file to your project directory
output_filename = "SRE_Postmortem_Report.docx"
doc.save(output_filename)

print(f"Success! Word document created: {output_filename}")