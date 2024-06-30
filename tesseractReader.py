import pytesseract
from pdf2image import convert_from_path
import os
import torch

def clean_text(text):
    chars_to_remove = ['"', ',', '!', '?', '.', '/', '(', ')', '{', '}', '[', ']', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', ';', ':', '-', '‘', '’']
    for char in chars_to_remove:
        text = text.replace(char, " ")
    return text

def generate_text(prompt):
    print("enter generate text")
#     eval_prompt = "Uncorrected balinese language:umbhE kepri alkab kadajéyané séng tkano sai wéuudj banget nengsemak ita \nCorrected balinese language: #"
    model_input = tokenizer(prompt, return_tensors="pt").to("cuda")

    ft_model.eval()
    with torch.no_grad():
        generated_text = tokenizer.decode(ft_model.generate(**model_input, max_new_tokens=100, repetition_penalty=1.15)[0], skip_special_tokens=True)
        print(tokenizer.decode(ft_model.generate(**model_input, max_new_tokens=100, repetition_penalty=1.15)[0], skip_special_tokens=True))

    print("out generate text")
    return generated_text

def extract_text_from_pdf(pdf_path, first_page_number, last_page_number, output_txt_uncorrected, output_txt_corrected):
    images = convert_from_path(pdf_path, first_page=first_page_number, last_page=last_page_number)
    temp_image_dir = 'temp_images'
    if not os.path.exists(temp_image_dir):
        os.makedirs(temp_image_dir)
    
    extracted_text_uncorrected = ''
    extracted_text_corrected = ''
    
    for i, image in enumerate(images):
        temp_image_path = os.path.join(temp_image_dir, f'page_{i}.jpg')
        image.save(temp_image_path, 'JPEG')
        text = pytesseract.image_to_string(image)
        cleaned_text = clean_text(text)
        
        extracted_text_uncorrected += cleaned_text + '\n\n'
        print("get cleaned text\n")
        print(cleaned_text)
        corrected_text = generate_text("Uncorrected balinese language: " + cleaned_text + "\nCorrected balinese language: #")
        extracted_text_corrected += corrected_text + '\n\n'

    with open(output_txt_uncorrected, 'w', encoding='utf-8') as txt_file_uncorrected:
        txt_file_uncorrected.write(extracted_text_uncorrected)
    print("write uncorrected")
        
    with open(output_txt_corrected, 'w', encoding='utf-8') as txt_file_corrected:
        txt_file_corrected.write(extracted_text_corrected)
    print("write corrected")

    for image_path in os.listdir(temp_image_dir):
        os.remove(os.path.join(temp_image_dir, image_path))
    os.rmdir(temp_image_dir)

fileName = input("Input file name: ")
pdf_file = fileName + ".pdf"
start_page_number = int(input("Start page number: "))
last_page_number = int(input("Last page number: "))
output_text_file_uncorrected = "./TesOcr/output/" +  fileName + "_" + str(start_page_number) + "_" + str(last_page_number) + "_output_uncorrected.txt"
output_text_file_corrected = "./TesOcr/output/" +  fileName + "_" + str(start_page_number) + "_" + str(last_page_number) + "_output_corrected.txt"
extract_text_from_pdf(pdf_file, start_page_number, last_page_number, output_text_file_uncorrected, output_text_file_corrected)
