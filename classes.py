import controller
from datetime import date

class Usuario():

    def __init__(self, id):
        self.id = str(id)

        dados = controller.select_CursorDict('*', 'table_usuarios', f'id="{self.id}"')[0]
        self.username = dados['username']
        self.nome = dados['nome']
        self.cpf = dados['cpf']
        self.telefone = dados['telefone']
        self.email = dados['email']
        self.senha = dados['senha']
