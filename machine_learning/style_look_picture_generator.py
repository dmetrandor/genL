from PIL import Image
import io
import requests

API_URL = "https://api-inference.huggingface.co/models/prompthero/openjourney"
headers = {"Authorization": "Bearer "}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

def generate_style_look_picture(prompt):
    image_bytes = query({
        "inputs": prompt,
    })
    image = Image.open(io.BytesIO(image_bytes))
    return image