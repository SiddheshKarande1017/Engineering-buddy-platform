import docx
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm,Addproblem,Addtopic
from django.contrib import messages
from .models import Problem, Sources
from django.contrib.auth.decorators import login_required
from .scoringAlgorithm.parse import *
from .scoringAlgorithm.query import QueryProcessor

# from .parse import *
# from .query import QueryProcessor
from django.http import HttpResponse
import operator
import docx2txt
from django.shortcuts import render, redirect
from .forms import UploadDocForm
from .models import UploadedDoc
from .models import UploadedDoc
#from .utils import parse_docx, parse_doc
import warnings
import os
from .pdf_parser import parse_pdf
def func(value):
    return ''.join(value.splitlines())
warnings.filterwarnings('ignore')

from .pdf_parser import parse_pdf
from urllib.parse import quote

# Create your views here.
Dict = {}
@login_required(login_url='login')
def home(request):
    return render(request,'index.html',{'success_message': ''})

def register(request):
    form_pre = UserForm()
    if request.method == 'POST':
        form_pre = UserForm(request.POST)
        if form_pre.is_valid():
            form_pre.save()
            messages.success(request, 'Account created successfully..')
            return redirect('login')
    context = {'form': form_pre}
    return render(request,"register.html",context)

#--Login view-->
def loginuser(request):
    if request.method == 'POST':

        username_entered = request.POST.get('username')
        password_entered = request.POST.get('password')

        user = authenticate(request,username = username_entered, password = password_entered)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,"username or password is incorrect...")
    context = {}
    return render(request,"login.html",context)

@login_required(login_url='login')
def problems(request):
    mydata = Problem.objects.all().values()
    mydata1=Problem.objects.values('topic').distinct()
    print(mydata1)
    data={
        'mydata':mydata,
        'mydata1':mydata1
    }
    return render(request,"problem.html",data)

def logoutuser(request):
    logout(request)
    return redirect('register')

@login_required(login_url='login')
def topics(request):
    mydata=Sources.objects.all().values()
    mydata1 = Sources.objects.values('topic').distinct()
    data={
        'mydata':mydata,
        'mydata1':mydata1
    }
    return render(request,"topics.html",data)

@login_required(login_url='login')
def discuss(request):
    return redirect('http://localhost:3000/')

def pfilter(request):
    mydata = Problem.objects.all().values()
    mydata1 = Problem.objects.values('topic').distinct()
    k=1
    d = []
    if(request.method == 'POST'):
        res_rate=request.POST.get("Rate",None)
        print(res_rate)
        if(res_rate==None):
            k=0
        for i in mydata:
            print(i)
            if(i['topic']==res_rate):
                d.append(i)
    if(k==1):
        data = {
            'mydata': d,
            'mydata1': mydata1
        }
        return render(request,"problem.html",data)
    data = {
        'mydata': mydata,
        'mydata1': mydata1
    }
    return render(request,"problem.html",data)

def tfilter(request):
    mydata = Sources.objects.all().values()
    mydata1 = Sources.objects.values('topic').distinct()
    k=1
    d = []
    if(request.method == 'POST'):
        res_rate=request.POST.get("Rate",None)
        print(res_rate)
        if(res_rate==None):
            k=0
        for i in mydata:
            print(i)
            if(i['topic']==res_rate):
                d.append(i)
    if(k==1):
        data = {
            'mydata': d,
            'mydata1': mydata1
        }
        return render(request,"topics.html",data)
    data = {
        'mydata': mydata,
        'mydata1': mydata1
    }
    return render(request,"topics.html",data)

@login_required(login_url='login')
def AddProblem(request):
    form_pre = Addproblem()
    if request.method == 'POST':
        form_pre = Addproblem(request.POST)
        if form_pre.is_valid():
            Problem.objects.create(**form_pre.cleaned_data)
            return redirect('problems')
        else:
            return redirect('problems')
    context = {'form': form_pre}
    return render(request, "AddProblem.html", context)

@login_required(login_url='login')
def AddTopic(request):
    form_pre = Addtopic()
    if request.method == 'POST':
        form_pre = Addtopic(request.POST)
        if form_pre.is_valid():
            Sources.objects.create(**form_pre.cleaned_data)
            return redirect('topics')
        else:
            return redirect('topics')
    context = {'form': form_pre}
    return render(request, "AddTopic.html", context)

@login_required(login_url='login')
def Resume(request):
    file_pat1 = os.path.join(os.path.dirname(__file__), 'text', 'queries.txt')
    file_pat2 = os.path.join(os.path.dirname(__file__), 'text', 'corpus.txt')
    print("File path:", file_pat1)
    print("File exists:", os.path.exists(file_pat1))
    qp = QueryParser(filename=file_pat1)
    cp = CorpusParser(filename=file_pat2)
    qp.parse()
    queries = qp.get_queries()
    cp.parse()
    corpus = cp.get_corpus()
    proc = QueryProcessor(queries, corpus)
    results = proc.run()
    data = []
    qid = 0
    for result in results:
        sorted_x = sorted(result.items(), key=operator.itemgetter(1))
        sorted_x.reverse()
        index = 0
        for i in sorted_x[:100]:
            tmp = (qid, i[0], index, i[1])
            data.append({
                'qid': tmp[0],
                'doc_id': tmp[1],
                'index': tmp[2],
                'score': tmp[3]
            })
            index += 1
        qid += 1
    context = {
        'result_data': data,
    }
    return render(request, 'Resume.html', context)

def upload_doc(request):
    if request.method == 'POST':
        form = UploadDocForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_doc=form.save()
            return redirect('parse_doc', pk=uploaded_doc.pk)
    else:
        form = UploadDocForm()
    return render(request, 'upload_doc.html', {'form': form})

# def parse_doc_view(request):
#     uploaded_docs = UploadedDoc.objects.all()
#     parsed_text = ""
#     p = 1
#     for doc in uploaded_docs:
#         resume = docx2txt.process(doc)
#         if p == 1:
#             file = open('C:\\Users\\Admin\\PycharmProjects\\BM25\\text\\corpus.txt', 'w')
#         else:
#             file = open('C:\\Users\\Admin\\PycharmProjects\\BM25\\text\\corpus.txt', 'a')
#         resume = func(resume)
#         resume = "#" + str(p) + "\n" + resume + "\n"
#         # job=func(job)
#         file.write(resume)
#         # file2.write(job)
#         file.close()
#         # file2.close()
#         p = p + 1
#     print(uploaded_docs)
#     return redirect('resume')
    # redirect('resume')


# def parse_doc_view(request):
#     uploaded_docs = UploadedDoc.objects.all()
#     corpus_file = 'C:\\Users\\Admin\\PycharmProjects\\BM25\\text\\corpus.txt'
#
#     with open(corpus_file, 'w') as file:
#         for p, doc in enumerate(uploaded_docs, start=1):
#             # Get the actual file content using doc.doc.read()
#             file_content = doc.doc.read()
#
#             # Process the file content
#             resume = docx2txt.process(file_content)
#             resume = func(resume)
#             resume = f"#{p}\n{resume}\n"
#             file.write(resume)
#
#     # Redirect to the 'resume' view after processing
#     return redirect('resume')

from django.http import HttpResponse


# def parse_doc_view(request):
#     uploaded_docs = UploadedDoc.objects.all()
#     corpus_file = 'C:\\Users\\Admin\\PycharmProjects\\BM25\\text\\corpus.txt'
#
#     with open(corpus_file, 'w') as file:
#         for p, doc in enumerate(uploaded_docs, start=1):
#             # Ensure that 'doc' is the actual 'UploadedFile' object
#             if doc.doc:
#                 # Seek to the beginning of the file (required for reading)
#                 doc.doc.seek(0)
#
#                 # Read and process the file content
#                 file_content = doc.doc.read()
#                 resume = docx2txt.process(file_content)
#                 resume = func(resume)
#                 resume = f"#{p}\n{resume}\n"
#                 file.write(resume)
#
#     # Redirect to the 'resume' view after processing
#     return redirect('resume')


def parse_doc_view(request, pk):
    uploaded_doc = UploadedDoc.objects.get(pk=pk)
    print("Hello")
    # if request.method == 'POST':
    doc_file = uploaded_doc.doc_file.path
    doc = docx.Document(doc_file)
    print("okdone")
    extracted_text = ''

    for paragraph in doc.paragraphs:
        extracted_text += paragraph.text + '\n'

    # Save extracted text to the database
    file_p = os.path.join(os.path.dirname(__file__), 'text', 'corpus.txt')
    extracted_text = func(extracted_text)

    uploaded_doc.extracted_text = extracted_text
    uploaded_doc.save()
    with open(file_p, 'a',  encoding='utf-8') as text_file:
        text_file.write("\n")
        doc_file_name = uploaded_doc.doc_file.name
        text_file.write("!!!!!" + f'{doc_file_name}')
        text_file.write("\n")
        text_file.write(extracted_text)
    # messages.success(request, 'Document successfully processed!')

    # Render the 'resume' template with the success message
    # return redirect(home, {'success_message': 'Document successfully processed!'});
    return render(request, 'index.html', {'success_message': 'Document successfully processed!'})
