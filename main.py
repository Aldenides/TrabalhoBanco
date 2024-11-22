from doctest import master
from tkinter import ttk
import customtkinter
import tkinter
from tkinter import messagebox
from tabulate import tabulate

from database import Database, CrudClientes



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
        self.db = Database()
        self.CrudClientes = CrudClientes(self.db)
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

    def cadastrar_cliente (self):
        nome = self.nome_entry.get()
        tipo = self.tipo_entry.get()
        cpf = self.cpf_entry.get() if tipo == 'Pessoa Física' else None
        cnpj = self.cnpj_entry.get() if tipo == 'Empresa' else None
        endereco = self.endereco_entry.get()
        telefone = self.telefone_entry.get()
        representante = self.representante_entry.get() if tipo == 'Empresa' else None
        telefone_representante = self.telefone_representante_entry.get() if tipo == 'Empresa' else None
        inscricao_estadual = self.inscricao_estadual_entry.get() if tipo == 'Empresa' else None
        resultado = self.CrudClientes.create(nome, tipo, cpf, cnpj, endereco, telefone, representante, telefone_representante, inscricao_estadual)
        messagebox.showinfo("Resultado", resultado)

    def atualizar_cliente(self):
        id_cliente = self.CrudClientes.queryID(self.nome_entry.get())
        nome = self.nome_entry.get()
        tipo = self.tipo_entry.get()
        cpf = self.cpf_entry.get() if tipo == 'Pessoa Física' else None
        cnpj = self.cnpj_entry.get() if tipo == 'Empresa' else None
        endereco = self.endereco_entry.get()
        telefone = self.telefone_entry.get()
        representante = self.representante_entry.get() if tipo == 'Empresa' else None
        telefone_representante = self.telefone_representante_entry.get() if tipo == 'Empresa' else None
        inscricao_estadual = self.inscricao_estadual_entry.get() if tipo == 'Empresa' else None

        resultado = self.CrudClientes.update(id_cliente, nome, tipo, cpf, cnpj, endereco, telefone, representante, telefone_representante, inscricao_estadual)
        messagebox.showinfo("Resultado", resultado)

    def excluir_cliente(self):
        id_cliente = self.CrudClientes.queryID(self.nome_entry.get())
        resultado = self.CrudClientes.delete(id_cliente)
        messagebox.showinfo("Resultado", resultado)

    def limpar_campos(self):
        self.nome_entry.delete(0, tkinter.END)
        self.cpf_entry.delete(0, tkinter.END)
        self.cnpj_entry.delete(0, tkinter.END)
        self.endereco_entry.delete(0, tkinter.END)
        self.telefone_entry.delete(0, tkinter.END)
        self.representante_entry.delete(0, tkinter.END)
        self.telefone_representante_entry.delete(0, tkinter.END)
        self.inscricao_estadual_entry.delete(0, tkinter.END)
        self.tipo_entry.set('')  # Reseta o OptionMenu

    def setup_clientes_tab(self):
        clientes_tab = self.tabview.tab("Clientes")
        clientes_tab.grid_columnconfigure(0, weight=1)
        clientes_tab.grid_rowconfigure(0, weight=1)
        clientes_tab

    def listar_clientes(self):
        query = "SELECT nome, tipo, telefone FROM Clientes;"
        try:
            # Executar a consulta
            resultados = self.db.fetch_all(query)

            # Verificar se há dados
            if not resultados:
                print("Nenhum cliente encontrado.")
                return
            
            # Converter resultados para tabela
            headers = ["Nome", "Tipo", "Telefone"]
            tabela = tabulate(resultados, headers=headers, tablefmt="grid")
            
            # Exibir tabela
            messagebox.showinfo("Resultado", tabela)
            print(tabela)
        except Exception as e:
            print(f"Erro ao listar clientes: {e}")

    def setup_clientes_tab(self):
        # Clientes
        clientes_tab = self.tabview.tab("Clientes")
        clientes_tab.grid_columnconfigure(0, weight=1)
        clientes_tab.grid_rowconfigure(0, weight=1)  # Parte superior
        clientes_tab.grid_rowconfigure(1, weight=3)  # Parte inferior

        #Cadastro
        cadastro_frame = customtkinter.CTkFrame(clientes_tab)
        cadastro_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.nome_entry = customtkinter.CTkEntry(cadastro_frame, placeholder_text="Nome")
        self.nome_entry.grid(row=0, column=0, padx=10, pady=5)
        self.cpf_entry = customtkinter.CTkEntry(cadastro_frame, placeholder_text="CPF")
        self.cpf_entry.grid(row=1, column=0, padx=10, pady=5)
        self.cnpj_entry = customtkinter.CTkEntry(cadastro_frame, placeholder_text="CNPJ")
        self.cnpj_entry.grid(row=2, column=0, padx=10, pady=5)
        self.endereco_entry = customtkinter.CTkEntry(cadastro_frame, placeholder_text="Endereço")
        self.endereco_entry.grid(row=3, column=0, padx=10, pady=5)
        self.telefone_entry = customtkinter.CTkEntry(cadastro_frame, placeholder_text="Telefone")
        self.telefone_entry.grid(row=0, column=1, padx=10, pady=5)
        self.representante_entry = customtkinter.CTkEntry(cadastro_frame, placeholder_text="Representante")
        self.representante_entry.grid(row=1, column=1, padx=10, pady=5)
        self.telefone_representante_entry = customtkinter.CTkEntry(cadastro_frame, placeholder_text="Telefone Representante")
        self.telefone_representante_entry.grid(row=2, column=1, padx=10, pady=5)
        self.inscricao_estadual_entry = customtkinter.CTkEntry(cadastro_frame, placeholder_text="Inscrição Estadual")
        self.inscricao_estadual_entry.grid(row=3, column=1, padx=10, pady=5)
        self.tipo_entry = customtkinter.CTkOptionMenu(cadastro_frame, fg_color="gray20", button_color="black", values=["Pessoa Física", "Empresa"])
        self.tipo_entry.grid(row=4, column=0, padx=10, pady=5)
        # Botões
        botao_cadastrar = customtkinter.CTkButton(cadastro_frame, text="Cadastrar", command=self.cadastrar_cliente)
        botao_cadastrar.grid(row=0, column=2, padx=10, pady=10)
        botao_atualizar = customtkinter.CTkButton(cadastro_frame, text="Atualizar", command=self.atualizar_cliente)
        botao_atualizar.grid(row=1, column=2, padx=10, pady=10)
        botao_excluir = customtkinter.CTkButton(cadastro_frame, text="Excluir", command=self.excluir_cliente)
        botao_excluir.grid(row=2, column=2, padx=10, pady=10)
        botao_limpar = customtkinter.CTkButton(cadastro_frame, text="Limpar", command=self.limpar_campos)
        botao_limpar.grid(row=3, column=2, padx=10, pady=10)

        #Consulta
        consulta_frame = customtkinter.CTkFrame(clientes_tab)
        consulta_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        customtkinter.CTkLabel(consulta_frame, text="Consulta de Clientes", font=("Arial", 16)).pack(pady=10)
        botao_listar = customtkinter.CTkButton(consulta_frame, text="Listar Clientes", command=self.listar_clientes)
        botao_listar.pack(pady=10)

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