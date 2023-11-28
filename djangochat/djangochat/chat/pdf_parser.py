
# import PyPDF2
# import docx2txt
# import warnings
# import os
# from .pdf_parser import parse_pdf
# def func(value):
#     return ''.join(value.splitlines())
# warnings.filterwarnings('ignore')
# # load the data
#
# #
# def parse_pdf(pdf_file_path):
#  pdf_text = ""
#  with open(pdf_file_path, 'rb') as pdf:
#   pdf_reader = PyPDF2.PdfFileReader(pdf)
#   for page_num in range(pdf_reader.numPages):
#    page = pdf_reader.getPage(page_num)
#    pdf_text += page.extractText()
#  file = open('C:\\Users\\Admin\\PycharmProjects\\BM25\\text\\corpus.txt', 'a')
#  pdf_text=func(pdf_text)
#  resume = "#" + "\n" + pdf_text + "\n"
#  # job=func(job)
#  file.write(resume)
#  # file2.write(job)
#  file.close()
#  return pdf_text

from PyPDF2 import PdfReader

def parse_pdf(pdf_file_path):
    pdf_text = ""
    with open(pdf_file_path, 'rb') as pdf:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            pdf_text += page.extract_text()
    return pdf_text
