import argparse
import shutil
import os
from keras.optimizers import adam_v2
from keras.preprocessing.image import ImageDataGenerator
from networks.ResNet101 import ResNet101
from networks.ResNet50 import ResNet50
from tempfile import mkdtemp
import matplotlib.pyplot as plt
from networks.utils.stoppingValidations import EarlyStoppingByAccuracy
from networks.utils.stoppingValidations import EarlyStoppingByLoss

BATCH = 32
EPOCHS = 100
ACCURACY = 0.88
LOSS = 0.4


ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", required=True,
	help="path to output trained model")
ap.add_argument("-d", "--dataset", required=False,
	help="path to input dataset of images")
args = vars(ap.parse_args())

# ----------------------------------------------------------------------------------------
# -------------------------------Load Images ---------------------------------------------
# ----------------------------------------------------------------------------------------

print("[INFO] loading images...")



datasetPath = args["dataset"]
tempPath = mkdtemp()

def splitImages(images, point):
    idx = int(len(images) * point)
    return images[:idx], images[idx:]

gameList = [f for f in os.listdir(datasetPath)]

for gameName in gameList:
    tempTrainDst = os.path.join(tempPath,'train',gameName)
    tempTestDst = os.path.join(tempPath,'test',gameName)

    os.makedirs(tempTestDst)
    os.makedirs(tempTrainDst)

    gameDirectory = os.path.join(datasetPath,gameName)
    gameImages = [(os.path.join(gameDirectory,i)) for i in os.listdir(gameDirectory)]

    (gameImage75, gameImage25) = splitImages(gameImages, 0.75)

    for i in gameImage75:
        shutil.copy(i, tempTrainDst)

    for i in gameImage25:
        shutil.copy(i, tempTestDst)


trainImgDataGen = ImageDataGenerator(rescale=1.0/255.)
trainingGenerator = trainImgDataGen.flow_from_directory(os.path.join(tempPath,'train'), (224,224), class_mode = 'categorical', batch_size=BATCH)

testImgDataGen = ImageDataGenerator(rescale=1.0/255.)
testingGenerator = testImgDataGen.flow_from_directory(os.path.join(tempPath,'test'), (224,224), class_mode = 'categorical', batch_size=BATCH)

print(trainingGenerator.class_indices)
print("[INFO] compiling model...") 
opt = adam_v2.Adam()
model = ResNet50.build(numChannels=3, imgRows=224, imgCols=224, numClasses=len(trainingGenerator.class_indices))
model.summary()

model.compile(loss="categorical_crossentropy", optimizer=opt,
	metrics=["accuracy"])


print("[INFO] training...")
callbacks = [EarlyStoppingByAccuracy(monitor='val_accuracy', value=ACCURACY, verbose=1),
    EarlyStoppingByLoss(monitor='val_loss', value=LOSS, verbose=1)]
h = model.fit(trainingGenerator, epochs=EPOCHS, verbose=1, validation_data=testingGenerator, callbacks = callbacks)

print("[INFO] evaluating...")
(loss, accuracy) = model.evaluate(testingGenerator, verbose=1)

print("[INFO] accuracy: {:.2f}%".format(accuracy * 100))

print("[INFO] serializing network and label binarizer...")
model.save(args["model"], save_format="h5")



# summarize history for accuracy
plt.plot(h.history['accuracy'])
plt.plot(h.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()
# summarize history for loss
plt.plot(h.history['loss'])
plt.plot(h.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()

