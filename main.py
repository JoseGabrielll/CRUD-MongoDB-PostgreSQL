from pessoa import Pessoa
from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
import psycopg2

#Criando conexão com MongoDB:
client = MongoClient('localhost', 27017) #host e porta
db = client.get_database('pessoasdb')
collection = db.get_collection('pessoas')

#Criando conexão com Postgres:
conn = psycopg2.connect(host='localhost', database='flask1', 
                        user='postgres', password='senha070202')
cur = conn.cursor()
'''
#Criando uma tabela com Postgres que vai possuir (id, nome, idade, cpf):
cur.execute(
    "CREATE TABLE pessoas(id serial PRIMARY KEY, nome varchar(255), idade integer, cpf char(11));"
    )   
'''

'''
#Criando alguns dados no mongoDB
p1 = Pessoa('Mario', '32', '651651561')
p2 = Pessoa('renata', '21', '984632131')

data = [
    {
        'nome': p1.nome,
        'idade': p1.idade,
        'cpf': p1.cpf
    },
    {
        'nome': p2.nome,
        'idade': p2.idade,
        'cpf': p2.cpf
    }
]
collection.insert(data)
'''
'''
#Criando dados no Postgres 2 formas diferentes:
cur.execute("INSERT INTO pessoas (nome, idade, cpf) VALUES (%s, %s, %s)", ('Felipe', 34, 34199098114))
cur.execute("INSERT INTO pessoas (nome, idade, cpf) VALUES ('Rodrigo', 20, 12345678932)")
conn.commit()
'''

app = Flask(__name__)

def ListarPessoas(): #Lista pessoas do mongoDB
    lista_pessoas = []

    for pessoa in collection.find():
        nome = pessoa.get('nome') 
        idade = pessoa.get('idade')
        cpf = pessoa.get('cpf')
        id_pessoa = pessoa.get('_id')

        p_atual = Pessoa(nome, idade, cpf, id_pessoa)
        lista_pessoas.append(p_atual)
        
    return lista_pessoas 

def ListarPessoas2(): #Lista pessoas do postgres
    lista_pessoas2 = []
    cur.execute("SELECT * FROM pessoas;")
    pessoas = cur.fetchall()

    for pessoa in pessoas:
        id_pessoa = pessoa[0]
        nome = pessoa[1]
        idade = pessoa[2]
        cpf = pessoa[3]

        p_atual = Pessoa(nome, idade, cpf, id_pessoa)
        lista_pessoas2.append(p_atual)  

    return lista_pessoas2

@app.route('/')
def index():
    return render_template('index.html', titulo = 'Bem vindo ao banco de dados de pessoas')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/lista')
def lista():
    #chamar lista de pessoas do banco de dados  
    lista_pessoas = ListarPessoas() #Lista de pessoas do MongoDB
    lista_pessoas2 = ListarPessoas2() #Lista de pessoas Postgres
    return render_template('lista.html', titulo = 'Lista de pessoas', pessoas = lista_pessoas, pessoas2 = lista_pessoas2)

@app.route('/novo')
def novo():
    return render_template('novo.html', titulo = 'Novo cadastro')

@app.route('/criar', methods=['POST',])
def criar():
    #recebo os dados do formulário
    nome = request.form['nome']
    idade = request.form['idade']
    cpf = request.form['cpf']

    #crio o objeto pessoa
    nova_pessoa = Pessoa(nome, idade, cpf)
    
    #passo para uma variável 
    data = {
        'nome': nova_pessoa.nome,
        'idade': nova_pessoa.idade,
        'cpf': nova_pessoa.cpf
    }
    #adiciono no banco de dados MongoDB
    collection.insert(data)

    #Inserindo pessoa no PostgreSQL:
    cur.execute("INSERT INTO pessoas (nome, idade, cpf) VALUES (%s, %s, %s)", (nova_pessoa.nome, nova_pessoa.idade, nova_pessoa.cpf))
    conn.commit()

    
    return redirect(url_for('index'))

@app.route('/deleta')
def deleta():
    #exibe a lista de pessoas e pergunta qual quer deletar pelo id
    lista_pessoas = ListarPessoas()
    lista_pessoas2 = ListarPessoas2() #Lista de pessoas Postgres
    return render_template('deleta.html', titulo = 'Deletar Usuário', pessoas = lista_pessoas, pessoas2 = lista_pessoas2)

@app.route('/auth_delete', methods=['POST',])
def auth_delete():
    cpf_pessoa = request.form['cpf_pessoa']
    collection.remove(
        {'cpf' : cpf_pessoa} 
    )
    return redirect(url_for('lista'))


@app.route('/atualiza')
def atualiza():
    #exibe a lista de pessoas e pergunta qual quer atualizar pelo
    lista_pessoas = ListarPessoas() 
    lista_pessoas2 = ListarPessoas2() #Lista de pessoas Postgres
    return render_template('atualiza.html', titulo = 'Atualizar Usuário', pessoas = lista_pessoas, pessoas2 = lista_pessoas2)

@app.route('/auth_atualiza', methods=['POST',])
def auth_atualiza():
    cpf_pessoa = request.form['cpf_pessoa']
    nome_pessoa = request.form['nome_pessoa']
    idade_pessoa = request.form['idade_pessoa']

    collection.update(
        {'cpf': cpf_pessoa},
        {'$set': 
            {
            'nome': nome_pessoa,
            'idade': idade_pessoa
            }
        }
    )

    return redirect(url_for('lista'))

def main():
    app.run(host='0.0.0.0', port=8080)
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()