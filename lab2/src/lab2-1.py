import numpy as np
import torch
import torchvision.transforms as transforms
from PIL import Image

DATA_PATH = '../data/lab2/'

img_to_tensor = transforms.ToTensor()

FILTER_SIZE = 3
POOL_SIZE = 2


def print_weight(weight, name):
    print(name)
    print("filter_number--->", len(weight))
    print("channel--->", len(weight[0]))
    print("filter_size--->", len(weight[0, 0]))
    print("filter_size--->", len(weight[0, 0, 0]))


def padding(image):
    n_row = len(image)
    n_col = len(image[0])
    channel = len(image[0][0])
    zero_dot = np.zeros(channel)
    result = np.array([[zero_dot for i in range(n_col + 2)]])
    for i in range(n_row):
        temp = np.concatenate((np.array([zero_dot]), image[i], np.array([zero_dot])))
        temp = np.expand_dims(temp, 0)
        result = np.concatenate((result, temp))

    result = np.concatenate((result, np.array([[zero_dot for i in range(n_col + 2)]])))
    return result


def gen_empty_result(n_row, n_col, channel):
    zero_dot = np.zeros(channel)
    result = np.array([[zero_dot for i in range(n_col)]])
    for i in range(n_row - 1):
        temp = np.array([[zero_dot for i in range(n_col)]])
        result = np.concatenate((result, temp))
    return result


def calc_conv(bias, weight, image):
    n_row = len(image) - 2
    n_col = len(image[0]) - 2
    n_channel = len(weight[0])
    n_filter = len(weight)
    result = gen_empty_result(n_row, n_row, n_filter)
    # [64, 3, 3, 3] = "filter_number * channel * filter_size * filter_size"
    # [224,224,3]=" size * size * channel "
    for _row in range(n_row):
        for _col in range(n_col):
            for _filter in range(n_filter):
                temp = bias[_filter]
                for i in range(FILTER_SIZE):
                    for j in range(FILTER_SIZE):
                        row = _row + i
                        col = _col + j
                        for _channel in range(n_channel):
                            temp += image[row, col, _channel] * weight[_filter, _channel, i, j]
                result[_row, _col, _filter] = temp if temp > 0 else 0
    return result


def MaxPooling2D(image):
    n_row = len(image)
    n_col = len(image[0])
    n_channel = len(image[0, 0])
    result = gen_empty_result(int(n_row / 2), int(n_col / 2), n_channel)
    for _row in range(int(n_row / 2)):
        for _col in range(int(n_col / 2)):
            for _channel in range(n_channel):
                temp = 0
                for i in range(POOL_SIZE):
                    for j in range(POOL_SIZE):
                        row = _row * 2 + i
                        col = _col * 2 + j
                        if temp < image[row, col, _channel]:
                            temp = image[row, col, _channel]
                result[_row, _col, _channel] = temp
    return result


def Conv2D(index, image):
    bias_file = "Conv" + str(index) + "_bias.npy"
    weight_file = "Conv" + str(index) + "_weights.npy"

    weight = np.load(DATA_PATH + weight_file)
    bias = np.load(DATA_PATH + bias_file)
    image = padding(image)
    print("calc conv ",index)
    result = calc_conv(bias, weight, image)
    # [64, 3, 3, 3] = "filter_number * channel * filter_size * filter_size"
    np.save("conv_result_" + str(index), result)
    return result


def test_Conv(image, weight, bias):
    image = padding(image)
    result = calc_conv(bias, weight, image)
    return result


def Flatten(image):
    n_row = len(image)
    n_col = len(image[0])
    n_channel = len(image[0, 0])
    result = np.zeros(n_row * n_col * n_channel)

    for _channel in range(n_channel):
        temp = _channel * n_row * n_col
        for _row in range(n_row):
            for _col in range(n_col):
                result[temp + _row * n_col + _col] = image[_row, _col, _channel]
    return result


def calc_dense(weight, bias, image, activation):
    input_size = len(image)
    output_len = len(bias)

    for output in range(output_len):
        temp = 0
        for i in range(input_size):
            temp += weight[output][i] * image[i]
        bias[output] += temp
        if bias[output] < 0 and activation == "ReLU":
            bias[output] = 0
    return bias


def Dense(image, index, activation=None):
    bias_file = "Fc" + str(index) + "_bias.npy"
    weight_file = "Fc" + str(index) + "_weights.npy"
    weight = np.load(DATA_PATH + weight_file)
    bias = np.load(DATA_PATH + bias_file)
    print("calc dense_",index)
    result = calc_dense(weight, bias, image, activation)
    np.save("Fc_result_" + str(index), result)
    return result


def transfer_dim(image, _type):
    # me to model
    if _type == "to":
        n_channel = len(image[0, 0])
        n_col = len(image[0])
        n_row = len(image)
        result = gen_empty_result(n_channel, n_row, n_col)
        for _channel in range(n_channel):
            for _row in range(n_row):
                for _col in range(n_col):
                    result[_channel, _row, _col] = image[_row, _col, _channel]
        return result
    # model to me
    if _type == "back":
        n_col = len(image[0, 0])
        n_row = len(image[0])
        n_channel = len(image)
        result = gen_empty_result(n_row, n_col, n_channel)
        for _channel in range(n_channel):
            for _row in range(n_row):
                for _col in range(n_col):
                    result[_row, _col, _channel] = image[_channel, _row, _col]
        return result


def test_func():
    image = np.array([
        [[1, 1], [2, 1], [3, 1], [4, 1]],
        [[5, 2], [6, 2], [7, 2], [8, 2]],
        [[1, 3], [2, 3], [3, 3], [4, 3]],
        [[5, 4], [6, 4], [7, 4], [8, 4]],
    ])
    weight = np.array([
        [[[1, 1, 1],
          [1, 1, 1],
          [1, 1, 1], ],
         [[1, 0, 1],
          [1, 0, 1],
          [1, 0, 1]]],
        [[[1, 0, 1],
          [1, 0, 1],
          [1, 0, 1], ],
         [[1, 0, 1],
          [1, 0, 1],
          [1, 0, 1]]]
    ])
    bias = np.array([2, 1])
    image = test_Conv(image, weight, bias)  # 64
    pooling = MaxPooling2D(image)

def init_vgg16():
    image = Image.open("../data/lab2/input.jpg")
    image = image.resize((224, 224))
    tensor = img_to_tensor(image)
    image = tensor.data.cpu().numpy()
    return transfer_dim(image, "back")

def vgg_16():
    print("In vgg_16:")
    image = init_vgg16()

    image = Conv2D(index=1, image=image)  # 64
    image = Conv2D(index=2, image=image)  # 64
    image = MaxPooling2D(image)
    # --------------------------------------------------
    image = Conv2D(index=3, image=image)  # 128
    image = Conv2D(index=4, image=image)  # 128
    image = MaxPooling2D(image)
    # --------------------------------------------------
    image = Conv2D(index=5, image=image)  # 256
    image = Conv2D(index=6, image=image)  # 256
    image = Conv2D(index=7, image=image)  # 256
    image = MaxPooling2D(image)
    # --------------------------------------------------
    image = Conv2D(index=8, image=image)  # 512
    image = Conv2D(index=9, image=image)  # 512
    image = Conv2D(index=10, image=image)  # 512
    image = MaxPooling2D(image)
    # --------------------------------------------------
    image = Conv2D(index=11, image=image)  # 512
    image = Conv2D(index=12, image=image)  # 512
    image = Conv2D(index=13, image=image)  # 512
    image = MaxPooling2D(image)
    # --------------------------------------------------
    # image = transfer_dim(image, "to")
    # avgPool2d = torch.nn.AdaptiveAvgPool2d(output_size=(7, 7))
    # image = avgPool2d(torch.from_numpy(image))

    # --------------------------------------------------
    image = Flatten(image)  # 攤平

    image = Dense(image, index=14, activation="ReLU")  # fully connected 4096
    image = Dense(image, index=15, activation="ReLU")  # fully connected 4094
    image = Dense(image, index=16) # fully connected 1000
    np.save("my_output", image)
    print("output= ",image)

def print_output():
    image = np.load("my_output.npy")
    print("output",image)

if __name__ == '__main__':
    vgg_16()
    # test_func()
    # print_output()


