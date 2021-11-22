In Lab2-1:
    Please use python to load data.
    Using numpy.load('filename.npy') to open the npy file.
    Each file is the weights in filters of each layer.
    [64, 3, 3, 3] means that there are "filter_number * channel * filter_size * filter_size"

    The detail of model VGG16 is in the VGG16_detail image.

    You don't have to implement the dropout layer, it's only work while training.

    Your output should be an array which contain 1000 floating point number.

    Your largest output of your VGG16 should be the same of the output.npy I gave. (The 453th number)