import os
import logging
from flask import Flask, redirect, render_template, request
from flask_cors import CORS
from PIL import Image
import torchvision.transforms.functional as TF
import CNN
import numpy as np
import torch
import pandas as pd

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

# ── Resolve paths relative to this file ──────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Load data ────────────────────────────────────────────────────────────────
disease_info = pd.read_csv(
    os.path.join(BASE_DIR, 'disease_info.csv'), encoding='cp1252'
)
supplement_info = pd.read_csv(
    os.path.join(BASE_DIR, 'supplement_info.csv'), encoding='cp1252'
)

# ── Load model ───────────────────────────────────────────────────────────────
MODEL_PATH = os.path.join(BASE_DIR, 'plant_disease_model_1_latest.pt')
model = None
try:
    model = CNN.CNN(39)
    model.load_state_dict(
        torch.load(MODEL_PATH, map_location=torch.device('cpu'))
    )
    model.eval()
    logger.info('Model loaded successfully from %s', MODEL_PATH)
except FileNotFoundError:
    logger.error(
        'Model file not found at %s. '
        'Download it and place it in the app directory before deploying.',
        MODEL_PATH
    )
except Exception as exc:
    logger.error('Failed to load model: %s', exc)

def prediction(image_path):
    image = Image.open(image_path)
    image = image.resize((224, 224))
    input_data = TF.to_tensor(image)
    input_data = input_data.view((-1, 3, 224, 224))
    output = model(input_data)
    output = output.detach().numpy()
    index = np.argmax(output)
    return index


# ── Ensure uploads directory exists ─────────────────────────────────────────
UPLOADS_DIR = os.path.join(BASE_DIR, 'static', 'uploads')
os.makedirs(UPLOADS_DIR, exist_ok=True)

app = Flask(__name__)
CORS(app)  # Enable CORS for Vercel frontend

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/contact')
def contact():
    return render_template('contact-us.html')

@app.route('/index')
def ai_engine_page():
    return render_template('index.html')

@app.route('/mobile-device')
def mobile_device_detected_page():
    return render_template('mobile-device.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        if model is None:
            return render_template('home.html'), 503
        image = request.files['image']
        filename = image.filename
        file_path = os.path.join(UPLOADS_DIR, filename)
        image.save(file_path)
        logger.info('Image saved: %s', file_path)
        pred = prediction(file_path)
        title = disease_info['disease_name'][pred]
        description = disease_info['description'][pred]
        prevent = disease_info['Possible Steps'][pred]
        image_url = disease_info['image_url'][pred]
        supplement_name = supplement_info['supplement name'][pred]
        supplement_image_url = supplement_info['supplement image'][pred]
        supplement_buy_link = supplement_info['buy link'][pred]
        return render_template('submit.html', title=title, desc=description, prevent=prevent,
                               image_url=image_url, pred=pred, sname=supplement_name,
                               simage=supplement_image_url, buy_link=supplement_buy_link)

@app.route('/market', methods=['GET', 'POST'])
def market():
    return render_template('market.html', supplement_image = list(supplement_info['supplement image']),
                           supplement_name = list(supplement_info['supplement name']), disease = list(disease_info['disease_name']), buy = list(supplement_info['buy link']))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
