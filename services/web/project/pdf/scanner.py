"""
This module provides functions for working with PDF files and URLs. It uses the urllib.request library
to download files from URLs, and the fitz library to extract text from PDF files. And GPT3 modules to generate
text completions.
"""
import urllib.request
import fitz
import re


def download_pdf(url, output_path):
    urllib.request.urlretrieve(url, output_path)


def preprocess(text):
    text = text.replace('\n', ' ')
    text = re.sub('\s+', ' ', text)
    return text


def pdf_to_text(path, start_page=1, end_page=None):
    doc = fitz.open(path)
    total_pages = doc.page_count

    if end_page is None:
        end_page = total_pages

    text_list = []

    for i in range(start_page - 1, end_page):
        text = doc.load_page(i).get_text("text")
        text = preprocess(text)
        text_list.append(text)

    doc.close()
    return text_list



def load_recommender(path, start_page=1):
    texts = pdf_to_text(path, start_page=start_page)
    print(texts)
    return texts

# a = load_recommender('C:\\Users\\Rouse\\Documents\\WeChat Files\\luosi411848\\FileStorage\\File\\2023-04\\1.二十大报告（文字实录）.pdf')
# print(a)