import datetime
import pprint

import pymongo as pyM

client = pyM.MongoClient("mongodb+srv://rclaranjeira:R5WOnrRqJzJljLoR@cluster0.matzfrl.mongodb.net/?retryWrites=true&w=majority")

db = client.test
collection = db.test_collection
print(db.test_collection)

# definição de infor para compor o doc
cliente = {
    "nome": "Lucas",
    "cpf": "111.111.111-11",
    "endereco": "Rua Leandro Marques, 458",
    "conta": {"tipo": "CC", "agencia": "7852-5", "numero": "5844", "saldo": "1254.32"}}

# preparando para submeter as infos
clientes = db.clientes
cliente_id = clientes.insert_one(cliente).inserted_id
print(f"ID -> {cliente_id}")

# print(db.clientes.find_one())
pprint.pprint(db.clientes.find_one())

# multi inserts
new_clientes = [{
            "nome": "Jorge",
            "cpf": "222.222.222-2",
            "endereco": "Rua Paes Lemes, 69",
            "conta": {"tipo": "CC", "agencia": "9265-5", "numero": "6587", "saldo": "1500.02"}},
            {
            "nome": "Mateus",
            "cpf": "333.333.333-33",
            "endereco": "Rua Jorge Sa, 245",
            "conta": {"tipo": "CC", "agencia": "4582-5", "numero": "3254", "saldo": "2514.32"}}]

result = clientes.insert_many(new_clientes)
print(f"IDs -> {result.inserted_ids}")

print("\nRecuperação final")
pprint.pprint(db.clientes.find_one({"nome": "Lucas"}))

print("\n Documentos presentes na coleção posts")
for cliente in clientes.find():
    pprint.pprint(cliente)
