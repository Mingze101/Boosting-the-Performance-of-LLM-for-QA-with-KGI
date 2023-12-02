"""
此为4.2版本
-1.先将代码去冗余例如重复加载文件重复声明路径
0.entities数量为2657,但是输出到文件的entities数量为1824，原因在于Iterate over the graph中并没有使用objects只有subjects（不明白为什么要这样因此先保留，有可能是-1这一步的问题）

#下面全是基于entities数量为1824的操作，应该不会影响实际的数量
1.通过python脚本发现所有包含uri的triple都在tail entity中表明了数据类型^^xsd:anyURI（数量为509），因此对于生成的“entity_label_description.xlsx”文件我看可以直接在description上写明：“URI=”
2.对于http://purl.obolibrary.org/obo/的实体，他们的matwerk的实体并没有对应的description而是Definition. 
3.大多数description值为NaN（数量为984），例如来自http://demo.fiz-karlsruhe.de/matwerk的实体并没有对应的description，这意味我们需要在网上检索，下面探讨可能性：
    4.0通过脚本添加，还剩570个值为NaN的赋值为“No results found”
    4.1通过检索label手动添加description
    4.2对于无法通过脚本检索获取description的entity，只能将label的值赋给description的值。
This is version 4.2
-1. First remove redundancy from the code, such as loading files repeatedly and declaring paths repeatedly.
0.The number of entities is 2657, but the number of entities output to the file is 1824. The reason is that objects are
not used in Iterate over the graph, only subjects
(I don’t understand why this is done, so I keep it first. It may be a problem with the -1 step)

#The following are all operations based on the number of entities being 1824, which should not affect the actual number.
1. Through the python script, it is found that all triples containing uri indicate
the data type ^^xsd:anyURI (the number is 509) in the tail entity.
Therefore, I think that the generated "entity_label_description.xlsx" file can be written directly on the description. :"URI="
2. For the entities of http://purl.obolibrary.org/obo/,
their matwerk entities do not have corresponding descriptions but Definitions.
3. Most description values are NaN (the number is 984).
For example, the entity from http://demo.fiz-karlsruhe.de/matwerk does not have a corresponding description,
which means that we need to search online. Let’s explore the possibilities below:
     4.0 was added through script, and there are still 570 values
     that are NaN and assigned the value "No results found"
     4.1 Manually add description by retrieving label
     4.2 For entities whose description cannot be obtained through script retrieval,
     the value of label can only be assigned to the value of description.
"""
# Path to the RDF file (Turtle format)
import pandas as pd
import rdflib

# Path to the RDF file (Turtle format)
file_path = r"C:\Users\Li\PycharmProjects\pythonProject\venv\inputData\output.ttl"
excel_file_path = r"C:\Users\Li\PycharmProjects\pythonProject\venv\inputData\entity_label_description.xlsx"

# Create a new RDF graph
g = rdflib.Graph()

# Parse the RDF file
g.parse(file_path, format='turtle')

# Initialize data structures
entities = set()
label_dict = {}
descriptions = {}

description_info_set = {
    rdflib.URIRef("http://purls.helmholtz-metadaten.de/mwo/description"),
    rdflib.URIRef("http://www.w3.org/2000/01/rdf-schema#comment"),
    rdflib.URIRef("http://purl.obolibrary.org/obo/IAO_0000115")
}

# Iterate over the graph
for subject, predicate, obj in g:
    if isinstance(subject, rdflib.URIRef):
        entities.add(subject)
    if isinstance(obj, rdflib.URIRef):#scan objects
        entities.add(obj)
    if predicate == rdflib.RDFS.label or predicate == rdflib.URIRef("http://purl.org/dc/terms/title"):
        label_dict[subject] = str(obj)
    if predicate in description_info_set:
        descriptions[subject] = str(obj)
    if isinstance(obj, rdflib.Literal) and obj.datatype == rdflib.URIRef("http://www.w3.org/2001/XMLSchema#anyURI"):#handel uro description
        if subject in descriptions:
            descriptions[subject] += " | URI: " + str(obj)
        else:
            descriptions[subject] = "URI: " + str(obj)
"""
# Preparing data for DataFrame
data = []
for entity in entities:
    label = label_dict.get(entity, str(entity))
    description = descriptions.get(entity, label)  # Update: Use label if description is 'NaN'
    data.append([str(entity), label, description])

# Create DataFrame
df = pd.DataFrame(data, columns=['Entity', 'Label', 'Description'])

"""
data = []
for entity in entities:
    label = label_dict.get(entity, str(entity))
    description = descriptions.get(entity)  # Do not use label if description is not available
    data.append([str(entity), label, description if description is not None else 'NaN'])  # Use 'NaN' if description is missing

# Create DataFrame
df = pd.DataFrame(data, columns=['Entity', 'Label', 'Description'])
# Save to Excel
df.to_excel(excel_file_path, index=False)

print("Number of entities:", df.shape[0])
