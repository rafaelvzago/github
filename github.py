import requests
import os
import dotenv
import argparse
import re

# Carregando as variáveis de ambiente do arquivo .env
dotenv.load_dotenv()

# Funçcão para deletar repositórios do GitHub baseados numa lista de nomes de repositórios.
def delete_repositories(username, token, repositories):
    for repo in repositories:
        print(f"Deletando {repo}...")
        delete_repository(username, token, repo)

# Função para deletar um repositório do GitHub.
def delete_repository(username, token, repo):
    url = f"https://api.github.com/repos/{username}/{repo}"
    headers = {"Authorization": f"token {token}"}
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        print(f"Repositório {repo} deletado.")
    else:
        print(f"Erro ao deletar repositório {repo}: {response.status_code} - {response.text}")

# Carregando o nome de usuário e token de acesso pessoal do GitHub do arquivo .env
username = os.getenv("GITHUB_USERNAME")
token = os.getenv("GITHUB_TOKEN")

# Função para clonar todos os repositórios de um usuário do GitHub usando paginação.
def clone_repositories(username, token, directory):
    page = 1

    while True:
        # Define a URL da API do GitHub para listar seus repositórios com base na página atual
        url = f"https://api.github.com/users/{username}/repos?page={page}&per_page=100"

        # Faz uma solicitação GET para a API do GitHub
        headers = {"Authorization": f"token {token}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            repositories = response.json()
            if not repositories:
                break  # Não há mais repositórios para listar
            for repo in repositories:
                repo_name = repo["name"]
                repo_url = repo["clone_url"]
                print(f"Clonando {repo_name}...")
                os.system(f"git clone {repo_url} {directory}/{repo_name}")
            page += 1
        else:
            print(f"Erro ao listar repositórios: {response.status_code} - {response.text}")
            break


# Função para testar a conexão com a API do GitHub.
def test_connection(username, token):
    url = f"https://api.github.com/users/{username}"
    headers = {"Authorization": f"token {token}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Conexão com a API do GitHub bem sucedida.")
    else:
        print(f"Erro ao conectar com a API do GitHub: {response.status_code} - {response.text}")

# Função para listar todos os repositórios de um usuário do GitHub.
def list_repositories(username, token):
    page = 1
    repositories = []

    while True:
        # Define a URL da API do GitHub para listar seus repositórios com base na página atual
        url = f"https://api.github.com/users/{username}/repos?page={page}&per_page=100"

        # Faz uma solicitação GET para a API do GitHub
        headers = {"Authorization": f"token {token}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            new_repositories = response.json()
            if not new_repositories:
                break  # Não há mais repositórios para listar
            repositories.extend(new_repositories)
            page += 1
        else:
            print(f"Erro ao listar repositórios: {response.status_code} - {response.text}")
            break
    for repo in repositories:
        print(repo["name"])

        
def rename_camelcase_to_kebabcase(username, token, directory):
    # Obtém a lista de repositórios locais no diretório especificado
    local_repositories =  get_all_repository_names(username, token)

    for remote_repo_name in local_repositories:
        # Verifica se o nome do repositório local está em CamelCase
        
        if not re.match(r'^[a-z]+(?:[A-Z][a-z]*)*$', remote_repo_name):
            # Converte CamelCase para KebabCase
            kebab_case_name = re.sub(r'([a-z0-9])([A-Z])', r'\1-\2', remote_repo_name).lower()


            # Define a URL da API do GitHub para renomear o repositório
            url = f"https://api.github.com/repos/{username}/{remote_repo_name}"
            # Cria um payload com o novo nome
            payload = {
                "name": kebab_case_name
            }
            
            # Faz uma solicitação PATCH para atualizar o nome do repositório
            headers = {"Authorization": f"token {token}"}
            response = requests.patch(url, json=payload, headers=headers)
            if response.status_code == 200:
                print(f"Repositório {remote_repo_name} renomeado para {kebab_case_name}.")
            else:
                print(f"Erro ao renomear repositório {remote_repo_name}: {response.status_code} - {response.text}")


def get_all_repository_names(username, token):
    page = 1
    repositories = []

    while True:
        # Define a URL da API do GitHub para listar os repositórios do usuário com base na página atual
        url = f"https://api.github.com/users/{username}/repos?page={page}&per_page=100"

        # Faz uma solicitação GET para a API do GitHub
        headers = {"Authorization": f"token {token}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            new_repositories = response.json()
            if not new_repositories:
                break  # Não há mais repositórios para listar
            repositories.extend(new_repositories)
            page += 1
        else:
            print(f"Erro ao listar repositórios: {response.status_code} - {response.text}")
            break

    repository_names = [repo["name"] for repo in repositories]
    return repository_names



def main():

    # Recebendo por parametro da linha de comando o argumento com a ser executada.
    parser = argparse.ArgumentParser(description="Script para clonar todos os repositórios de um usuário do GitHub.")
    parser.add_argument("--test", help="Testa a conexão com a API do GitHub.", action="store_true", required=False)
    parser.add_argument("--clone", help="Clona todos os repositórios de um usuário do GitHub.", action="store_true", required=False)
    parser.add_argument("--list", help="Lista todos os repositórios de um usuário do GitHub.", action="store_true", required=False)
    parser.add_argument("--kebabcase", help="Renomeia todos os repositórios de um usuário do GitHub de CamelCase para KebabCase.", action="store_true", required=False)
    parser.add_argument("--directory", help="Diretório onde os repositórios serão clonados. O padrão é o diretório atual.", default=".", required=False)
    args = parser.parse_args()

    if args.test:
        test_connection(username, token)
    elif args.list:
        list_repositories(username, token)
    elif args.clone:
        clone_repositories(username, token, args.directory)
    elif args.kebabcase:
        rename_camelcase_to_kebabcase(username, token, args.directory)
    else:
        print("Comando inválido.")

if __name__ == "__main__":
    main()