# 🧺 Lavanderia Automatizada

Este projeto consiste no desenvolvimento de um **Sistema de Controle para Lavanderia Automatizada**, concebido como atividade prática para a disciplina de **Análise e Projeto de Sistemas (APS)**. O software foi construído com foco na organização da arquitetura e na implementação de requisitos funcionais baseados em modelagem UML.

## 📖 Sobre o Projeto

A solução foi desenvolvida para digitalizar o fluxo operacional de uma lavanderia, abrangendo desde a recepção do cliente até a entrega final das peças. O sistema visa a eficiência no atendimento e a transparência no rastreio de pedidos, integrando regras de negócio como precificações por material e descontos automáticos por volume.

### Principais Funcionalidades

- **Gestão de Fluxo Lógico:** Os pedidos passam por etapas sequenciais (Recebido, Lavagem, Secagem, Passagem e Pronto para Retirada) que podem ser acompanhadas em tempo real.
- **Cálculo Dinâmico:** Precificação automática baseada no tipo de peça e tipo de material (ex: acréscimo de 20% para peças em seda).
- **Persistência de Dados:** Uso de banco de dados relacional para garantir o armazenamento seguro de informações de clientes, pedidos e itens.
- **Interface de Rastreio:** Módulo exclusivo para que o cliente consulte o status atual do seu pedido de forma visual e intuitiva.

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python
- **Framework Web:** Flask
- **Banco de Dados:** SQLite3
- **Frontend:** HTML5, CSS3 (Customizado) e Bootstrap 5

## 🚀 Como Executar

1.  **Certifique-se de ter o Python instalado em sua máquina.**
2.  **Instale as dependências necessárias (Flask):**

    ```bash
    pip install flask
    ```

3.  **Inicie a aplicação:**
    ```bash
    python app.py
    ```
4.  **Acesse no navegador:**
    Abra o endereço `http://127.0.0.1:5000`

> **Acesso Administrativo (Padrão):** > **Usuário:** `admin` | **Senha:** `123`

## 📝 Organização do Projeto

- `app.py`: Controlador principal contendo as rotas e a lógica de navegação do sistema.
- `models.py`: Definição das classes de negócio (`Cliente`, `Peca`, `Pedido`) e regras de cálculo de valores.
- `database.py`: Scripts de configuração, conexão e inicialização das tabelas do banco de dados SQLite.
- `static/css/style.css`: Estilização centralizada para garantir a identidade visual em todas as páginas.
- `templates/`: Diretório contendo as interfaces HTML (Login, Registro, Gestão e Consulta).
- `.gitignore`: Configurado para ignorar arquivos de sistema e o banco de dados local (`lavanderia.db`).

---

**Desenvolvido por:** Francisco de Cássio da Silva Mourão Júnior e Isaac de Jesus Santos.

**Instituição:** Instituto Federal de Educação, Ciência e Tecnologia do Piauí (IFPI) - Campus Teresina Central.
