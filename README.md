# CipherVault

Um aplicativo web simples e seguro para **criptografar** e **descriptografar** arquivos usando **AES-256-CBC**, desenvolvido com Flask.

Todo o processo acontece no servidor: você faz upload do arquivo, digita uma senha (4 a 10 caracteres) e baixa o resultado já criptografado ou descriptografado.

Nenhum arquivo em texto claro fica armazenado permanentemente.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)
![PyCryptodome](https://img.shields.io/badge/PyCryptodome-2.6%2B-orange)

## Funcionalidades

- Criptografar qualquer tipo de arquivo com senha
- Descriptografar arquivos `.enc` com a senha correta
- Senha obrigatória de 4 a 10 caracteres
- Chave derivada com SHA-256 (primeiros 16 bytes → AES-128 efetivo)
- IV aleatório gerado a cada criptografia (pré-pendado no arquivo)
- Padding PKCS7 padrão
- Interface limpa com mensagens de erro/sucesso
- Download automático do arquivo processado

## Aviso importante

**Projeto feito para fins educacionais.**

Embora use criptografia correta, não possui recursos avançados de segurança como:

- Salt + PBKDF2/Argon2
- Modo autenticado (ex: AES-GCM)
- Limite de tentativas (proteção contra brute-force)
- Limpeza automática de arquivos
- HTTPS obrigatório

Use apenas em ambientes confiáveis ou para estudo.

## Como rodar

### Pré-requisitos

- Python 3.8 ou superior

### Passo a passo

```bash
# 1. Clone o repositório
git clone https://github.com/SEU_USUARIO/ciphervault.git
cd ciphervault

# 2. (Recomendado) Crie um ambiente virtual
python -m venv venv
source venv/bin/activate        # Linux/Mac
# ou
venv\Scripts\activate           # Windows

# 3. Instale as dependências
pip install flask pycryptodome

# 4. Execute o aplicativo
python app.py
```
