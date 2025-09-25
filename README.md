# Sistema de Gerenciamento de Estoque

## 📝 Sobre o Projeto
Este é um **Sistema de Gerenciamento de Estoque** desenvolvido para otimizar e simplificar o controle de materiais de escritório. O projeto foi concebido com o objetivo de centralizar informações e agilizar as operações diárias de um almoxarifado

---

## ✨ Funcionalidades
O sistema foi construído para atender aos seguintes **requisitos funcionais (RFs)**, garantindo um MVP (Produto Mínimo Viável) robusto

* **RF-001 - Cadastro de Material**: Permite que o usuário cadastre um novo material no estoque, informando nome, categoria, quantidade e descrição
* **RF-002 - Listagem de Materiais**: Exibe todos os materiais cadastrados em uma lista ou tabela
* **RF-003 - Pesquisa de Materiais**: A tela de listagem possui um campo de busca para filtrar materiais por nome ou categoria
* **RF-004 - Atualização de Material**: Permite que o usuário edite as informações de um material já cadastrado
* **RF-005 - Remoção de Material**: Permite que o usuário remova um material do banco de dados

---

## 🛠️ Tecnologias
O projeto foi desenvolvido seguindo os seguintes **requisitos não funcionais (RNFs)**

* **Linguagem de Programação**: Python
* **Banco de Dados**: SQLite
* **Interface**: A interface é simples e intuitiva, de fácil aprendizado para usuários com conhecimentos básicos de informática

---

## 🏗️ Arquitetura
A arquitetura do sistema é baseada no padrão de **Arquitetura em Camadas** (Layered Architecture). Essa abordagem estrutura o software em blocos lógicos, onde cada camada tem uma responsabilidade bem definida.

* **Camada de Apresentação (UI)**: Responsável pela interação com o usuário, contendo as telas principais, de cadastro e de listagem.
* **Camada de Lógica de Negócio (BLL)**: O "cérebro" da aplicação, onde as regras de negócio são executadas e as operações de cadastro, atualização e remoção são orquestradas.
* **Camada de Acesso a Dados (DAL)**: Atua como uma ponte para o banco de dados, traduzindo requisições em comandos SQL (INSERT, SELECT, UPDATE, DELETE).
* **Banco de Dados (SQLite)**: A camada de persistência onde os dados são efetivamente armazenados.

---

## 🚀 Como Iniciar
Para utilizar o sistema, certifique-se de ter **Python 3.x** instalado. Em seguida, siga os passos abaixo:

1.  Baixe a pasta do sistema para o seu computador
2.  Abra o terminal na pasta do projeto
3. Execute o arquivo principal com o comando
    ```bash
    python main.py
    ```
