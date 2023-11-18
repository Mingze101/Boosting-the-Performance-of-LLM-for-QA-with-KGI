import PyPDF2
import os

def pdf_to_text(path):
    """将指定路径的PDF文件转换为文本。"""
    text = ""
    with open(path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text() + " "  # 添加空格替代换行符
    return text

def process_directory(directory):
    """处理指定目录下的所有PDF文件，将它们的内容合并为一个字符串。"""
    all_text = ""
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            path = os.path.join(directory, filename)
            all_text += pdf_to_text(path)
    return all_text

# 合并所有PDF文件的内容
def transferPDFtoStr(directory_paths):
    combined_text = ""
    for directory in directory_paths:
        combined_text += process_directory(directory)

    # 去除换行符
    combined_text = combined_text.replace('\n', ' ')

    return combined_text

#test
"""
# 指定目录路径
directory_paths = ["C:\\Users\\Li\\Desktop\\Praktikum Information Service Engineering (Master)\\Task2\\codes\\data\\pdf"]

#输出string
transferPDFtoStr=transferPDFtoStr(directory_paths)
print(transferPDFtoStr)
"""



