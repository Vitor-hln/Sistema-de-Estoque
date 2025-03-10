# Sistema de Estoque

Este projeto é um sistema de gerenciamento de estoque desenvolvido em Python utilizando a biblioteca Tkinter para a interface gráfica e MySQL para o gerenciamento de dados. O sistema permite a inclusão e retirada de produtos, além de fornecer um extrato detalhado das movimentações realizadas.

## Estrutura do Projeto

A estrutura do projeto é a seguinte:

```
sistema-de-estoque
├── src
│   ├── main.py                     # Ponto de entrada da aplicação
│   ├── database
│   │   ├── conexao.py              # Gerencia a conexão com o banco de dados MySQL
│   │   └── operacoes_db.py         # Contém funções para operações no banco de dados
│   ├── controllers
│   │   ├── produto_controller.py    # Controlador para gerenciamento de produtos
│   │   └── movimentacao_controller.py # Controlador para gerenciamento de movimentações
│   ├── models
│   │   ├── produto.py               # Modelo que representa um produto
│   │   └── movimentacao.py          # Modelo que representa uma movimentação de estoque
│   ├── views
│   │   ├── tela_principal.py        # Layout da tela principal da aplicação
│   │   ├── tela_cadastro.py         # Layout para cadastro de produtos
│   │   ├── tela_movimentacao.py     # Layout para movimentação de estoque
│   │   ├── tela_relatorios.py       # Layout para relatórios de movimentação
│   │   └── componentes.py           # Componentes reutilizáveis da interface
│   └── assets
│       └── theme.py                 # Configurações de tema da aplicação
├── resources
│   └── img
│       └── placeholder.txt           # Placeholder para futuras imagens
├── requirements.txt                 # Dependências do projeto
├── config.ini                       # Configurações da aplicação
└── README.md                        # Documentação do projeto
```

## Funcionalidades

- **Cadastro de Produtos**: Permite adicionar novos produtos ao estoque com informações como nome, descrição, preço e quantidade.
- **Movimentação de Estoque**: Registra inclusões e retiradas de produtos, armazenando a data e hora da interação.
- **Relatórios**: Gera relatórios detalhados das movimentações de estoque.
- **Interface Amigável**: Desenvolvido com uma interface moderna e intuitiva utilizando Tkinter.

## Requisitos

Para executar este projeto, você precisará ter o Python instalado, juntamente com as seguintes bibliotecas:

- Tkinter
- MySQL Connector

As dependências podem ser instaladas utilizando o arquivo `requirements.txt`.

## Como Executar

1. Clone o repositório ou faça o download do projeto.
2. Instale as dependências listadas em `requirements.txt`.
3. Configure o banco de dados conforme as instruções no arquivo `config.ini`.
4. Execute o arquivo `main.py` para iniciar a aplicação.

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests para melhorias e correções.

## Licença

Este projeto está licenciado sob a MIT License - veja o arquivo LICENSE para mais detalhes.