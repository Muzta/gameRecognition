# import the necessary packages
from keras.models import load_model
import keras.preprocessing.image as kerasImage
import argparse
from os import path

# gpus = tf.config.experimental.list_physical_devices('GPU')
# if gpus:
#     try:
#         # Currently, memory growth needs to be the same across GPUs
#         for gpu in gpus:
#             tf.config.experimental.set_memory_growth(gpu, True)
#         logical_gpus = tf.config.experimental.list_logical_devices('GPU')
#         print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
#     except RuntimeError as e:
#         # Memory growth must be set before GPUs have been initialized
#         print(e)

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True,
	help="name to input dataset we are going to classify")
ap.add_argument("-m", "--model", required=True,
	help="path to trained Keras model")
ap.add_argument("-w", "--width", type=int, default=224,
	help="target spatial dimension width")
ap.add_argument("-e", "--height", type=int, default=224,
	help="target spatial dimension height")
args = vars(ap.parse_args())


# load the input image and resize it to the target spatial dimensions
'''
image = cv2.imread(args["image"])
output = image.copy()
image = cv2.resize(image, (args["width"], args["height"]))
image = image.astype("float32") / 255.0

image = image.reshape((image.shape[0], image.shape[1], 3))
'''
'''
image = kerasImage.image.load_img(args['image'], target_size=(224,224))
image = kerasImage.img_to_array(image)
image = np.array(image)/255.

image = image.reshape(224,224,3)
'''
datasetPath = path.join('datasets',args['dataset'])
image = kerasImage.ImageDataGenerator(rescale=1.0/255.)
image = image.flow_from_directory(datasetPath, (args["width"],args["height"]), class_mode = 'categorical', batch_size=32, shuffle= False)



# load the model and label binarizer
print("[INFO] loading network...")
model = load_model(args["model"])

print("[INFO] loading prediction...")
# make a prediction on the image
preds = model.predict(image)
labels = preds.argmax(axis=-1)


# find the class label index with the largest corresponding
# probability

print('Prediction:')
i = 0
print(labels)
for label in labels:
	print(label)
	print(preds[i][label]*100)
	i = i+1

print(preds)

# draw the class label + probability on the output image

