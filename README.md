
# Trabalho de banco de dados

🛢Script utilizado para criar o banco:

-- Tabela Estados
CREATE TABLE Estados (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    icms_interno DECIMAL(5, 2) NOT NULL,
    icms_externo DECIMAL(5, 2) NOT NULL
);

-- Tabela Cidades
CREATE TABLE Cidades (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    estado_id INT NOT NULL,
    FOREIGN KEY (estado_id) REFERENCES Estados(id)
);

-- Tabela Clientes
CREATE TABLE Clientes (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(20) CHECK (tipo IN ('Pessoa Física', 'Empresa')),
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14),
    cnpj VARCHAR(18),
    inscricao_estadual VARCHAR(20),
    endereco VARCHAR(255) NOT NULL,
    telefone VARCHAR(15) NOT NULL,
    representante VARCHAR(100),
    telefone_representante VARCHAR(15),
    CHECK ((tipo = 'Pessoa Física' AND cpf IS NOT NULL AND cnpj IS NULL) OR 
           (tipo = 'Empresa' AND cnpj IS NOT NULL AND cpf IS NULL))
);

-- Tabela Funcionarios
CREATE TABLE Funcionarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    registro VARCHAR(20) NOT NULL UNIQUE
);

-- Tabela PrecosFrete
CREATE TABLE PrecosFrete (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(20) CHECK (tipo IN ('Peso', 'Valor')),
    valor_unitario DECIMAL(10, 2) NOT NULL
);

-- Tabela Fretes
CREATE TABLE Fretes (
    id SERIAL PRIMARY KEY,
    numero_conhecimento VARCHAR(50) NOT NULL UNIQUE,
    remetente_id INT NOT NULL,
    destinatario_id INT NOT NULL,
    cidade_origem_id INT NOT NULL,
    cidade_destino_id INT NOT NULL,
    peso DECIMAL(10, 2),
    valor_mercadoria DECIMAL(10, 2),
    frete_tipo VARCHAR(20) CHECK (frete_tipo IN ('Peso', 'Valor')),
    frete_valor DECIMAL(10, 2) NOT NULL,
    icms DECIMAL(10, 2) NOT NULL,
    pedagio DECIMAL(10, 2) DEFAULT 0,
    frete_pagador VARCHAR(20) CHECK (frete_pagador IN ('Remetente', 'Destinatário')),
    data_frete DATE NOT NULL,
    funcionario_id INT NOT NULL,
    FOREIGN KEY (remetente_id) REFERENCES Clientes(id),
    FOREIGN KEY (destinatario_id) REFERENCES Clientes(id),
    FOREIGN KEY (cidade_origem_id) REFERENCES Cidades(id),
    FOREIGN KEY (cidade_destino_id) REFERENCES Cidades(id),
    FOREIGN KEY (funcionario_id) REFERENCES Funcionarios(id)
);


