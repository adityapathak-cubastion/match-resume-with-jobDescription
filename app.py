"""
hi, i'm a comment made by aditya pathak.
i'm here to help you understand the changes made to the code!

this script:
- calculates the cosine similarity and jaccard similarity between a job description and a set of resumes,
- integrates the two similarity scores to calculate a combined match score for each resume,
- returns the resume with the highest combined match score.

follow the comments to understand how it works!
"""

### IMPORTING LIBRARIES

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from typing import Dict
from get_resume_text import get_all_texts
import re, nltk

### DEFINING FUNCTIONS

## download NLTK stopwords if not already downloaded
# nltk.download('stopwords')

## load embedding model (high-dimensional model chosen for better accuracy)
model = SentenceTransformer('WhereIsAI/UAE-Large-V1')

## function to clean and tokenize the text
def clean_and_tokenize(text):
    """
    preprocess the text: remove non-alphanumeric characters, lowercasing, and tokenization
    """
    text = re.sub(r'\W', ' ', text.lower())

    words = text.split()

    stop_words = set(stopwords.words('english')).union(ENGLISH_STOP_WORDS)
    words = [word for word in words if word not in stop_words]
    
    return set(words)

## function to get the sentence embeddings
def get_embedding(text):
    """
    get the sentence embedding for a given text
    """
    return model.encode([text])

## function to calculate cosine similarity
def cosine_similarity_score(resume, jd_embedding):
    """
    compare resume and job description using cosine similarity;
    returns the cosine similarity score as a percentage
    """
    resume_embedding = get_embedding(resume)
    
    similarity_score = cosine_similarity(resume_embedding, jd_embedding)[0][0]
    
    return similarity_score * 100

## function to calculate jaccard similarity
def jaccard_similarity_score(resume, jd_tokens):
    """
    compare resume and job description using jaccard similarity;
    returns the jaccard similarity score as a percentage
    """
    resume_tokens = clean_and_tokenize(resume)
    
    intersection = resume_tokens.intersection(jd_tokens)
    union = resume_tokens.union(jd_tokens)
    
    jaccard_score = len(intersection) / len(union)
    
    return jaccard_score * 100

## function to integrate cosine and jaccard similarity with specified weights
def integrated_match_score(resume, jd_embedding, jd_tokens, weight_cosine = 0.6, weight_jaccard = 0.4):
    """
    integrates cosine similarity and jaccard similarity to calculate a combined match score;
    returns the final match percentage
    """
    cosine_score = cosine_similarity_score(resume, jd_embedding)
    jaccard_score = jaccard_similarity_score(resume, jd_tokens)

    combined_score = (cosine_score * weight_cosine) + (jaccard_score * weight_jaccard)
    
    scores: Dict[str, float] = {
        "cosine_score": '%.2f' % round(cosine_score, 2),
        "jaccard_score": '%.2f' % round(jaccard_score, 2),
        "combined_score": '%.2f' % round(combined_score, 2)
    } 

    return scores

### MAIN

## defining J.D.
j_d = """
Job Title: Front-End Developer

Location: Remote (or specify location if applicable)

Job Type: Full-Time

Job Description:
We are seeking a passionate and talented Front-End Developer to join our dynamic and collaborative team. As a Front-End Developer, you will play a critical role in building engaging, responsive, and visually appealing web applications for our clients. You’ll work closely with designers, back-end developers, and product managers to bring user-centric designs to life while ensuring the best performance and user experience.

This position is perfect for someone with strong skills in JavaScript and modern front-end frameworks like React.js and Angular, and a keen eye for creating clean, well-structured code that delivers smooth, intuitive user experiences.

Responsibilities:
Develop and maintain responsive, high-performance web applications using React.js (with a focus on functional components and hooks) and Angular.
Collaborate with UX/UI designers to translate visual designs into interactive web pages with attention to detail and user experience.
Write clean, maintainable code while adhering to best practices for web development (HTML5, CSS3, JavaScript ES6+).
Optimize applications for maximum speed and scalability across all devices and browsers.
Implement version control and manage project dependencies using Git.
Collaborate with back-end developers to integrate APIs and ensure seamless communication between front-end and back-end systems.
Participate in daily stand-ups, code reviews, and maintain a continuous learning mindset to stay up-to-date with the latest front-end technologies.
Contribute to the improvement of the development process, including the adoption of new tools, frameworks, and workflows.
Requirements:
4+ years of experience as a Front-End Developer or in a similar role.
Proficiency in React.js, Angular, JavaScript, HTML5, and CSS3.
Experience with front-end build tools such as Webpack, Babel, and npm.
Strong understanding of responsive design principles and cross-browser compatibility.
Familiarity with RESTful APIs and working with back-end teams to integrate data-driven features.
Experience with Git for version control.
Knowledge of CSS preprocessors like Sass or LESS is a plus.
Ability to write semantic, modular, and well-documented code.
Excellent communication skills and the ability to work effectively in an Agile, collaborative environment.
A keen eye for design and attention to detail to ensure an outstanding user experience.

Nice to Have:
Familiarity with TypeScript and modern JavaScript features.
Experience with UI frameworks like Material-UI or Bootstrap.
Basic understanding of SEO principles and web accessibility (WCAG).
Experience with Jest or other testing frameworks for front-end applications.
A portfolio showcasing previous web development projects (GitHub or personal website).
"""

## getting text from all resumes in 'resume' directory
dirPath, allTexts, allDocNames = "resumes", [], []
allTexts, allDocNames = get_all_texts(dirPath, allTexts, allDocNames)

## generating tokens and embeddings for J.D.
jd_embedding = model.encode([j_d])
jd_tokens = clean_and_tokenize(j_d)

all_scores: Dict[str, Dict[str, float]] = {}

## comparing each resume with the J.D. and storing the scores
for i, resume in enumerate(allTexts):
    # print(f"Resume Name: {allDocNames[i]}\nResume Text: {resume}\n") # to print all resumes
    scores = integrated_match_score(resume, jd_embedding, jd_tokens, weight_cosine = 0.92, weight_jaccard = 0.08)
    all_scores[allDocNames[i]] = scores

for resume in all_scores: # printing all scores
    print(f"Resume Name: {resume}\nCosine Score: {all_scores[resume]['cosine_score']}% | Jaccard Score: {all_scores[resume]['jaccard_score']}%\n\
Combined Score: {all_scores[resume]['combined_score']}%\n")

## returning the resume with the highest combined score
highest_scorer = max(all_scores, key = lambda x: all_scores[x]['combined_score'])
print(f"'{highest_scorer}' has the best matching resume, with a score of {all_scores[highest_scorer]['combined_score']}%!")



## Using the link below, specifically the heapnq method, we can find as many "best matching" resumes as we want.
# https://www.geeksforgeeks.org/python-program-to-find-second-largest-number-in-a-list/