# Boosting the Performance of Large Language Models for Question Answering with Knowledge Graph Integration
Praktikum Information Service Engineering (Master)
Task 2 members: Haoran Yang, Mingze Li, Zhaotai Liu. 

Supervisors: Mirza Mohtashim Alam, Ebrahim Norouzi, Genet Asefa Gesese.

RAG and OpenAI’s Function-Calling for Question-Answering with Langchain.py uploaded by Mingze:
 Fixed bug: model result returns error solved. It can directly return the context that we want not the full response of model.
 Encapsulation: user only need one methord: get_answer_LLM(question: str, data: str, chunk_size: int = 1000) -> str 
 Hit: remove all commens to speed up.
