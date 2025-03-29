# Face Authentication API

## Descrição

Esta é uma API para autenticação de usuários com reconhecimento facial utilizando o modelo **FaceNet**. Ela compara uma imagem de entrada com imagens cadastradas previamente e retorna o usuário correspondente se a semelhança for suficiente.

## Tecnologias Utilizadas

- **Python 3.x**
- **Flask** (Framework web)
- **OpenCV** (Processamento de imagem)
- **NumPy** (Manipulação de matrizes)
- **PyTorch** (Execução do modelo FaceNet)
- **FaceNet-PyTorch** (Modelo de reconhecimento facial)

## Instalação e Execução

### 1. Clonar o projeto
$ git clone https://github.com/Thalys-Riquelmy/api-facial-recognition.git
$ cd api-facial-recognition
```

### 2. Criar um ambiente virtual
```bash
# Criar o ambiente virtual
$ python3 -m venv venv

# Ativar o ambiente virtual
$ source venv/bin/activate  # Linux/Mac
$ venv\Scripts\activate  # Windows
```

### 3. Instalar dependências
```bash
$ pip install -r requirements.txt
```

### 4. Executar a API
```bash
$ python app.py
```

A API estará disponível em `http://0.0.0.0:5000`.

## Uso da API

### Endpoint `/authenticate`
- **Método:** `POST`
- **Objetivo:** Autenticar um usuário com base em imagens cadastradas previamente.
- **Parâmetros:**
  - `image2` (arquivo): Imagem da pessoa que deseja autenticar.
  - `images1[]` (arquivos): Imagens cadastradas dos usuários (chaves nomeadas como `images1[ID]`).

### Exemplo de Teste no Postman
1. Abrir o **Postman**
2. Criar uma nova requisição `POST`
3. Definir a URL: `http://127.0.0.1:5000/authenticate`
4. No corpo da requisição, selecionar **form-data** e adicionar os seguintes campos:
   - **Key:** `image2` | **Tipo:** File | **Valor:** (Selecionar a imagem de teste)
   - **Key:** `images1[1]` | **Tipo:** File | **Valor:** (Selecionar a imagem do usuário cadastrado 1)
   - **Key:** `images1[2]` | **Tipo:** File | **Valor:** (Selecionar a imagem do usuário cadastrado 2)
5. Enviar a requisição e verificar a resposta.

### Possíveis Respostas
- **Sucesso:**
```json
{
    "status": "success",
    "message": "Usuário 1 validado com sucesso!",
    "userId": 1
}
```

- **Erro (usuário não reconhecido):**
```json
{
    "status": "error",
    "message": "Usuário não reconhecido"
}
```

## Ajustando o Limite de Similaridade
A semelhança entre imagens é avaliada pela distância entre embeddings gerados pelo FaceNet. O limite padrão é `0.8`, mas pode ser ajustado na linha:
```python
if best_distance <= 0.8 and best_user:
```
Diminuir o valor torna a verificação mais rigorosa, enquanto aumentar torna mais permissiva.

## Contribuição
Se desejar contribuir com melhorias, sinta-se à vontade para abrir uma issue ou um pull request!

## Licença
Este projeto é distribuído sob a licença MIT.

