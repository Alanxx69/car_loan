# Como Executar o Projeto

Este projeto utiliza Django com banco de dados PostgreSQL containerizado via Docker.

## Passos para executar localmente

### 1. Clone o repositório

```bash
git clone https://github.com/Alanxx69/car_loan.git
cd car_loan
```

### 2. Inicie os serviços com Docker Compose

```bash
docker-compose up
```

Este comando irá:

- Baixar a imagem oficial do PostgreSQL (caso necessário)
- Criar um banco de dados chamado `car_loan` com usuário e senha `admin`
- Executar automaticamente o script `init.sql` localizado na pasta `init_db/`

---

## ⚙️ Integração com Django

Após o banco de dados estar em funcionamento via Docker, siga os passos abaixo para conectar o Django ao serviço:

### 3. Execute as migrações

No diretório raiz do projeto, execute:

```bash
python manage.py migrate
```

### 4. Inicie o servidor de desenvolvimento

```bash
python manage.py runserver
```

A aplicação estará acessível em:

```
http://127.0.0.1:8000
```

Se tudo estiver corretamente configurado, o Django estará operando com o banco de dados PostgreSQL fornecido pelo contêiner Docker.
