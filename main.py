import transfer_PDF_to_str
import RAG_GPT3_5

import PyPDF2
import os

import PyPDF2
from pdf2image import convert_from_path
import pytesseract
import numpy as np
#pip install PyPDF2 pdf2image pytesseract numpy

from textsplitter import TextSplitter
#pip install textsplitter

from langchain.text_splitter import CharacterTextSplitter
#pip install langchain
#from openai.embeddings_utils import get_embedding

from sentence_transformers import SentenceTransformer#pip install sentence_transformers

import faiss

import os
from openai import OpenAI
import openai

# 指定目录路径
directory_paths = ["C:\\Users\\Li\\Desktop\\Praktikum Information Service Engineering (Master)\\Task2\\codes\\data\\pdf"]


def main():
    # 输出string
    data = transfer_PDF_to_str.transferPDFtoStr(directory_paths)  # data
    print("data:", data)
    query = " LLM RAG"  # query
    question = "how could we build a RAG based on LLM"  # question

    result = RAG_GPT3_5.get_answer_LLM(question,query, data, 1024)  # result from the model
    print("result:", result)  # ['result']

if __name__ == "__main__":
    main()