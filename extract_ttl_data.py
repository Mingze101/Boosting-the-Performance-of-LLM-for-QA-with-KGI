from rdflib import Graph

def extract_ttl_data(file_path):
    """
    从指定的 .ttl 文件中提取数据，并返回 entities, relations 和 triples 的字符串表示。

    :param file_path: .ttl 文件的路径
    :return: entities_str, relations_str, triples_str
    """
    # 创建一个 RDF Graph
    g = Graph()

    # 解析 .ttl 文件
    g.parse(file_path, format="turtle", encoding='utf-8')

    # 初始化 sets 来存储唯一的实体和关系
    entities = set()
    relations = set()

    # 初始化列表来存储 triples
    triples_list = []

    # 遍历图中的所有三元组
    for s, p, o in g:
        triples_list.append((s, p, o))
        entities.add(s)
        entities.add(o)
        relations.add(p)

    # 转换 entities 和 relations 为字符串
    entities_str = ', '.join(str(e) for e in entities)
    relations_str = ', '.join(str(r) for r in relations)

    # 转换 triples_list 为字符串
    triples_str = '; '.join(f'({s}, {p}, {o})' for s, p, o in triples_list)

    return entities_str, relations_str, triples_str

import csv

def write_to_csv(data, file_path):
    """
    将数据写入指定路径的 CSV 文件，并确保使用 UTF-8 编码。
    :param data: 要写入的数据列表。
    :param file_path: CSV 文件的完整路径。
    """
    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for item in data:
            writer.writerow([item])

def extract_and_write_ttl_data(ttl_file_path, entities_csv_path, relations_csv_path, triples_csv_path):
    entities_str, relations_str, triples_str = extract_ttl_data(ttl_file_path)

    # 将字符串转换为列表
    entities_list = entities_str.split(', ')
    relations_list = relations_str.split(', ')
    triples_list = triples_str.split('; ')

    # 写入指定路径的 CSV 文件
    write_to_csv(entities_list, entities_csv_path)
    write_to_csv(relations_list, relations_csv_path)
    write_to_csv(triples_list, triples_csv_path)
def read_csv(file_path):
    """
    从指定路径读取 CSV 文件，并返回其中的数据。
    :param file_path: CSV 文件的路径。
    :return: 文件中的数据，每行作为列表的一个元素。
    """
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    return data
# Scanner
file_path = r"C:\Users\Li\PycharmProjects\pythonProject\venv\data\output.ttl"
entities_str, relations_str, triples_str = extract_ttl_data(file_path)
print("Entities:", entities_str)
print("Relations:", relations_str)
print("Triples:", triples_str)

#csv generater
folder_entities_path = r"C:\Users\Li\PycharmProjects\pythonProject\venv\data\entities.csv"
folder_relations_path = r"C:\Users\Li\PycharmProjects\pythonProject\venv\data\relations.csv"
folder_triples_path = r"C:\Users\Li\PycharmProjects\pythonProject\venv\data\triples.csv"
extract_and_write_ttl_data(
    file_path,
    folder_entities_path,
    folder_relations_path,
    folder_triples_path
)
#note: ensure that no csv files named by relations, relations and triples in the path



# 示例调用
csv_data = read_csv(folder_entities_path)
for row in csv_data:
    print(row)
