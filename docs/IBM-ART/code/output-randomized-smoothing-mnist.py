"""
ART Randomized Smoothing
"""

import keras.backend as k
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Dropout

from art import DATA_PATH
from art.defences import GaussianAugmentation
from art.attacks import FastGradientMethod
from art.classifiers import KerasClassifier
from art.utils import load_dataset, get_file, compute_accuracy
from art.wrappers import RandomizedSmoothing

import numpy as np
%matplotlib inline
import matplotlib.pyplot as plt

# 1. 加载MNIST数据

(x_train, y_train), (x_test, y_test), min_, max_ = load_dataset(str('mnist'))
num_samples_test = 250
x_test = x_test[0:num_samples_test]
y_test = y_test[0:num_samples_test]

# 2. 训练分类器

# 2.1 创建Keras卷积神经网络的基本框架
def cnn_mnist(input_shape, min_val, max_val):
  
    model = Sequential()
    model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=input_shape))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(10, activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    classifier = KerasClassifier(clip_values=(min_val, max_val), 
                                model=model, use_logits=False)
    return classifier

num_epochs = 3

# 2.2 构造和训练一个神经网络
# classifier = cnn_mnist(x_train.shape[1:], min_, max_)
# classifier.fit(x_train, y_train, nb_epochs=num_epochs, batch_size=128)

# import trained model to save time :)
path = get_file('mnist_cnn_original.h5', extract=False, path=DATA_PATH,
                url='https://www.dropbox.com/s/p2nyzne9chcerid/mnist_cnn_original.h5?dl=1')
classifier_model = load_model(path)
classifier = KerasClassifier(clip_values=(min_, max_), model=classifier_model, use_logits=False)

# 2.3 添加高斯噪声并训练两个分类器
sigma1 = 0.25
sigma2 = 0.5

ga = GaussianAugmentation(sigma=sigma1, augmentation=False)
x_new1, _ = ga(x_train)

classifier_ga1 = cnn_mnist(x_train.shape[1:], min_, max_)
classifier_ga1.fit(x_new1, y_train, nb_epochs=num_epochs, batch_size=128)

ga = GaussianAugmentation(sigma=sigma2, augmentation=False)
x_new2, _ = ga(x_train)

classifier_ga2 = cnn_mnist(x_train.shape[1:], min_, max_)
classifier_ga2.fit(x_new2, y_train, nb_epochs=num_epochs, batch_size=128)

# 2.4 创建平滑的分类器
classifier_rs = RandomizedSmoothing(classifier, sample_size=100, scale=0.25, alpha=0.001)
classifier_rs1 = RandomizedSmoothing(classifier_ga1, sample_size=100, scale=sigma1, alpha=0.001)
classifier_rs2 = RandomizedSmoothing(classifier_ga2, sample_size=100, scale=sigma2, alpha=0.001)

# 3. 进行检测

# 3.1 将随机平滑模型的预测结果与原始模型f进行比较
x_preds = classifier.predict(x_test)
x_preds_rs1 = classifier_rs1.predict(x_test)
x_preds_rs2 = classifier_rs2.predict(x_test)
acc, cov = compute_accuracy(x_preds, y_test)
acc_rs1, cov_rs1 = compute_accuracy(x_preds_rs1, y_test)
acc_rs2, cov_rs2 = compute_accuracy(x_preds_rs2, y_test)

print("Original test data (first 250 images):")
print("Original Classifier")
print("Accuracy: {}".format(acc))
print("Coverage: {}".format(cov))
print("Smoothed Classifier, sigma=" + str(sigma1))
print("Accuracy: {}".format(acc_rs1))
print("Coverage: {}".format(cov_rs1))
print("Smoothed Classifier, sigma=" + str(sigma2))
print("Accuracy: {}".format(acc_rs2))
print("Coverage: {}".format(cov_rs2))
"""
4 prediction(s) abstained.
4 prediction(s) abstained.
Original test data (first 250 images):
Original Classifier
Accuracy: 0.996
Coverage: 1.0
Smoothed Classifier, sigma=0.25
Accuracy: 0.9959349593495935
Coverage: 0.984
Smoothed Classifier, sigma=0.5
Accuracy: 1.0
Coverage: 0.984
"""

# 4. 认证精度和半径

# 4.1 计算给定半径的认证精度
def getCertAcc(radius, pred, y_test):

    rad_list = np.linspace(0,2.25,201)
    cert_acc = []
    num_cert = len(np.where(radius > 0)[0])
    for r in rad_list:
        rad_idx = np.where(radius > r)[0]
        y_test_subset = y_test[rad_idx]
        cert_acc.append(np.sum(pred[rad_idx] == np.argmax(y_test_subset, axis=1))/num_cert)
    return cert_acc

# 4.2 计算认证
pred0, radius0 = classifier_rs.certify(x_test, n=500)
pred1, radius1 = classifier_rs1.certify(x_test, n=500)
pred2, radius2 = classifier_rs2.certify(x_test, n=500)

# 4.3 plot certification accuracy wrt to radius
rad_list = np.linspace(0,2.25,201)
plt.plot(rad_list, getCertAcc(radius0, pred0, y_test), 'r-', label='original')
plt.plot(rad_list, getCertAcc(radius1, pred1, y_test), '-', color='cornflowerblue', label='smoothed, $\sigma=$' + str(sigma1))
plt.plot(rad_list, getCertAcc(radius2, pred2, y_test), '-', color='royalblue', label='smoothed, $\sigma=$' + str(sigma2))
plt.xlabel('radius')
plt.ylabel('certified accuracy')
plt.legend()
plt.show()
"""
y: certificated accuracy
x: radius
three: original,smoothed sigma=0.25,smoothed sigma=0.5
"""







