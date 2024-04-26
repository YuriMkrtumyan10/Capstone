from django.conf import settings
import os
import pdfplumber
from .gpt import chatgpt_query
import hashlib
import base64

directory = os.path.join(settings.BASE_DIR, 'myapp', 'static', 'pdf')

# def pdf_answer():
#     pdf = os.path.join(settings.BASE_DIR, 'myapp', 'static', 'pdf', 'cyber_kch.pdf')
#     query = 'Explain the image in the pdf'

#     pdf_text = extract_pdf_text(pdf)
#     chatgpt_response = chatgpt_query(query, pdf_text)

#     return chatgpt_response, pdf_text

def extract_pdf_text(pdf_name):
    text = ""
    with pdfplumber.open(directory + '/' + pdf_name + '.pdf') as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    
    return text

def handlePDF(file):
    file_hash = hashlib.sha256(file.read()).hexdigest()[:20]

    file.seek(0)
    
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, file_hash + '.pdf')

    with open(file_path, 'wb') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    
    extract_images_from_pdf(file_hash)

    return file_hash

def load_pdf(file_name):
    messages = []
    if file_name:
        file_content = extract_pdf_text(file_name)
        content = get_images_base64(file_name)
        messages.append(
            {
                "role": "system", 
                "content": [
                    {
                        "type": "text",
                        "text": "The text of the PDF file has been provided. Here it is: '" + file_content + "'"
                    },
                    *content
                ]
            }
        )
        # messages.append({"role": "system", "content": "The text of the PDF file has been provided. Here it is: '" + file_content + "'"})


    return messages

import fitz  # PyMuPDF

def extract_images_from_pdf(pdf_name):
    # Create a subdirectory to store images
    image_directory = os.path.join(directory, 'pdf_images', pdf_name)
    os.makedirs(image_directory, exist_ok=True)

    pdf_path = os.path.join(directory, pdf_name + '.pdf')
    pdf_document = fitz.open(pdf_path)

    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)
        image_list = page.get_images(full=True)

        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]

            image_path = os.path.join(image_directory, f"{img_index}.png")
            with open(image_path, "wb") as image_file:
                image_file.write(image_bytes)

    pdf_document.close()

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def get_images_base64(file):
    content = []

    i = 0
    file_path = os.path.join(directory, 'pdf_images', file, f'{i}.png')

    while os.path.exists(file_path):
        base64_image = encode_image(file_path)
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{base64_image}"
            }
        })
        i += 1
        file_path = os.path.join(directory, 'pdf_images', file, f'{i}.png')
    
    return content
