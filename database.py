import psycopg2
from psycopg2 import sql


class Database:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                dbname="cmp1611-ativ2-Johnatan",
                user="postgres",
                password="salame123",
                host="localhost",
                port="5432"
            )
            self.cursor = self.conn.cursor()
            print("Conexão com o banco estabelecida.")
        except Exception as e:
            print(f"Erro ao conectar ao banco: {e}")

    def close(self):
        self.cursor.close()
        self.conn.close()

    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Erro na consulta: {e}")
            self.conn.rollback()
            return False

    def fetch_all(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()


class CrudClientes:
    def __init__(self, db: Database):
        self.db = db

    def create(self, nome, tipo, cpf=None, cnpj=None, endereco=None, telefone=None, representante=None, telefone_representante=None, inscricao_estadual=None):
        # Verificar se os campos obrigatórios estão presentes
        if not nome or not endereco or not telefone:
            return "Erro: Nome, endereço e telefone são campos obrigatórios."

        # Verificar se o tipo de cliente é válido
        if tipo not in ['Pessoa Física', 'Empresa']:
            return "Erro: Tipo inválido. Deve ser 'Pessoa Física' ou 'Empresa'."

        # Verificar se CPF e CNPJ são fornecidos corretamente de acordo com o tipo
        if tipo == 'Pessoa Física' and cnpj is not None:
            return "Erro: CNPJ não deve ser informado para Pessoa Física."
        if tipo == 'Empresa' and cpf is not None:
            return "Erro: CPF não deve ser informado para Empresa."
        
        # Verificar se inscrição estadual é fornecida para empresas
        if tipo == 'Empresa' and not inscricao_estadual:
            return "Erro: Inscrição estadual é obrigatória para empresas."
        
        # Verificar se o cliente já existe
        check_query = """
        SELECT * FROM Clientes WHERE (cpf = %s AND cpf IS NOT NULL) OR (cnpj = %s AND cnpj IS NOT NULL);
        """
        if self.db.fetch_all(check_query, (cpf, cnpj)):
            return "Erro: Cliente já existe no banco de dados."

        query = """
        INSERT INTO Clientes (nome, tipo, cpf, cnpj, endereco, telefone, representante, telefone_representante, inscricao_estadual)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        if self.db.execute_query(query, (nome, tipo, cpf, cnpj, endereco, telefone, representante, telefone_representante, inscricao_estadual)):
            return "Cliente incluído com sucesso."
        return "Erro ao incluir cliente."

    def read(self):
        query = "SELECT * FROM Clientes;"
        return self.db.fetch_all(query)

    def update(self, id_cliente, nome=None, tipo=None, cpf=None, cnpj=None, endereco=None, telefone=None, representante=None, telefone_representante=None, inscricao_estadual=None):
        # Verificar se o cliente existe
        check_query = "SELECT * FROM Clientes WHERE id = %s;"
        if not self.db.fetch_all(check_query, (id_cliente,)):
            return "Erro: Cliente não encontrado para atualização."

        # Verificar se o tipo de cliente é válido
        if tipo and tipo not in ['Pessoa Física', 'Empresa']:
            return "Erro: Tipo inválido. Deve ser 'Pessoa Física' ou 'Empresa'."

        # Verificar se CPF e CNPJ são fornecidos corretamente de acordo com o tipo
        if tipo == 'Pessoa Física' and cnpj is not None:
            return "Erro: CNPJ não deve ser informado para Pessoa Física."
        if tipo == 'Empresa' and cpf is not None:
            return "Erro: CPF não deve ser informado para Empresa."

        # Verificar se inscrição estadual é fornecida para empresas
        if tipo == 'Empresa' and not inscricao_estadual:
            return "Erro: Inscrição estadual é obrigatória para empresas."

        # Atualizar apenas os campos que foram fornecidos
        query = """
        UPDATE Clientes
        SET nome = COALESCE(%s, nome),
            tipo = COALESCE(%s, tipo),
            cpf = COALESCE(%s, cpf),
            cnpj = COALESCE(%s, cnpj),
            endereco = COALESCE(%s, endereco),
            telefone = COALESCE(%s, telefone),
            representante = COALESCE(%s, representante),
            telefone_representante = COALESCE(%s, telefone_representante),
            inscricao_estadual = COALESCE(%s, inscricao_estadual)
        WHERE id = %s;
        """
        if self.db.execute_query(query, (nome, tipo, cpf, cnpj, endereco, telefone, representante, telefone_representante, inscricao_estadual, id_cliente)):
            return "Cliente atualizado com sucesso."
        return "Erro ao atualizar cliente."
    
    def queryID(self, name):
        query = "SELECT id FROM Clientes WHERE nome = %s;"
        try:
            result = self.db.fetch_all(query, (name,))
            if result:  
                return result[0][0]  
            return None  
        except Exception as e:
            print(f"Erro ao executar a consulta: {e}")
            return None
    
    def delete(self, id_cliente):
        # Verificar se o cliente está referenciado em fretes
        check_query = """
        SELECT 1 FROM Fretes WHERE remetente_id = %s OR destinatario_id = %s;
        """
        if self.db.fetch_all(check_query, (id_cliente, id_cliente)):
            return "Erro: Não é possível excluir cliente referenciado em um frete."

        # Excluir o cliente
        delete_query = "DELETE FROM Clientes WHERE id = %s;"
        if self.db.execute_query(delete_query, (id_cliente,)):
            return "Cliente excluído com sucesso."
        return "Erro: Cliente não encontrado para exclusão."
