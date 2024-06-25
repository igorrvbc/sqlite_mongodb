"""
- - - DESAFIO MONGODB DIO - - -
"""
import datetime
import pprint
import pymongo as pym


# Criando a conexão com o banco de dados
client = pym.MongoClient("mongodb+srv:"
                         "//igorrvbc:<password>@cluster0.ogahb9h.mongodb.net/"
                         "?retryWrites=true&w=majority&appName=Cluster0")

db = client.test
collection = db.test_collection

# Retornando infos sobre o banco teste
pprint.pprint(db.test_collection)

# Definição de infos para compor o doc
# Atributos
cliente = [{
    "tipo": "conta_corrente",
    "agencia": "brbr",
    "numero": "000000000001",
    "cliente": {
        "nome": "Mike",
        "cpf": "0000111",
        "endereco": "Anyplace"
    },
    "tags": ["cc", "cliente"],
    "date": datetime.datetime.now(datetime.UTC)
}, {
    "tipo": "conta_corrente",
    "agencia": "brbr",
    "numero": "000000000001",
    "cliente": {
        "nome": "Tyson",
        "cpf": "0000222",
        "endereco": "galaxy6"
    },
    "tags": ["cc", "vip", "cliente"],
    "date": datetime.datetime.now(datetime.UTC)
}, {
    "tipo": "conta_corrente",
    "agencia": "brbr",
    "numero": "000000000001",
    "cliente": {
        "nome": "Xyz",
        "cpf": "0000003",
        "endereco": "dimension7"
    },
    "tags": ["cp", "cliente"],
    "date": datetime.datetime.now(datetime.UTC)
}]

# Preparando para submeter as infos:
clientes = db.bank

# Inserindo os documentos no banco de dados
result = clientes.insert_many(cliente)
print("\nRecuperando os ids criados:")
pprint.pprint(result.inserted_ids)

# Recuperando dados...
# Infos pelo nome:
print("\nRecuperando infos:")
pprint.pprint(db.clientes.find_one({"nome": "Tyson"}))

# Número de docs correspondentes:
print("\nNumero de clientes com um nome especifico:")
print(clientes.count_documents({"nome": "Tyson"}))

print("\nNumero de clientes com um tipo de conta por tag:")
print(clientes.count_documents({"tags": "cc"}))

# Listando coleções do banco
print("\nNome das coleções presentes no BD:")
print(db.list_collection_names())
print("\n")
pprint.pprint(db.clientes.find_one({"conta": "conta_corrente"}))

# Recuperando todos os documentos em Clientes
print("\nDocumentos presentes na coleção bank")
for cliente in clientes.find():
    pprint.pprint(cliente)
    print("\n")

# Ordenando busca por data
print("\nRecuperando info da coleção bank de maneira ordenada")
for cliente in clientes.find({}).sort("date"):
    pprint.pprint(cliente)
