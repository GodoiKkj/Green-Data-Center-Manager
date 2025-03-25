from sortedcontainers import SortedDict

class DicionarioOrdenado:
    """
    Classe que encapsula o comportamento de um SortedDict para facilitar
    a manipulação de um dicionário ordenado. Usa a estrutura de dados 
    SortedDict da biblioteca 'sortedcontainers'.
    """
    
    def __init__(self):
        """
        Inicializa o dicionário ordenado vazio.
        
        Complexidade: O(1)
        """
        self.data = SortedDict()

    def inserir(self, chave, valor):
        """
        Insere um novo par chave-valor no dicionário ordenado.
        
        Parâmetros:
        chave (str): A chave a ser inserida no dicionário.
        valor (int): O valor associado à chave.
        
        Complexidade: O(log N)
        """
        self.data[chave] = valor

    def buscar(self, chave):
        """
        Retorna o valor associado à chave fornecida.
        
        Parâmetros:
        chave (str): A chave para buscar no dicionário.
        
        Retorna:
        int: O valor associado à chave.
        
        Complexidade: O(log N)
        """
        return self.data[chave]

    def existe(self, chave):
        """
        Verifica se a chave existe no dicionário.
        
        Parâmetros:
        chave (str): A chave a ser verificada.
        
        Retorna:
        bool: True se a chave existir, False caso contrário.
        
        Complexidade: O(log N)
        """
        return chave in self.data

    def remover(self, chave):
        """
        Remove um item do dicionário com base na chave fornecida.
        
        Parâmetros:
        chave (str): A chave a ser removida.
        
        Complexidade: O(log N)
        """
        del self.data[chave]

    def mostrar_dados(self):
        """
        Exibe todos os dados do dicionário ordenado.
        
        Retorna:
        dict: O dicionário ordenado como um objeto dict.
        """
        return self.data

    def iterar(self):
        """
        Itera sobre o dicionário, exibindo todas as chaves e valores.
        
        Exibe cada chave e valor no formato: "chave: valor".
        """
        for chave, valor in self.data.items():
            print(f"{chave}: {valor}")

    def menor_chave(self):
        """
        Retorna o menor par chave-valor no dicionário.
        
        Retorna:
        tuple: O par (chave, valor) do menor item.
        
        Complexidade: O(1)
        """
        return self.data.peekitem(0)

    def maior_chave(self):
        """
        Retorna o maior par chave-valor no dicionário.
        
        Retorna:
        tuple: O par (chave, valor) do maior item.
        
        Complexidade: O(1)
        """
        return self.data.peekitem(-1)

    def remover_menor(self):
        """
        Remove o menor item (par chave-valor) do dicionário.
        
        Complexidade: O(log N)
        """
        self.data.popitem(0)

    def remover_maior(self):
        """
        Remove o maior item (par chave-valor) do dicionário.
        
        Complexidade: O(log N)
        """
        self.data.popitem(-1)


# Criando e manipulando o dicionário ordenado
dicionario = DicionarioOrdenado()

# Inserindo elementos
dicionario.inserir("a", 1)
dicionario.inserir("b", 2)
dicionario.inserir("c", 3)

# Realizando buscas
print(dicionario.buscar("a"))  # Saída: 1
print(dicionario.existe("b"))  # Saída: True

# Mostrando os dados em ordem
print(dicionario.mostrar_dados())  # Saída: SortedDict({'a': 1, 'b': 2, 'c': 3})

# Adicionando mais elementos
dicionario.inserir("d", 4)
dicionario.inserir("e", 5)

# Mostrando os dados após a adição
print(dicionario.mostrar_dados())  # Saída: SortedDict({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5})

# Removendo um item
dicionario.remover("b")

# Mostrando os dados após a remoção
print(dicionario.mostrar_dados())  # Saída: SortedDict({'a': 1, 'c': 3, 'd': 4, 'e': 5})

# Iterando sobre o dicionário ordenado
dicionario.iterar()
# Saída:
# a: 1
# c: 3
# d: 4
# e: 5

# Buscando o menor e maior valor
print("Menor chave:", dicionario.menor_chave())  # Saída: ('a', 1)
print("Maior chave:", dicionario.maior_chave())  # Saída: ('e', 5)

# Removendo o menor e maior valor
dicionario.remover_menor()  # Remove o menor item
dicionario.remover_maior()  # Remove o maior item

# Mostrando os dados após a remoção dos itens extremos
print(dicionario.mostrar_dados())  # Saída: SortedDict({'c': 3, 'd': 4})
