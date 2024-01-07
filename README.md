# Script GitHub

Este script Python permite clonar todos os repositórios de um usuário do GitHub, listar todos os repositórios de um usuário do GitHub, testar a conexão com a API do GitHub e renomear todos os repositórios de um usuário do GitHub de CamelCase para KebabCase.

## Instalação

Para rodar o programa é necessário ter o Python 3 instalado e um arquivo de configuração com o token de acesso à API do GitHub. Para criar o arquivo de configuração, siga os seguintes passos:

1. Crie um arquivo chamado `.env` na raiz do projeto.

2. Adicione a seguinte linha ao arquivo:

    ```bash
    GITHUB_USERNAME=username
    GITHUB_TOKEN=token
    ```
    Substitua `username` pelo seu nome de usuário do GitHub.
    Substitua `token` pelo seu token de acesso à API do GitHub.

## Uso

Aqui estão as opções disponíveis:

- `-h`, `--help`: Mostra a mensagem de ajuda e sai.
- `--test`: Testa a conexão com a API do GitHub.
- `--clone`: Clona todos os repositórios de um usuário do GitHub.
- `--list`: Lista todos os repositórios de um usuário do GitHub.
- `--kebabcase`: Renomeia todos os repositórios de um usuário do GitHub de CamelCase para KebabCase.
- `--directory DIRECTORY`: Diretório onde os repositórios serão clonados. O padrão é o diretório atual.

## Exemplo

Para clonar todos os repositórios de um usuário do GitHub para um diretório específico, você pode usar o seguinte comando:

```bash
python github.py --clone --directory /caminho/para/o/diretorio

# Licensa

[GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.pt-br.html)
```

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.pt-br.html)