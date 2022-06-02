# import the necessary packages
from keras.models import Model
from keras.layers import BatchNormalization, Add, Input
from keras.layers.convolutional import Conv2D, MaxPooling2D, AveragePooling2D
from keras.layers.core import Activation, Flatten, Dense
from keras import backend as K

class ResNet101:

	@staticmethod
	def build(numChannels, imgRows, imgCols, numClasses, activation="relu", weightsPath=None):

		def resnetBlock(input, filters, kernelSize, activation, strides):

			x = Conv2D(filters, 1, padding="same", strides=strides)(input)
			x = BatchNormalization()(x)
			x = Activation(activation)(x)

			x = Conv2D(filters, kernelSize, padding="same", strides=1)(x)
			x = BatchNormalization()(x)
			x = Activation(activation)(x)

			x = Conv2D(filters*4, 1, padding="same", strides=1)(x)
			x = BatchNormalization()(x)

			input = Conv2D(filters*4, 1, strides, "same")(input)

			x = Add()([x,input])
			x = Activation(activation)(x)
			return x


		# initialize the model
		inputShape = (imgRows, imgCols, numChannels)

		# if we are using "channels first", update the input shape
		if K.image_data_format() == "channels_first":
			inputShape = (numChannels, imgRows, imgCols)

		inputs = Input(shape=inputShape)

		x = Conv2D(64, 7, padding="same", strides=2)(inputs)
		x = BatchNormalization()(x)
		x = MaxPooling2D(pool_size=(3,3),strides=2,padding="same")(x)


		for i in range(3):
				x = resnetBlock(x, 64, 3, activation, 1)
		for i in range(4):
			if i == 0:
				x = resnetBlock(x, 128, 3, activation, 2)
			else:
				x = resnetBlock(x, 128, 3, activation, 1)
		for i in range(6):
			if i == 0:
				x = resnetBlock(x, 256, 3, activation, 2)
			else:
				x = resnetBlock(x, 256, 3, activation, 1)
		for i in range(3):
			if i == 0:
				x = resnetBlock(x, 512, 3, activation, 2)
			else:
				x = resnetBlock(x, 512, 3, activation, 1)

		

		x = AveragePooling2D(pool_size = 7, padding="same")(x)

		x = Flatten()(x)
		x = Dense(numClasses, activation ='softmax')(x)

		model = Model(inputs = inputs, outputs = x)
		

        # if a weights path is supplied (inicating that the model was
		# pre-trained), then load the weights
		if weightsPath is not None:
			model.load_weights(weightsPath)
            
		# return the constructed network architecture
		return model