import os
import sys
from functools import partial
from typing import List, Optional

import cv2
from pdf2image import convert_from_path
import typer
import numpy as np
import nltk, string
import pytesseract
from nltk.corpus import stopwords
from pyaspeller import YandexSpeller
from PIL import Image

# Histogram threshold
THRESHOLD = 0.07
# Longest common subsequence fraction threshold
LCS_THRESHOLD = 1 / 3

# Helper function to remove punctuation
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

# Yandex speller
speller = YandexSpeller()
# Russian stop words (might be long to download for the first time)
nltk.download("stopwords")
stop_words = set(stopwords.words('russian'))


def fix_misspelling(text):
    """
    Uses Yaspeller to correct grammar
    :param text: Text with possible misspellings (recognition errors)
    :return: Fixed text
    """
    if not text.strip():
        return text
    changes = {change['word']: change['s'][0] for change in speller.spell(text) if change['s']}
    for word, suggestion in changes.items():
        text = text.replace(word, suggestion)
    return text


def normalize(text):
    """
    Text normalizer and splitter
    :param text: Raw text
    :return: Text splitted into words, lowercased with stop words and punctuation removed
    """
    return [w for w in nltk.word_tokenize(text.lower().translate(remove_punctuation_map)) if w not in stop_words]


def extract_text(doc):
    """
    TODO: speed-up
    Slow function since very general. There's a lot of space for improvements
    :param doc: RGB image or path
    :return: Text from the document
    """
    return fix_misspelling(pytesseract.image_to_string(doc, lang='rus'))


def preprocess(doc):
    """
    Converts BGR image to list of hashed words
    :param doc: BGR cv2 image, np array
    :return: Hashed words found in the document
    """
    doc = cv2.cvtColor(doc, cv2.COLOR_BGR2RGB)
    doc = Image.fromarray(doc)
    return list(map(hash, normalize(extract_text(doc))))


def lcs_similarity(seq1, seq2):
    """
    LCS similarity metrics
    :param seq1: Array of words
    :param seq2: Array of words
    :return: LCS(seq1, seq2) / max(len(seq1), len(seq2))
    """
    lengths = np.zeros((len(seq1) + 1, len(seq2) + 1), dtype=np.int)

    # row 0 and column 0 are initialized to 0 already
    for i, char1 in enumerate(seq1):
        for j, char2 in enumerate(seq2):
            if char1 == char2:
                lengths[i + 1][j + 1] = lengths[i][j] + 1
            else:
                lengths[i + 1][j + 1] = max(lengths[i + 1][j], lengths[i][j + 1])

    return lengths[len(seq1)][len(seq2)] / max(len(seq1), len(seq2))


def read_document(path):
    """
    Reads PDF(if pdf2image is successfully configured, might be unstable) and image files
    :param path: PDF or image path
    :return: cv2 BGR array
    """
    if path.endswith(".pdf"):
        img = convert_from_path(path)[0]
        img = np.array(img)
    else:
        img = cv2.imread(path)

    return img


def is_doc(img):
    """
    Quick histogram check
    :param img: cv2 array
    :return: where a given images is a document or not
    """
    divisor = img.shape[0] * img.shape[1]

    min_vals = img.min(axis=-1, keepdims=True)
    new_image = img - min_vals

    return (np.linalg.norm(new_image) / divisor) < THRESHOLD


def is_similar(doc1, doc2):
    """
    :param doc1: Preprocessed list of words
    :param doc2: Preprocessed list of words
    :return: Whether similarity of doc1 and doc2 meets threshold or not
    """
    return lcs_similarity(doc1, doc2) >= LCS_THRESHOLD


def main(template: str, path: str):
    """
    CLI script to check if a given document is like template
    :param template: Path to a template or directory to check every template
    :param path: Path to a test doc or directory for mass run
    """
    if os.path.isdir(template):
        templates = map(partial(os.path.join, template), os.listdir(template))
    else:
        templates = [template]

    true_docs = [read_document(template) for template in templates]
    true_docs_processed = [preprocess(true_doc) for true_doc in true_docs]

    if os.path.isdir(path):
        for doc_path in os.listdir(path):
            doc_path = os.path.join(path, doc_path)
            doc = read_document(doc_path)
            ok = is_doc(doc) and any(
                is_similar(true_doc_processed, preprocess(doc)) for true_doc_processed in true_docs_processed
            )
            print(doc_path, "-", "ok" if ok else "no")
    else:
        doc = read_document(path)
        if is_doc(doc) and any(
                is_similar(true_doc_processed, preprocess(doc)) for true_doc_processed in true_docs_processed
        ):
            print("ok")


if __name__ == '__main__':
    typer.run(main)
