import sys
import cv2
import numpy as np
from pdf2image import convert_from_bytes

import typer

THRESHOLD = 0.07
IOU_THRESHOLD = 0.75
BLACK_THRESHOLD = 30


def read_document(path):
    if path.endswith(".pdf"):
        img = convert_from_bytes(open(path).read())[0]
        img = np.array(img)
    else:
        img = cv2.imread(path)

    return img


def is_doc(img):
    divisor = img.shape[0] * img.shape[1]

    min_vals = img.min(axis=-1, keepdims=True)
    new_image = img - min_vals

    return (np.linalg.norm(new_image) / divisor) < THRESHOLD


def get_printed_boxes(img):
    kernel = np.ones((5, 5), np.uint8)
    black_mask = img.max(axis=-1, keepdims=True) <= BLACK_THRESHOLD
    printed_text = cv2.dilate((black_mask * 255).astype(np.uint8), kernel, iterations=3)
    return printed_text


def iou(img1, img2):
    shape = (min(img1.shape[0], img2.shape[0]), min(img1.shape[1], img2.shape[1]))
    img1 = cv2.resize(img1, shape)
    img2 = cv2.resize(img2, shape)
    return np.logical_and(img1, img2).sum() / np.logical_or(img1, img2).sum()


def is_alike(doc1, doc2):
    doc1 = get_printed_boxes(doc1)
    doc2 = get_printed_boxes(doc2)

    cv2.imwrite("doc1.jpg", doc1)
    cv2.imwrite("doc2.jpg", doc2)
    print(iou(doc1, doc2))

    return iou(doc1, doc2) >= IOU_THRESHOLD


def main(path: str, template: str= None):
    doc = read_document(path)
    # Yet unused
    # true_doc = read_document(template)

    if not is_doc(doc):
        sys.exit(0)
    # TBA
    # if not is_alike(doc, true_doc):
    #     sys.exit(0)

    print("ok")


if __name__ == '__main__':
    typer.run(main)
