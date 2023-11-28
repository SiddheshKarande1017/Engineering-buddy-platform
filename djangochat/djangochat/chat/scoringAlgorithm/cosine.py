import docx2txt
from sklearn.feature_extraction.text import CountVectorizer
import warnings
from sklearn.metrics.pairwise import cosine_similarity

warnings.filterwarnings('ignore')


def cosine_score(resume_list, job_list):
    resume = ' '.join(resume_list)
    job=' '.join(job_list)
    # print(job)
    # print(resume)
    #job = ' '.join(job_list)
    text = [resume, job]
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(text)
    matchpercentage = cosine_similarity(count_matrix)[0][1]
    matchpercentage = round(matchpercentage * 10000, 2)
    # print(matchpercentage)
    return matchpercentage
