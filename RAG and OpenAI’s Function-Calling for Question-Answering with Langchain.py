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

api_key = os.environ.get('OPENAI_API_KEY')  # Replace 'OPENAI_API_KEY' with the name of your environment variable

client = OpenAI(api_key=api_key)

#将从pdf获得的data分割成更小的chunks
def get_data_chunks(data: str, chunk_size: int):#Splitting text into smaller
    text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=5, separator="\n", length_function=len)
    chunks = text_splitter.split_text(data)
    return chunks

#创建knowledge hub 或者 database
def create_knowledge_hub(chunks: list): #Creating the knowledge hub or database
    model = SentenceTransformer('all-MiniLM-L6-v2')  # Example model, you can choose others
    embeddings = model.encode(chunks, show_progress_bar=True)
    index = faiss.IndexFlatL2(embeddings.shape[1])  # L2 distance for similarity
    index.add(np.array(embeddings).astype('float32'))  # Add embeddings to index
    return index

def retrieve_relevant_chunks(query, index, chunks, k=2):#bigger context
    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_embedding = model.encode([query])[0]
    distances, indices = index.search(np.array([query_embedding]).astype('float32'), k)
    relevant_chunks = [chunks[i] for i in indices[0]]
    return relevant_chunks
# Then use these chunks with your language model for generating answers.

#使用 QA chain进行信息检索#Using Q&A chain for information retrieval
def get_answer_LLM(question: str, data: str, chunk_size: int = 1000) -> str:
    if data == "":
        return ""
    # 创建文本块
    chunks = get_data_chunks(data, chunk_size=chunk_size)
    # 创建知识库
    knowledge_hub = create_knowledge_hub(chunks)
    # 检索相关块
    relevant_chunks = retrieve_relevant_chunks(question, knowledge_hub, chunks, k=2)
    # 将相关块组合成单一上下文
    context = ' '.join(relevant_chunks)
    # 初始化 generated_text
    generated_text = "没有生成的文本。"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": context + " " + question}
        ]
    )
    if response.choices:
        first_choice = response.choices[0]
        generated_text = first_choice.message  # 假设文本位于 'content' 键中
        print("context: ",context)
        print("response: ",response)
    return generated_text

#test all
data="""
We endow pre-trained, parametric-memory generation models with a non-parametric memory through a general-purpose fine-tuning approach which we refer to as retrieval-augmented generation (RAG). 
We build RAG models where the parametric memory is a pre-trained seq2seq transformer, and the non-parametric memory is a dense vector index of Wikipedia, accessed with a pre-trained neural retriever. 
We combine these components in a probabilistic model trained end-to-end (Fig. 1). 
The retriever DPR (Dense Passage Retriever [26], henceforth DPR) provides latent documents conditioned on the input, and the seq2seq model (BART [32]) then conditions on these latent documents together with the input to generate the output. 
We marginalize the latent documents with a top-K approximation, either on a per-output basis (assuming the same document is responsible for all tokens) or a per-token basis (where different documents are responsible for different tokens). 
Like T5 [51] or BART, RAG can be fine-tuned on any seq2seq task, whereby both the generator and retriever are jointly learned.
"""
print("data: ",data)
#成功验证get_data_chunks
chunks = get_data_chunks(data,300)#max averages of char.
print(chunks)

#成功验证create_knowledge_hub
index = create_knowledge_hub(chunks)
print("index",index)

#验证retrieve_relevant_chunks
query = "what is RAG"
relevant_chunks = retrieve_relevant_chunks(query, index, chunks, k=2)
print("relevant_chunks: ",relevant_chunks)
'''for chunk in relevant_chunks:
    print(chunk)
'''
# 测试get_answer_LLM（确保已正确设置data变量）成功
question = "which problem can RAG solve?"
result = get_answer_LLM(question, data, 5)
print("result:", result['result'])

#mistral 7b
#zephyr 7b
#entities , mach entities, push them into the query

#rdf lib, turtle file
#Play with chunking with bigger context size, probably texts from a document (i.e, pdf).
#Play with the knowledge graph which will be uploaded later today (i.e, in the evening). Try to find the entities and relation.
#Try to find if the information of the entities are available
#BLEU, ROGUE, METEOR (these are the evaluation metrics used in literature)