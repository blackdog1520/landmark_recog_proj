import os
# import cv2
import numpy as np
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
from keras.applications.resnet50 import ResNet50
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.preprocessing import image

filepath="Best1ResNet.hdf5"
resNet.load_weights("Best1ResNet.hdf5")

print("+"*50, "Model is loaded")

application = Flask(__name__)

@application.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@application.route('/prediction', methods=['GET', 'POST'])
def prediction():
    f =  request.files['img']
    # basepath = 'D:\\7th Sem\\Building Innovative System\\Project 1\\uploads'
    # file_path = os.path.join(basepath, secure_filename(f.filename))
    # f.save(file_path)
    
    basepath = os.path.dirname(__file__)
    file_path = os.path.join(basepath, 'uploads', secure_filename(f.filename))
    f.save(file_path)
    
    img = image.load_img(file_path, target_size=(224, 224))
    # Preprocessing the image
    x = image.img_to_array(img)
    # x = np.true_divide(x, 255)
    x = np.expand_dims(x, axis=0)

    # Be careful how your trained model deals with the input
    # otherwise, it won't make correct prediction!
    x = preprocess_input(x, mode='caffe')

    preds = resnet.predict(x)
    
    # image = cv2.imread(file_path)
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # image = cv2.resize(image, (224,224))
    # image = np.reshape(image, (1, 224, 224, 3))
    
    # pred = resnet.predict(image)
    # pred = np.argmax(pred)
    pred_class = decode_predictions(preds, top=1)   # ImageNet Decode
    result = str(pred_class[0][0][1])               # Convert to string
    
    return render_template("prediction.html", data = result)    


if __name__ == "__main__":
    application.run(debug = True)
    
    
