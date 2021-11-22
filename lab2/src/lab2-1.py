import numpy as np
from PIL import Image

DATA_PATH = '../data/'

input_shape = (224, 224, 3)
padding = (1, 1)
kernel_size = (3, 3)


def padding(pic):
    n_row = len(pic)
    n_col = len(pic[0])
    channel = len(pic[0][0])
    zero_dot = np.zeros(channel)
    result = np.array([[zero_dot for i in range(n_col + 2)]])
    for i in range(n_row):
        temp = np.concatenate((np.array([zero_dot]), pic[i], np.array([zero_dot])))
        temp = np.expand_dims(temp, 0)
        result = np.concatenate((result, temp))

    result = np.concatenate((result, np.array([[zero_dot for i in range(n_col + 2)]])))
    print("result==>", result)
    print("result,", type(result), len(result))
    print("result,", type(result[0]), len(result[0]))
    print("result,", type(result[0, 0]), len(result[0, 0]))
    print("result,", type(result[0, 0, 0]))
    return result


def MaxPooling2D(pool_size, strides):
    return


def Conv2D(_filter_size, kernel_size, padding, input_shape, index, pic, activation="relu"):
    DATA_FILE = "Conv" + str(index) + "_weights.npy"
    weight = np.load(DATA_PATH + DATA_FILE)
    # print("--->", len(pic))
    # print("--->", len(pic[0]))
    # print("--->", len(pic[0][0]))
    pic = padding(pic)
    # for i in range(len(pic)):
    #     for j in range(len(pic[0])):
    # print("i=", i, "j=", j, "pic=", pic[i][j])
    # print("R-->", pic[i][j][0], "G-->", pic[i][j][1], "B-->", pic[i][j][2])
    # print("--->", pic)
    # pr
    # [64, 3, 3, 3] = "filter_number * channel * filter_size * filter_size"
    return


def vgg_16():
    print("In vgg_16:")
    pic = np.array(Image.open("../input.jpg"))
    print("input-->", len(pic[0][0]))
    # for idx, val in enumerate(INPUT):
    #     print(idx, val)
    # temp = numpy.load(DATA_PATH + 'output.npy')
    print("pic-->", type(pic[0, 0]))
    Conv2D(64, kernel_size, padding=padding, input_shape=input_shape, index=1, pic=pic)
    # Conv2D(64, kernel_size, padding=padding, index=2)
    # MaxPooling2D(pool_size=(2, 2), strides=(2, 2))
    # Conv2D(128, kernel_size, padding=padding, index=3)
    # Conv2D(128, kernel_size, padding=padding, index=4)
    # MaxPooling2D(pool_size=(2, 2), strides=(2, 2))
    # Conv2D(256, kernel_size, padding=padding, index=5)
    # Conv2D(256, kernel_size, padding=padding, index=6)
    # Conv2D(256, kernel_size, padding=padding, index=7)
    # MaxPooling2D(pool_size=(2, 2), strides=(2, 2))
    # Conv2D(512, kernel_size, padding=padding, index=8)
    # Conv2D(512, kernel_size, padding=padding, index=9)
    # Conv2D(512, kernel_size, padding=padding, index=10)
    # MaxPooling2D(pool_size=(2, 2), strides=(2, 2))
    # Conv2D(512, kernel_size, padding=padding, index=11)
    # Conv2D(512, kernel_size, padding=padding, index=12)
    # Conv2D(512, kernel_size, padding=padding, index=13)
    # MaxPooling2D(pool_size=(2, 2), strides=(2, 2))
    # Flatten() #攤平
    # Dense(4096) # fully connected
    # Dense(4096)
    # Dense(1000, activation='softmax')


if __name__ == '__main__':
    vgg_16()
