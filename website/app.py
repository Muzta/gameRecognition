import io
import os
import numpy as np
import cv2
from PIL import Image
from keras.models import load_model
from flask import Flask, abort, render_template, request
# import tensorflow as tf
# from tensorflow.config import experimental
from base64 import b64encode
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png']

# gpus = experimental.list_physical_devices('GPU')
# if gpus:
#     try:
#         # Currently, memory growth needs to be the same across GPUs
#         for gpu in gpus:
#             experimental.set_memory_growth(gpu, True)
#         logical_gpus = experimental.list_logical_devices('GPU')
#         print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
#     except RuntimeError as e:
#         # Memory growth must be set before GPUs have been initialized
#         print(e)

model = os.path.join(os.getcwd(),'website','models','resnet50model88.hdf5')
model = load_model(model)

@app.route('/', methods=['GET', 'POST'])
def index():
    game = ''
    score = ''
    img_data = ''

    if request.method == 'POST':
        # Read the uploaded image and make it workable 
        submited_image = request.files['predict_image']
        filename = secure_filename(submited_image.filename)
        # Check the file is an image
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                abort(400)

        submited_npimg = np.fromstring(submited_image.read(), np.uint8)
        predict_image = cv2.imdecode(submited_npimg, cv2.IMREAD_COLOR)

        # Convert cv2 image to PIL image (cv2 work with brg model, PIL with rgb model)
        pil_img = cv2.cvtColor(predict_image, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(pil_img)

        predicted = image_prediction(predict_image)
        game = predicted[0]
        score = predicted[1]

        if request.files:
            # Prepare uploaded image to be displayed in HTML without saving in memory
            data = io.BytesIO()
            pil_img.save(data, "JPEG")
            encoded_img_data = b64encode(data.getvalue())
            img_data = encoded_img_data.decode('utf-8')

    return render_template("index.html", game=game, score=score, img_data=img_data)

def image_prediction(predict_image):

    image = cv2.resize(predict_image, (224, 224))
    image = image.astype("float") / 255.0
    image = image.reshape((1, image.shape[0], image.shape[1],
		image.shape[2]))

    preds = model.predict(image)
    labels = preds.argmax(axis=-1)

    labelNames = np.array(['Deathloop','It takes two','Metroid Dread','Psychonauts 2','Ratchet and Clank: Rift aparts','Resident Evil Village'])
    
    game_prediction = labels[0]
    game_prediction_name = labelNames[game_prediction]
    model_score = round((preds[0][game_prediction]) * 100, 2)

    return game_prediction_name, model_score

app.run()