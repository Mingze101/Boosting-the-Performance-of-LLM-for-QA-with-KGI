# Boosting the Performance of Large Language Models for Question Answering with Knowledge Graph Integration
Praktikum Information Service Engineering (Master)
Task 2 members: Haoran Yang, Mingze Li, Zhaotai Liu. 

Supervisors: Mirza Mohtashim Alam, Ebrahim Norouzi, Genet Asefa Gesese.

There are three files: RAG_GPT3_5, transfer_PDF_to_str, and main. The main file integrates questions, queries, and a string converted from a PDF by transfer_PDF_to_str, and feeds them into the RAG model based on GPT-3.5, which is implemented in RAG_GPT3_5.

RAG before interim report has uploaded: RAG_GPT3_5.py

This code is mainly used to extract relevant information from large amounts of text data to answer a series of questions. First, it uses regular expressions and sorting logic to split the raw data into smaller chunks of text. Then, a SentenceTransformer is utilized to generate embedding representations of these text blocks, and the faiss library is used to create an index for fast similarity searches. Next, the program retrieves the text blocks most relevant to the query given the query and the created knowledge base. Finally, these relevant chunks of text are used as context for the OpenAI GPT-3.5 model to generate answers to a series of questions. The code also includes the necessary library imports and configurations, as well as the definition of some functions for processing text blocks, creating knowledge bases, retrieving related text blocks, and generating answers using the GPT-3.5 model.
