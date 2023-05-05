"""
This module provides functions for working with PDF files and URLs. It uses the urllib.request library
to download files from URLs, and the fitz library to extract text from PDF files. And GPT3 modules to generate
text completions.
"""
import urllib.request
import fitz
import re
import numpy as np
import tensorflow_hub as hub
import os
from sklearn.neighbors import NearestNeighbors


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


def text_to_chunks(texts, word_length=150, start_page=1):
    text_toks = [t.split(' ') for t in texts]
    page_nums = []
    chunks = []

    for idx, words in enumerate(text_toks):
        for i in range(0, len(words), word_length):
            chunk = words[i:i + word_length]
            if (i + word_length) > len(words) and (len(chunk) < word_length) and (
                    len(text_toks) != (idx + 1)):
                text_toks[idx + 1] = chunk + text_toks[idx + 1]
                continue
            chunk = ' '.join(chunk).strip()
            chunk = f'[{idx + start_page}]' + ' ' + '"' + chunk + '"'
            chunks.append(chunk)
    return chunks


class SemanticSearch:

    def __init__(self):

        embedding = "https://tfhub.dev/google/universal-sentence-encoder/4"
        # "https://tfhub.dev/google/universal-sentence-encoder-multilingual/3"
        #embedding = "https://hub.tensorflow.google.cn/google/universal-sentence-encoder/4"

        self.use = hub.load(embedding)
        #self.use = tf.saved_model.load('./universal-sentence-encoder')
        self.fitted = False

    def fit(self, data, batch=1000, n_neighbors=5):
        self.data = data
        self.embeddings = self.get_text_embedding(data, batch=batch)
        n_neighbors = min(n_neighbors, len(self.embeddings))
        self.nn = NearestNeighbors(n_neighbors=n_neighbors)
        self.nn.fit(self.embeddings)
        self.fitted = True

    def __call__(self, text, return_data=True):
        inp_emb = self.use([text])
        neighbors = self.nn.kneighbors(inp_emb, return_distance=False)[0]

        if return_data:
            return [self.data[i] for i in neighbors]
        else:
            return neighbors

    def get_text_embedding(self, texts, batch=1000):
        embeddings = []
        for i in range(0, len(texts), batch):
            text_batch = texts[i:(i + batch)]
            emb_batch = self.use(text_batch)
            embeddings.append(emb_batch)
        embeddings = np.vstack(embeddings)
        return embeddings


def load_recommender(path, start_page=1):
    global recommender
    texts = pdf_to_text(path, start_page=start_page)
    print(texts)
    chunks = text_to_chunks(texts, start_page=start_page)
    recommender.fit(chunks)
    return 'Corpus Loaded.'


def generate_answer(question):
    topn_chunks = recommender(question)
    prompt = ""
    prompt += 'search results:\n\n'
    for c in topn_chunks:
        prompt += c + '\n\n'

    return prompt




# main to this

def question_answer(url, file, question):
    # if openAI_key.strip() == '':
    #     return '[ERROR]: Please enter you Open AI Key. Get your key here : https://platform.openai.com/account/api-keys'

    # if url.strip() == '' and file == None:
    #     return '[ERROR]: Both URL and PDF is empty. Provide atleast one.'

    # if url.strip() != '' and file != None:
    #     return '[ERROR]: Both URL and PDF is provided. Please provide only one (eiter URL or PDF).'

    if True:
        #glob_url = url
        #download_pdf(glob_url, 'corpus.pdf')
        #load_recommender('corpus.pdf')
        print('local file' + question + 'path=' + url)
        load_recommender(url)

    else:
        old_file_name = file.name
        print('upload file:' + old_file_name)
        file_name = file.name
        file_name = file_name[:-12] + file_name[-4:]
        os.remove(file_name)
        os.rename(old_file_name, file_name)
        load_recommender(file_name)

    if question.strip() == '':
        return '[ERROR]: Question field is empty'

    return generate_answer(question)


recommender = SemanticSearch()
