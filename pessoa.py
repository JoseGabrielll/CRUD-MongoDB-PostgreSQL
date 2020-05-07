class Pessoa:
    def __init__(self, nome, idade, cpf, id_pessoa=None):
        self.__nome = nome
        self.__idade = idade
        self.__cpf = cpf
        self.id_pessoa = id_pessoa

    #Métodos get:
    @property
    def nome(self):
        return self.__nome
    
    @property
    def idade(self):
        return self.__idade
    
    @property
    def cpf(self):
        return self.__cpf

    #Métodos set:
    @nome.setter
    def nome(self, valor):
        self.__nome = valor.title() #padrão Xxxxxxxx

    @idade.setter
    def idade(self, valor):
        self.__idade = valor
    
    @cpf.setter
    def cpf(self, valor):
        self.__cpf = valor



