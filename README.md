# Projeto Capstone de DevOps

Este repositório é dedicado ao projeto capstone do curso de DevOps, focado no desenvolvimento e implementação de um microsserviço de contas de cliente. O projeto abrange diversas etapas do ciclo de vida de desenvolvimento de software, incluindo planejamento ágil, desenvolvimento orientado a testes (TDD), conteinerização com Docker e orquestração com Kubernetes.

## Visão Geral do Projeto

O objetivo principal é desenvolver um microsserviço de contas que permita criar, ler, atualizar, deletar e listar informações de clientes para um site de e-commerce. Este serviço será construído como uma API REST bem definida, permitindo a integração com outros microsserviços.

O desenvolvimento seguiu práticas ágeis, utilizando o GitHub para gerenciamento de projetos, incluindo quadros Kanban para acompanhamento de sprints e user stories para definição de funcionalidades.

## Estrutura do Repositório

- `.github/ISSUE_TEMPLATE/`: Contém o template padrão para a criação de user stories.
- `service/`: Contém o código-fonte do microsserviço Flask.
- `tests/`: Contém os testes unitários e de integração para o serviço.
- `Dockerfile`: Arquivo para conteinerização da aplicação Flask.
- `requirements.txt`: Lista as dependências Python do projeto.
- `deployment.yaml`: Manifesto Kubernetes para o Deployment do serviço.
- `service.yaml`: Manifesto Kubernetes para expor o Service.
- `README.md`: Este arquivo, com a documentação do projeto.
- `LICENSE`: Arquivo de licença MIT.
- `.gitignore`: Especifica arquivos e diretórios ignorados pelo Git.
- `setup.cfg`: Arquivo de configuração para ferramentas de teste como pytest.

## Funcionalidades Implementadas

1.  Configuração do ambiente de desenvolvimento e planejamento ágil.
2.  Desenvolvimento de um serviço RESTful para Contas de Cliente com os seguintes endpoints:
    *   `GET /accounts`: Lista todas as contas.
    *   `POST /accounts`: Cria uma nova conta.
    *   `GET /accounts/{id}`: Lê uma conta específica.
    *   `PUT /accounts/{id}`: Atualiza uma conta específica.
    *   `DELETE /accounts/{id}`: Deleta uma conta específica.
3.  Desenvolvimento orientado a testes (TDD) com pytest, alcançando alta cobertura de código.
4.  Conteinerização do microsserviço utilizando Docker.
5.  Deploy da imagem Docker no Kubernetes.

## Tecnologias e Ferramentas

- Python (Flask)
- REST APIs
- Git e GitHub
- Docker
- Kubernetes
- Pytest (para testes)
- Práticas Ágeis (Scrum/Kanban)

## Como Executar o Projeto

### Pré-requisitos

- Git
- Python 3.9+
- Docker
- kubectl (configurado para acessar um cluster Kubernetes)
- Um registro de contêiner (ex: Docker Hub) se for fazer deploy no Kubernetes.

### 1. Clonar o Repositório

```bash
git clone https://github.com/galafis/devops-capstone-project.git
cd devops-capstone-project
```

### 2. Execução Local (sem Docker, para desenvolvimento/testes)

É recomendado criar um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # No Linux/macOS
# venv\Scripts\activate    # No Windows

pip install -r requirements.txt
flask run --port=8000
```

Os testes podem ser executados com:
```bash
pytest
```

### 3. Execução com Docker

#### a. Construir a Imagem Docker

Na raiz do projeto (onde o `Dockerfile` está localizado):

```bash
docker build -t devops-capstone-project:latest .
```

(Se você pretende enviar para um registro como o Docker Hub, use seu nome de usuário: `docker build -t seu_usuario_dockerhub/devops-capstone-project:latest .`)

#### b. Executar o Container Docker

```bash
docker run -p 8000:8000 devops-capstone-project:latest
```

(Se usou seu nome de usuário no build: `docker run -p 8000:8000 seu_usuario_dockerhub/devops-capstone-project:latest`)

A aplicação estará acessível em `http://localhost:8000`.

### 4. Deploy no Kubernetes

#### a. Enviar a Imagem para um Registro de Contêiner

Se você ainda não o fez, envie sua imagem Docker para um registro acessível pelo seu cluster Kubernetes (ex: Docker Hub).

```bash
# Faça login no seu registro (ex: Docker Hub)
# docker login

# Envie a imagem (substitua 'seu_usuario_dockerhub' se aplicável)
docker push galafis/devops-capstone-project:latest
```

**Importante:** O arquivo `deployment.yaml` está configurado para usar a imagem `galafis/devops-capstone-project:latest`. Se você usou um nome de imagem ou registro diferente, atualize o campo `spec.template.spec.containers[0].image` no arquivo `deployment.yaml` antes de aplicar.

#### b. Aplicar os Manifestos Kubernetes

Na raiz do projeto, onde os arquivos `deployment.yaml` e `service.yaml` estão localizados:

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

#### c. Verificar o Deploy

```bash
kubectl get deployments
kubectl get pods
kubectl get services devops-capstone-project-service
```

Aguarde até que os pods estejam no estado `Running` e o serviço `devops-capstone-project-service` tenha um `EXTERNAL-IP` (se estiver usando `type: LoadBalancer` e seu provedor de nuvem suportar).

#### d. Acessar a Aplicação no Kubernetes

Use o `EXTERNAL-IP` e a porta exposta pelo serviço (porta 80, conforme `service.yaml`) para acessar a aplicação. Se estiver usando `NodePort`, você precisará do IP de um dos nós do cluster e da `NodePort` atribuída.

## Contribuições

Este projeto foi desenvolvido como parte de um programa de formação. Pull requests e sugestões são bem-vindos para melhorias e aprendizado contínuo.

Este projeto visa demonstrar competências em desenvolvimento full-stack, com ênfase em práticas de DevOps, seguindo as diretrizes do programa de formação IBM Full-Stack JavaScript Developer.

