from keras.layers.normalization import BatchNormalization
from keras.layers.convolutional import Conv2D, AveragePooling2D, MaxPooling2D, ZeroPadding2D
from keras.layers.core import Activation, Dense
from keras.layers import Flatten, Input, add
from keras.models import Model
from keras.regularizers import l2
from keras import backend as K

class ResNetPreActivation:
	@staticmethod
	def residual_module(data, K, stride, chanDim, red=False, reg=0.0001, bnEps=2e-5, bnMom=0.9):
		shortcut = data
		bn1 = BatchNormalization(axis=chanDim, epsilon=bnEps, momentum=bnMom)(data)
		act1 = Activation("relu")(bn1)
		conv1 = Conv2D(int(K * 0.25), (1, 1), use_bias=False, kernel_regularizer=l2(reg))(act1)

		bn2 = BatchNormalization(axis=chanDim, epsilon=bnEps, momentum=bnMom)(conv1)
		act2 = Activation("relu")(bn2)
		conv2 = Conv2D(int(K * 0.25), (3, 3), strides=stride, padding="same", use_bias=False, kernel_regularizer=l2(reg))(act2)

		bn3 = BatchNormalization(axis=chanDim, epsilon=bnEps, momentum=bnMom)(conv2)
		act3 = Activation("relu")(bn3)
		conv3 = Conv2D(K, (1, 1), use_bias=False, kernel_regularizer=l2(reg))(act3)

		if red:
			shortcut = Conv2D(K, (1, 1), strides=stride, use_bias=False, kernel_regularizer=l2(reg))(act1)
			# shortcut = Conv2D(K, (1, 1), strides=stride, use_bias=False, kernel_regularizer=l2(reg))(shortcut)


		x = add([conv3, shortcut])

		return x

	@staticmethod
	def build(width, height, depth, classes, stages, filters, reg=0.0001, bnEps=2e-5, bnMom=0.9, dataset="cifar"):
		inputShape = (height, width, depth)
		chanDim = -1

		if K.image_data_format() == "channels_first":
			inputShape = (depth, height, width)
			chanDim = 1

		inputs = Input(shape=inputShape)
		x = BatchNormalization(axis=chanDim, epsilon=bnEps, momentum=bnMom)(inputs)

		if dataset == "cifar":
			x = Conv2D(filters[0], (3, 3), use_bias=False, padding="same", kernel_regularizer=l2(reg))(x)

		for i in range(0, len(stages)):
			stride = (1, 1) if i == 0 else (2, 2)
			x = ResNetPreActivation.residual_module(x, filters[i + 1], stride, chanDim, red=True, bnEps=bnEps, bnMom=bnMom)

			for j in range(0, stages[i] - 1):
				x = ResNetPreActivation.residual_module(x, filters[i + 1], (1, 1), chanDim, bnEps=bnEps, bnMom=bnMom)

		x = BatchNormalization(axis=chanDim, epsilon=bnEps, momentum=bnMom)(x)
		x = Activation("relu")(x)
		x = AveragePooling2D((8, 8))(x)

		x = Flatten()(x)
		x = Dense(classes, kernel_regularizer=l2(reg))(x)
		x  =Activation("softmax")(x)

		model = Model(inputs, x, name="resnetPreActivation")

		return model
'''
class ResNetBottlenecks:
	@staticmethod
	def residual_module(data, K, stride, chanDim, red=False, reg=0.0001, bnEps=2e-5, bnMom=0.9):
		shortcut = data

		conv1 = Conv2D(int(K * 0.25), (1, 1), kernel_regularizer=l2(reg))(data)
		bn1 = BatchNormalization(axis=chanDim, epsilon=bnEps, momentum=bnMom)(conv1)
		act1 = Activation("relu")(bn1)

		conv2 = Conv2D(int(K * 0.25), (3, 3), kernel_regularizer=l2(reg))(act1)
		bn2 = BatchNormalization(axis=chanDim, epsilon=bnEps, momentum=bnMom)(conv2)
		act2 = Activation("relu")(bn2)

		conv3 = Conv2D(K, (1, 1), kernel_regularizer=l2(reg))(act2)
		bn3 = BatchNormalization(axis=chanDim, epsilon=bnEps, momentum=bnMom)(conv3)

		act3 = Activation("relu")(bn3)

		if red:
			shortcut = Conv2D(K, (1, 1), strides=stride, use_bias=False, kernel_regularizer=l2(reg))(act1)
			# shortcut = Conv2D(K, (1, 1), strides=stride, use_bias=False, kernel_regularizer=l2(reg))(shortcut)


		x = add([act3, shortcut])

		return x

	@staticmethod
	def build(width, height, depth, classes, stages, filters, reg=0.0001, bnEps=2e-5, bnMom=0.9, dataset="cifar"):
		inputShape = (height, width, depth)
		chanDim = -1

		if K.image_data_format() == "channels_first":
			inputShape = (depth, height, width)
			chanDim = 1

		inputs = Input(shape=inputShape)
		x = BatchNormalization(axis=chanDim, epsilon=bnEps, momentum=bnMom)(inputs)

		if dataset == "cifar":
			x = Conv2D(filters[0], (3, 3), use_bias=False, padding="same", kernel_regularizer=l2(reg))(x)

		for i in range(0, len(stages)):
			stride = (1, 1) if i == 0 else (2, 2)
			x = ResNetBottlenecks.residual_module(x, filters[i + 1], stride, chanDim, red=True, bnEps=bnEps, bnMom=bnMom)

			for j in range(0, stages[i] - 1):
				x = ResNetBottlenecks.residual_module(x, filters[i + 1], (1, 1), chanDim, bnEps=bnEps, bnMom=bnMom)

		x = BatchNormalization(axis=chanDim, epsilon=bnEps, momentum=bnMom)(x)
		x = Activation("relu")(x)
		x = AveragePooling2D((8, 8))(x)

		x = Flatten()(x)
		x = Dense(classes, kernel_regularizer=l2(reg))(x)
		x  =Activation("softmax")(x)

		model = Model(inputs, x, name="resNetbottlenecks")

		return model
'''