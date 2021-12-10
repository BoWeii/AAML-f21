import os
import torchvision.models as models
import torch
import torch.nn
from torch.autograd import Variable
import torch.cuda
import torchvision.transforms as transforms
from PIL import Image
import numpy as np

TARGET_IMG_SIZE = 224
img_to_tensor = transforms.ToTensor()


def make_model():
    model = models.vgg16(pretrained=True)  # .features[:]
    model = model.eval()
    return model


def extract_feature(model, imgpath):
    model.eval()
    img = Image.open(imgpath)
    img = img.resize((TARGET_IMG_SIZE, TARGET_IMG_SIZE))
    tensor = img_to_tensor(img)
    tensor = tensor.resize_(1, 3, 224, 224)
    result = model(Variable(tensor))
    # print(result.data.max(1, keepdim=True)[1])
    result_npy = result.data.cpu().numpy()
    return result_npy[0]


if __name__ == "__main__":
    model = make_model()
    imgpath = "../data/input.jpg"
    tmp = extract_feature(model, imgpath)
    print(tmp.shape)
    print(tmp)
    # np.save('Lab2\output.npy', tmp)
    # print model
    model = models.vgg16(pretrained=True)  # .features[:]
    feature = torch.nn.Sequential(*list(model.children())[:])
    print(feature)

"""
# print model
model = models.vgg16(pretrained= True)#.features[:]
feature = torch.nn.Sequential(*list(model.children())[:])
print(feature)
"""

"""
# print layer (bias and weights)
model = models.vgg16(pretrained= True)#.features[:]
#weight_tensor = np.array(model.features[0].weight.data) #features = cnn, classifier = fc
weight_tensor = np.array(model.classifier[6].bias.data)
print(weight_tensor.shape)
print(weight_tensor)
np.save('Lab2\Fc16_bias.npy', weight_tensor)
"""