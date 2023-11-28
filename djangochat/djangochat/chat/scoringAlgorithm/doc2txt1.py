import docx2txt
import warnings
import os
from .pdf_parser import parse_pdf
def func(value):
    return ''.join(value.splitlines())
warnings.filterwarnings('ignore')
# load the data



path = "./resume"
p=1
for root, d_names, f_names in os.walk(path):
   for i in f_names:
    pat="./resume/"
    resume = docx2txt.process(pat+i)
    # job = docx2txt.process('python-job-description.docx')
    if p==1:
     file = open('C:\\Users\\Admin\\PycharmProjects\\BM25\\text\\corpus.txt','w')
    else:
     file = open('C:\\Users\\Admin\\PycharmProjects\\BM25\\text\\corpus.txt', 'a')
    # file2=open('C:\\Users\\Admin\\PycharmProjects\\BM25\\text\\queries.txt','w')
    resume=func(resume)
    resume="#"+str(p)+"\n"+resume+"\n"
    # job=func(job)
    file.write(resume)
    # file2.write(job)
    file.close()
    # file2.close()
    p=p+1