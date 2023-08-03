import os
from pdf2docx import Converter
import mammoth

import docx
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.enum.style import WD_STYLE_TYPE
from bs4 import BeautifulSoup

def removeImages(input_html_path,output_html_path):
    # Load the HTML file
    with open(input_html_path, 'r') as file:
        html_content = file.read()

    # Create a BeautifulSoup object
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all <img> tags
    img_tags = soup.find_all('img')

    # Remove the HTML content between <img> tags
    for img in img_tags:
        # Remove the next_sibling content (HTML content after <img>)
        img.extract()
    # Get the modified HTML content
    modified_html = soup.prettify()

    # Save the modified HTML content to a file
    with open(output_html_path, 'w') as file:
        file.write(modified_html)



# Threshold for font size (in points)
thresh = 11

def convertBigText(doc_path,output_path,threshold):
    # Load the DOCX file
    doc = docx.Document(doc_path)

    # Iterate over each paragraph in the document
    for paragraph in doc.paragraphs:
        # Check the font size of the paragraph
        if paragraph.runs:
            first_line_font_size = paragraph.runs[0].font.size
            if first_line_font_size is not None and first_line_font_size.pt > threshold:
                # Split the paragraph into two paragraphs
                new_paragraph = paragraph.insert_paragraph_before(paragraph.text.split('\n')[0], style=doc.styles["Heading 1"])
                #new_paragraph.runs[0].font.size = Pt(first_line_font_size.pt)

                # Remove the first line from the original paragraph
                paragraph.text = '\n'.join(paragraph.text.split('\n')[1:])

    # Save the modified document
    doc.save(output_path)

for rawprefix in os.listdir("toGrade"):
    prefix = rawprefix.split("-")[3].strip()
    pdf_file = rawprefix
    docx_file_raw = prefix+"_unprocessed.docx"
    html_file = prefix+".html"
    docx_file = prefix+".docx"
    #now convert docx to html

for docx_file in os.listdir("docxs"):
    with open("docxs/"+docx_file,'rb') as docFile:
        result = mammoth.convert_to_html(docFile)

    html_file = docx_file.split(".docx")[0].strip()
    
    with open("docxs/"+html_file,'w') as htmlFile:
        htmlFile.write(result.value)
        
    #remove images, since images are now saved as raw data inside of the html
    removeImages("docxs/"+html_file,"processed/"+html_file.split(".html")[0]+"_clean.html")
    
    
"""
    #Convert pdf to docx
    c = Converter("toGrade/"+pdf_file)
    c.convert("docxs/"+docx_file_raw)
    c.close
    
    #Update the heading information
    convertBigText("docxs/"+docx_file_raw,"docxs/"+docx_file,12)
"""
