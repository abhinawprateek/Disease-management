import os
import logging
from flask import Flask, redirect, render_template, request, url_for
from flask_cors import CORS
from PIL import Image
import torchvision.transforms.functional as TF
import CNN
import numpy as np
import torch
import pandas as pd
import csv
import random

# ── Logging ────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

# ── Base Directory ─────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Load CSV Files ─────────────────────────────────────────────────────────
disease_info = pd.read_csv(
    os.path.join(BASE_DIR, 'disease_info.csv'), encoding='cp1252'
)

# ── Load Model ─────────────────────────────────────────────────────────────
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
    logger.error('Model file not found at %s', MODEL_PATH)

except Exception as exc:
    logger.error('Failed to load model: %s', exc)


# ── Prediction Function ────────────────────────────────────────────────────
def prediction(image_path):
    image = Image.open(image_path)
    image = image.resize((224, 224))
    input_data = TF.to_tensor(image)
    input_data = input_data.view((-1, 3, 224, 224))

    output = model(input_data)
    output = output.detach().numpy()

    index = np.argmax(output)
    return index


# ── Uploads Folder ─────────────────────────────────────────────────────────
UPLOADS_DIR = os.path.join(BASE_DIR, 'static', 'uploads')
os.makedirs(UPLOADS_DIR, exist_ok=True)


# ── Flask App ──────────────────────────────────────────────────────────────
app = Flask(__name__)
CORS(app)


# ── Routes ─────────────────────────────────────────────────────────────────

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


# ── SUBMIT (FIXED) ─────────────────────────────────────────────────────────
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':

        file = request.files.get('file')

        if not file or file.filename == '':
            return "No file uploaded", 400

        filename = file.filename   # ✅ IMPORTANT
        file_path = os.path.join(UPLOADS_DIR, filename)
        file.save(file_path)

        logger.info('Image saved: %s', file_path)

        # Prediction
        pred = prediction(file_path)
        title = disease_info['disease_name'][pred]

        print("Prediction:", title)

        # Load products from CSV
        products = []
        csv_path = os.path.join(BASE_DIR, 'supplement_info.csv')

        with open(csv_path, 'r', encoding='cp1252') as f:
            reader = csv.DictReader(f)
            for row in reader:
                disease_raw = row.get('disease', '')

                if title.lower() in disease_raw.lower():
                    products.append({
                        "name": row.get('name', ''),
                        "image": row.get('image', ''),
                        "link": row.get('link', ''),
                        "type": row.get('type', 'Healthy')
                    })

        # ✅ FIXED RETURN
        return render_template(
            'submit.html',
            title=title,
            filename=filename,   # ✅ THIS FIXES YOUR ERROR
            products=products
        )

    return render_template('index.html')


# ── MARKET (CSV BASED) ─────────────────────────────────────────────────────
@app.route('/market', methods=['GET'])
def market():

    products = []
    csv_path = os.path.join(BASE_DIR, 'supplement_info.csv')

    try:
        with open(csv_path, 'r', encoding='cp1252') as f:
            reader = csv.DictReader(f)

            for row in reader:
                disease_raw = row.get('disease', '')

                formatted_disease = disease_raw.replace('___', ' - ').replace('_', ' ') if disease_raw else ''

                products.append({
                    "name": row.get('name', ''),
                    "image": row.get('image', ''),
                    "disease": formatted_disease,
                    "disease_raw": disease_raw,
                    "link": row.get('link', ''),
                    "type": row.get('type', 'Healthy'),
                    "price": round(random.uniform(15.0, 30.0), 2),
                    "old_price": round(random.uniform(35.0, 50.0), 2),
                    "rating": round(random.uniform(4.0, 5.0), 1)
                })

    except Exception as e:
        logger.error('Failed to load supplements: %s', e)

    disease_query = request.args.get('disease')

    if disease_query:
        recommended_products = [
            p for p in products
            if disease_query.lower() in p["disease_raw"].lower()
        ]

        display_disease = disease_query.replace('___', ' - ').replace('_', ' ')

    else:
        recommended_products = products
        display_disease = None

    return render_template(
        'market.html',
        products=recommended_products,
        disease=display_disease
    )


# ── Run App ────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)