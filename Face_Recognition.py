from flask import Flask, request, jsonify
import numpy as np
import cv2
from facenet_pytorch import InceptionResnetV1
import torch
import re

app = Flask(__name__)

# Carregar modelo FaceNet pré-treinado
facenet = InceptionResnetV1(pretrained='vggface2').eval()

def preprocess_image(image_file):
    """Converte a imagem para um formato adequado para FaceNet"""
    npimg = np.frombuffer(image_file.read(), np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    return cv2.resize(img, (160, 160))  # Redimensionar para 160x160, necessário para FaceNet

def generate_embedding(image):
    """Gera embeddings de uma imagem usando FaceNet"""
    tensor = torch.tensor(image).permute(2, 0, 1).unsqueeze(0).float() / 255.0  # Transformar para tensor
    embedding = facenet(tensor)
    return embedding.detach().numpy()

def compare_embeddings(embedding1, embedding2):
    """Compara dois embeddings usando distância de similaridade"""
    distance = np.linalg.norm(embedding1 - embedding2)
    return distance

@app.route('/authenticate', methods=['POST'])
def authenticate():
    """Endpoint para autenticação usando FaceNet"""
    image2 = request.files.get("image2")  
    if not image2:
        return jsonify({"status": "error", "message": "Envie a image2 para autenticação"}), 400

    auth_image = preprocess_image(image2)
    auth_embedding = generate_embedding(auth_image)

    images_with_ids = {}
    for field_name in request.files:
        match = re.match(r'images1\[(\d+)\]', field_name)
        if match:
            user_id = match.group(1)
            img = preprocess_image(request.files[field_name])
            embedding = generate_embedding(img)
            images_with_ids[user_id] = embedding

    best_user = None
    best_distance = float('inf')  

    for user_id, registered_embedding in images_with_ids.items():
        distance = compare_embeddings(registered_embedding, auth_embedding)
        if distance < best_distance:  # Menor distância é o melhor match
            best_distance = distance
            best_user = user_id

    # Limite de similaridade (ajuste conforme necessário, ex.: 0.8 para maior rigor)
    if best_distance <= 0.8 and best_user:
        return jsonify({
            "status": "success", 
            "message": f"Usuário {best_user} validado com sucesso!", 
            "userId": int(best_user)
        }), 200
    else:
        return jsonify({"status": "error", "message": "Usuário não reconhecido"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
