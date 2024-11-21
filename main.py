from doctest import master
import psycopg2
from psycopg2 import sql
import customtkinter
import tkinter
from tkinter import messagebox


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

    def create(self, nome, tipo, cpf=None, cnpj=None):
        # Verificar se o cliente já existe
        check_query = """
        SELECT * FROM Clientes WHERE (cpf = %s AND cpf IS NOT NULL) OR (cnpj = %s AND cnpj IS NOT NULL);
        """
        if self.db.fetch_all(check_query, (cpf, cnpj)):
            return "Erro: Cliente já existe no banco de dados."

        query = """
        INSERT INTO Clientes (nome, tipo, cpf, cnpj)
        VALUES (%s, %s, %s, %s);
        """
        if self.db.execute_query(query, (nome, tipo, cpf, cnpj)):
            return "Cliente incluído com sucesso."
        return "Erro ao incluir cliente."

    def read(self):
        query = "SELECT * FROM Clientes;"
        return self.db.fetch_all(query)

    def update(self, id_cliente, nome=None, tipo=None, cpf=None, cnpj=None):
        query = """
        UPDATE Clientes
        SET nome = COALESCE(%s, nome),
            tipo = COALESCE(%s, tipo),
            cpf = COALESCE(%s, cpf),
            cnpj = COALESCE(%s, cnpj)
        WHERE id = %s;
        """
        if self.db.execute_query(query, (nome, tipo, cpf, cnpj, id_cliente)):
            return "Cliente atualizado com sucesso."
        return "Erro: Cliente não encontrado para atualização."

    def delete(self, id_cliente):
        # Verificar se o cliente está referenciado
        check_query = """
        SELECT * FROM Fretes WHERE remetente_id = %s OR destinatario_id = %s;
        """
        if self.db.fetch_all(check_query, (id_cliente, id_cliente)):
            return "Erro: Não é possível excluir cliente referenciado em um frete."

        query = "DELETE FROM Clientes WHERE id = %s;"
        if self.db.execute_query(query, (id_cliente,)):
            return "Cliente excluído com sucesso."
        return "Erro: Cliente não encontrado para exclusão."


def centralizar_janela(janela, largura, altura):
    #tamanho da tela
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    
    pos_x = (largura_tela // 2) - (largura // 2)
    pos_y = (altura_tela // 2) - (altura // 2)
    
    janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Transportadora")
        self.setup_ui()

    def setup_ui(self):
        # Inicializando o TabView com largura maior
        self.tabview = customtkinter.CTkTabview(self.root, width=1000, height=600)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)

        # Criando as tabs
        self.tabview.add("Clientes")
        self.tabview.add("Funcionários")
        self.tabview.add("Fretes")

        # Ajustando layout para tamanho da tela do app
        self.tabview._segmented_button.grid(sticky="ew")  # Preenche horizontalmente

        # Configurando tab
        self.setup_clientes_tab()
        self.setup_funcionarios_tab()
        self.setup_fretes_tab()

    def setup_clientes_tab(self):
        # Clientes
        clientes_tab = self.tabview.tab("Clientes")
        clientes_tab.grid_columnconfigure(0, weight=1)
        clientes_tab.grid_rowconfigure(0, weight=1)  # Parte superior
        clientes_tab.grid_rowconfigure(1, weight=3)  # Parte inferior

        #Cadastro
        cadastro_frame = customtkinter.CTkFrame(clientes_tab)
        cadastro_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        customtkinter.CTkLabel(cadastro_frame, text="Nome:").grid(row=0, column=0, padx=10, pady=5)
        customtkinter.CTkEntry(cadastro_frame).grid(row=0, column=1, padx=10, pady=5)

        customtkinter.CTkLabel(cadastro_frame, text="Tipo:").grid(row=1, column=0, padx=10, pady=5)
        customtkinter.CTkEntry(cadastro_frame).grid(row=1, column=1, padx=10, pady=5)

        customtkinter.CTkButton(cadastro_frame, text="Salvar Cliente",
                                 command=lambda: self.salvar_dados("Cliente")).grid(
            row=2, column=0, columnspan=2, pady=10
        )

        #Consulta
        consulta_frame = customtkinter.CTkFrame(clientes_tab)
        consulta_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        customtkinter.CTkLabel(consulta_frame, text="Consulta de Clientes", font=("Arial", 16)).pack(pady=10)

    def setup_funcionarios_tab(self):
        #Funcionários
        funcionarios_tab = self.tabview.tab("Funcionários")
        funcionarios_tab.grid_columnconfigure(0, weight=1)
        funcionarios_tab.grid_rowconfigure(0, weight=1)
        funcionarios_tab.grid_rowconfigure(1, weight=3)

        #Cadastro
        cadastro_frame = customtkinter.CTkFrame(funcionarios_tab)
        cadastro_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        customtkinter.CTkLabel(cadastro_frame, text="Nome do Funcionário:").grid(row=0, column=0, padx=10, pady=5)
        customtkinter.CTkEntry(cadastro_frame).grid(row=0, column=1, padx=10, pady=5)

        customtkinter.CTkLabel(cadastro_frame, text="Cargo:").grid(row=1, column=0, padx=10, pady=5)
        customtkinter.CTkEntry(cadastro_frame).grid(row=1, column=1, padx=10, pady=5)

        customtkinter.CTkButton(cadastro_frame, text="Salvar Funcionário",
                                 command=lambda: self.salvar_dados("Funcionário")).grid(
            row=2, column=0, columnspan=2, pady=10
        )

        # Consulta
        consulta_frame = customtkinter.CTkFrame(funcionarios_tab)
        consulta_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        customtkinter.CTkLabel(consulta_frame, text="Consulta de Funcionários", font=("Arial", 16)).pack(pady=10)

    def setup_fretes_tab(self):
        #retes
        fretes_tab = self.tabview.tab("Fretes")
        fretes_tab.grid_columnconfigure(0, weight=1)
        fretes_tab.grid_rowconfigure(0, weight=1)
        fretes_tab.grid_rowconfigure(1, weight=3)

        #Cadastro
        cadastro_frame = customtkinter.CTkFrame(fretes_tab)
        cadastro_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        customtkinter.CTkLabel(cadastro_frame, text="Número do Frete:").grid(row=0, column=0, padx=10, pady=5)
        customtkinter.CTkEntry(cadastro_frame).grid(row=0, column=1, padx=10, pady=5)

        customtkinter.CTkLabel(cadastro_frame, text="Origem:").grid(row=1, column=0, padx=10, pady=5)
        customtkinter.CTkEntry(cadastro_frame).grid(row=1, column=1, padx=10, pady=5)

        customtkinter.CTkButton(cadastro_frame, text="Salvar Frete", command=lambda: self.salvar_dados("Frete")).grid(
            row=2, column=0, columnspan=2, pady=10
        )



        #Consulta
        consulta_frame = customtkinter.CTkFrame(fretes_tab)
        consulta_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        customtkinter.CTkLabel(consulta_frame, text="Consulta de Fretes", font=("Arial", 16)).pack(pady=10)

    def salvar_dados(self, tipo):
        # Apenas uma mensagem de exemplo
        messagebox.showinfo("Salvar", f"{tipo} salvo com sucesso!")


if __name__ == "__main__":
    # Inicializando a interface principal
    root = customtkinter.CTk()
    root.geometry("1000x700")
    app = App(root)
    root.mainloop()